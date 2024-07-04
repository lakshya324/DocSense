import os
import streamlit as st
from dotenv import load_dotenv

import result
import LLM.gemini
import LLM.llama3
import LLM.prompt
from compare import PdfCompare
from pdf_extractor import extract_text

deployed = False
try:
    load_dotenv()

    # Google API Key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise Exception("API Key not found")
except Exception as e:
    api_key = st.secrets["GOOGLE_API_KEY"]
    deployed = True

scans = (
    "Document-Level Cosine Similarity Scan",
    "Sentence-Level Cosine Similarity Scan",
    "Preprocessed Sentence-Level Cosine Similarity Scan",
)

# Create a sidebar for navigation
with st.sidebar:
    st.title("Navigation")
    selected_page = st.radio("Go to", ["Home", "ChatBot"])

# HOME PAGE
if selected_page == "Home":
    st.title("Home")

    # * PDF Upload
    col1, col2 = st.columns(2)
    with col1:
        pdf1 = st.file_uploader("1st PDF", type=["pdf"])
    with col2:
        pdf2 = st.file_uploader("2nd PDF", type=["pdf"])

    # * Scan Type
    st.markdown("---")
    option = st.radio(
        "Choose type of Scan",
        scans,
        horizontal=True,
        captions=["upto 5mins", "upto 5mins", "upto 5mins"],
    )

    if option:
        if option == scans[0]:
            st.subheader(f"{scans[0]}ing")
            st.write(
                "Embeds the entire content of PDFs into vectors using embedding models. Cosine similarity is then calculated to compare the overall semantic content. This is a quick scan and is suitable for comparing large documents."
            )
        elif option == scans[1]:
            st.subheader(f"{scans[1]}ing")
            st.write(
                "Splits PDFs into sentences and embeds each sentence into vectors. The cosine similarity between sentence vectors is computed to assess semantic similarity at the sentence level. This is a moderate scan and is suitable for comparing documents with multiple sections or paragraphs."
            )
        elif option == scans[2]:
            st.subheader(f"{scans[2]}ing")
            st.write(
                "Splits PDFs into sentences, preprocesses them (cleaning, stemming), then embeds the cleaned sentences into vectors. Cosine similarity is used to compare the semantic content of the preprocessed sentences. This is a thorough scan and is suitable for comparing documents with complex or technical content."
            )

        # * Embedding Type
        vector = st.radio(
            "Choose Embedding Type:",
            ("Count Vectorizer", "TF-IDF Vectorizer", "all-MiniLM-L6-v2"),
            index=0,
            horizontal=True,
            captions=["", "", "Method with Longer Processing Time"],
        )

    # * Submit button
    if st.button("Submit"):
        with st.spinner("Comparing PDFs..."):
            embed = (
                0
                if vector == "Count Vectorizer"
                else 1 if vector == "TF-IDF Vectorizer" else 2
            )
            if pdf1 and pdf2:
                text1 = extract_text(pdf1)
                text2 = extract_text(pdf2)
                st.session_state.pdf_text1 = text1
                st.session_state.pdf_text2 = text2
                st.session_state.loaded = False

                pdf_compare = PdfCompare(text1, text2)
                if option == scans[0]:
                    similarity = pdf_compare.quick_scan(embed)
                elif option == scans[1]:
                    similarity = pdf_compare.moderate_scan(embed)
                elif option == scans[2]:
                    similarity = pdf_compare.thorough_scan(embed)

                st.write(f"Similarity Score: {similarity}")
            else:
                st.error("Please upload PDFs to compare.")


elif selected_page == "ChatBot":
    st.title("ChatBot")

    if "loaded" not in st.session_state:
        st.session_state.loaded = False

    if (
        st.button(label="Load PDF", disabled=st.session_state.loaded)
        and st.session_state.loaded == False
        and "pdf_text1" in st.session_state
        and "pdf_text2" in st.session_state
    ):
        with st.spinner("Loading PDFs to Vector DB(It may takes sometime)..."):
            result.load_pdf(st.session_state.pdf_text1, st.session_state.pdf_text2)
        st.session_state.loaded = True

    # Chatbot interaction
    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.form(key="chat_form"):
        user_input = st.text_input("You: ", "")
        # radio button
        if deployed:
            radio_button = st.radio(
                "Choose LLM Model:",
                ["LLAMA 3 (8B) LLM", "Google Gemini LLM"],
                index=1,
                horizontal=True,
                disabled=True,
            )
        else:
            radio_button = st.radio(
                "Choose LLM Model:",
                ["LLAMA 3 (8B) LLM", "Google Gemini LLM"],
                index=1,
                horizontal=True,
            )
        submit_button = st.form_submit_button(
            label="Send", disabled=not (st.session_state.loaded)
        )
        if submit_button and user_input and st.session_state.loaded:
            st.session_state.messages.insert(0, f"You: {user_input}")

            with st.spinner("Finding relevant data from PDFs..."):
                vectors = result.query(user_input)
                prompt = LLM.prompt.prompt(question=user_input, vectors=vectors)
            with st.spinner("Bot is typing..."):
                if radio_button == "LLAMA 3 (8B) LLM":
                    bot_response = LLM.llama3.llama3(prompt)
                else:
                    bot_response = LLM.gemini.gemini(prompt)

            # Placeholder for chatbot response (replace with actual chatbot logic)
            bot_response = f"Bot: {bot_response}"
            st.session_state.messages.insert(0, bot_response)

    # Display the chat history
    for message in st.session_state.messages:
        if message.startswith("You:"):
            styled_message = message.replace(
                "You:", "<b style='color: red;'>You:</b>\t"
            )
            st.markdown(
                f"<div style='text-align: right; background-color: #2f2f2f; padding: 5px; border-radius: 25px;'>{styled_message}</div>",
                unsafe_allow_html=True,
            )
        else:
            styled_message = message.replace(
                "Bot:", "<b style='color: green;'>Bot:</b>\t"
            )
            st.markdown(styled_message, unsafe_allow_html=True)
        # st.markdown("---")

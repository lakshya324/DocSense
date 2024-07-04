import streamlit as st
import time
from compare import PdfCompare
from pdf_extractor import extract_text

# Create a sidebar for navigation
with st.sidebar:
    st.title("Navigation")
    selected_page = st.radio("Go to", ["Home", "ChatBot"])

# HOME PAGE
if selected_page == "Home":    
    st.title("Home")

    #* PDF Upload
    col1, col2 = st.columns(2)
    with col1:
        pdf1 = st.file_uploader("1st PDF", type=["pdf"])
    with col2:
        pdf2 = st.file_uploader("2nd PDF", type=["pdf"])

    #* Scan Type
    st.markdown("---")
    option = st.radio("Choose type of Scan", ("Quick Scan", "Moderate Scan", "Thorough Scan"),horizontal=True,captions=["upto 5mins","upto 5mins","upto 5mins"])

    if option:
        if option == "Quick Scan":
            st.subheader("Quick Scanning")
            st.write("In this type of scanning, PDF's will be embedded to find cosine similarity is found.")
        elif option == "Moderate Scan":
            st.subheader("Moderate Scanning")
            st.write("In this type of scanning, PDF's will be divided into sentences and then embedded to find cosine similarity is found.")
        elif option == "Thorough Scan":
            st.subheader("Thorough Scanning")
            st.write("In this type of scanning, PDF's will be divided into sentences  and then cleaning and stemming of statements is done before embedded to find cosine similarity is found.")
        
        #* Embedding Type
        vector=st.radio("Choose Embedding Type:",("Count Vectorizer","TF-IDF Vectorizer","all-MiniLM-L6-v2"),index=2,horizontal=True)

    #* Submit button
    if st.button("Submit"):
        with st.spinner("Comparing PDFs..."):
            embed=0 if vector=="Count Vectorizer" else 1 if vector=="TF-IDF Vectorizer" else 2
            if pdf1 and pdf2:
                text1 = extract_text(pdf1)
                text2 = extract_text(pdf2)
                st.session_state.pdf_text1 = text1
                st.session_state.pdf_text2 = text2
                st.session_state.loaded = False
                
                pdf_compare = PdfCompare(text1, text2)
                if option=="Quick Scan":
                    similarity = pdf_compare.quick_scan(embed)
                elif option=="Moderate Scan":
                    similarity = pdf_compare.moderate_scan(embed)
                elif option=="Thorough Scan":
                    similarity = pdf_compare.thorough_scan(embed)
                    
                st.write(f"Similarity Score: {similarity}")
            else:
                st.error("Please upload PDFs to compare.")
            
            
        

elif selected_page == "ChatBot":
    st.title("ChatBot")
    
    if "loaded" not in st.session_state:
        st.session_state.loaded =False
    
    if st.button(label="Load PDF",disabled= st.session_state.loaded):
            with st.spinner("Loading PDFs..."):
                time.sleep(5)
                st.session_state.loaded = True

    # Chatbot interaction
    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.form(key="chat_form"):
        user_input = st.text_input("You: ", "")
        submit_button = st.form_submit_button(label="Send",disabled= not(st.session_state.loaded))
        if submit_button and user_input and st.session_state.loaded:
            st.session_state.messages.append(f"You: {user_input}")

            # Simulate a loading state
            with st.spinner("Bot is typing..."):
                time.sleep(2)  # Simulating a delay for bot response

            # Placeholder for chatbot response (replace with actual chatbot logic)
            bot_response = f"Bot: You said '{user_input}'"
            st.session_state.messages.append(bot_response)

    # Display the chat history
    for message in st.session_state.messages:
        st.write(message)

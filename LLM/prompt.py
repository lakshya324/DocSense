def prompt(question: str, vectors: list[str]) -> str:
    prompt_text = (
        f"User have asked '{question}' and the relevant data from PDFs are:\n\n"
    )
    prompt_text += " ".join(vectors)
    prompt_text += "\n\nNow, can you please provide the answer for the user?"
    return prompt_text

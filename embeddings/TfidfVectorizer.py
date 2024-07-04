from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def tfidf_vectorizer(string1, string2) -> float:
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the strings
    tfidf_matrix = vectorizer.fit_transform([string1, string2])

    # Compute cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])

    # Similarity score
    return cosine_sim[0, 0]

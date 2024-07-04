from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def count_vectorizer(string1, string2) -> float:
    # Create Count vectorizer
    vectorizer = CountVectorizer()

    # Fit and transform the strings
    count_matrix = vectorizer.fit_transform([string1, string2])

    # Compute cosine similarity
    cosine_sim = cosine_similarity(count_matrix[0], count_matrix[1])

    # Similarity score
    return cosine_sim[0, 0]

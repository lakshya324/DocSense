from chromadb.utils import embedding_functions
from sklearn.metrics.pairwise import cosine_similarity


def all_MiniLM_L6_v2(string1, string2) -> float:
    # all-MiniLM-L6-v2
    default_ef = embedding_functions.DefaultEmbeddingFunction()

    # Embed the strings
    embedded_text_1 = default_ef(string1)
    embedded_text_2 = default_ef(string2)

    # Compute cosine similarity
    cosine_sim = cosine_similarity(embedded_text_1, embedded_text_2)

    # Similarity score
    return cosine_sim[0, 0]

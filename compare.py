from embeddings import CountVectorizer, TfidfVectorizer, all_MiniLM_L6_v2
from text_preprocessing import segmentation


class PdfCompare:
    def __init__(self, pdf1: str, pdf2: str):
        self.pdf1 = pdf1
        self.pdf2 = pdf2

    def quick_scan(self, embeddings=2):
        if embeddings == 0:
            return CountVectorizer.count_vectorizer(self.pdf1, self.pdf2)
        elif embeddings == 1:
            return TfidfVectorizer.tfidf_vectorizer(self.pdf1, self.pdf2)
        else:
            return all_MiniLM_L6_v2.all_MiniLM_L6_v2(self.pdf1, self.pdf2)

    def moderate_scan(self, embeddings=2):
        pdf1 = segmentation(self.pdf1)
        pdf2 = segmentation(self.pdf2)
        if embeddings == 0:
            similarity_matrix = []
            for i in pdf1:
                for j in pdf2:
                    similarity_matrix.append(CountVectorizer.count_vectorizer(i, j))
            return sum(similarity_matrix) / len(similarity_matrix)
        elif embeddings == 1:
            similarity_matrix = []
            for i in pdf1:
                for j in pdf2:
                    similarity_matrix.append(TfidfVectorizer.tfidf_vectorizer(i, j))
            return sum(similarity_matrix) / len(similarity_matrix)
        else:
            return all_MiniLM_L6_v2.all_MiniLM_L6_v2(pdf1, pdf2)

    def thorough_scan(self, embeddings=2):
        pdf1 = segmentation(self.pdf1, detailed=True)
        pdf2 = segmentation(self.pdf2, detailed=True)
        if embeddings == 0:
            similarity_matrix = []
            for i in pdf1:
                for j in pdf2:
                    similarity_matrix.append(CountVectorizer.count_vectorizer(i, j))
            return sum(similarity_matrix) / len(similarity_matrix)
        elif embeddings == 1:
            similarity_matrix = []
            for i in pdf1:
                for j in pdf2:
                    similarity_matrix.append(TfidfVectorizer.tfidf_vectorizer(i, j))
            return sum(similarity_matrix) / len(similarity_matrix)
        else:
            return all_MiniLM_L6_v2.all_MiniLM_L6_v2(pdf1, pdf2)

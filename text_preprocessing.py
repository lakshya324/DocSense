import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


def segmentation(text: str, detailed=False) -> list[str]:
    text = text.split("\n")
    for i in range(len(text)):
        text[i] = re.sub("[^a-zA-Z0-9%.,]", " ", text[i])
        text[i] = text[i].lower()

        if detailed:
            text[i] = text[i].split()
            ps = PorterStemmer()
            text[i] = [
                ps.stem(word)
                for word in text[i]
                if not word in set(stopwords.words("english"))
            ]
            text[i] = " ".join(text[i])

    text = [x for x in text if x]

    return text

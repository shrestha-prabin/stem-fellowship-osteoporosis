from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

# Create a set of English stopwords
stop_words = set(stopwords.words("english"))

# Initialize the lemmatizer and stemmer
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()


def process_text(text):
    """
    Performs stemming, lemmatization, and stopword removal on input text.

    Args:
        text: The input text string.

    Returns:
        The processed text string.
    """
    if not isinstance(text, str):
        return ""

    # Tokenize the input text
    tokens = word_tokenize(text)

    # Convert tokens to lowercase and remove stopwords
    processed_tokens = [
        word.lower()
        for word in tokens
        if word.lower() not in stop_words and word.isalpha()
    ]

    # Part-of-speech tagging for accurate lemmatization
    pos_tags = pos_tag(processed_tokens)

    # Lemmatize the remaining tokens
    lemmatized_tokens = []
    for word, tag in pos_tags:
        wntag = tag[0].lower()
        wntag = wntag if wntag in ["a", "r", "n", "v"] else "n"
        lemmatized_tokens.append(lemmatizer.lemmatize(word, wntag))

    # Stem the lemmatized tokens
    stemmed_tokens = [stemmer.stem(word) for word in lemmatized_tokens]

    # Join the processed tokens back into a string
    return " ".join(stemmed_tokens)

import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('top2k_book_descriptions.csv')
df = df[(df['language_code'] == 'eng') | (df['language_code'] == 'en-US')]
data  = df[['original_title','description','authors']]
data = data.dropna(subset=['description']).reset_index()

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    # Lowercasing
    text = text.lower()
    # Removing punctuation
    text = text.translate(str.maketrans(' ', ' ', string.punctuation))
    # Tokenization
    tokens = word_tokenize(text)
    # Removing stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    tokens = [token for token in tokens if token != 'isbn']
    tokens = [token for token in tokens if token != 'isbn13']
    tokens = [token for token in tokens if token != 'isbn10']
    # Remove numerical digits
    tokens = [token for token in tokens if not token.isdigit()]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return ' '.join(tokens)


# Preprocess the description
data['processed_text'] = data['description'].apply(preprocess_text)


vectorizer = TfidfVectorizer()


tfidf_matrix = vectorizer.fit_transform(data['description'])

# Convert the TF-IDF matrix to DataFrame
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out(), index=data.index)
# Compute the cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to get recommendations based on cosine similarity
def get_recommendations(book_index, cosine_sim=cosine_sim, df=df, top_n=5):
    
    matching_books = df[df['original_title'] == book_index]
    
    if not matching_books.empty:
        idx = matching_books.index[0] if isinstance(book_index, str) else book_index
        sim_scores = list(enumerate(cosine_sim[idx]))
        # Rest of the recommendation code...
    else:
        # Handle case when no matching books are found
        return "No matching books found"
    
    # Get pairwise similarity scores with other books
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort books based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the top N similar books (excluding itself)
    sim_scores = sim_scores[1:top_n+1]
    
    # Get book indices
    book_indices = [i[0] for i in sim_scores]
    
    # Return recommended books
    return df.iloc[book_indices]

# Example: Get recommendations for a book by index or title
# book_index_or_title = 'The Hunger Games'  # Change this to the book index or title you want recommendations for
# recommendations = get_recommendations(book_index_or_title)
# print(recommendations[['original_title', 'authors']])

import pandas as pd
import string
import nltk
import pickle
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report

# Download required NLTK data
nltk.download('stopwords')

def clean_text(text):
    """Clean and preprocess text data"""
    text = str(text).lower()
    text = ''.join([c for c in text if c not in string.punctuation])
    words = text.split()
    words = [word for word in words if word not in stopwords.words('english')]
    return ' '.join(words)

def train_model():
    # Load the dataset
    print("Loading dataset...")
    df = pd.read_csv("spam.csv", encoding='latin-1')
    
    # Select relevant columns and rename them
    df = df[['v1', 'v2']]
    df.columns = ['label', 'text']
    
    # Convert labels to numbers: spam = 1, ham = 0
    df['label'] = df['label'].map({'spam': 1, 'ham': 0})
    
    # Clean text
    print("Preprocessing text...")
    df['cleaned_text'] = df['text'].apply(clean_text)
    
    # Create TF-IDF features
    print("Creating TF-IDF features...")
    tfidf = TfidfVectorizer(max_features=5000)
    X = tfidf.fit_transform(df['cleaned_text']).toarray()
    y = df['label']
    
    # Split the data
    print("Splitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train the model
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate the model
    print("\nEvaluating model performance...")
    y_pred = model.predict(X_test)
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model and vectorizer
    print("\nSaving model and vectorizer...")
    with open('model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)
    
    with open('vectorizer.pkl', 'wb') as vectorizer_file:
        pickle.dump(tfidf, vectorizer_file)
    
    print("Training completed! Model and vectorizer have been saved.")

if __name__ == "__main__":
    train_model()

from app import db
from models.core import EmployeeProfile
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
import numpy as np

class TextService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=100)
        self.tsne = TSNE(n_components=2, random_state=42, perplexity=3)

    def analyze_text(self, content, user_id):
        # Save text data to the database
        text_data = EmployeeProfile(user_id=user_id, summary=content)
        db.session.add(text_data)
        db.session.commit()

        # Perform text analysis
        summary = summarize(content)
        extracted_keywords = keywords(content, words=5, lemmatize=True)
        sentiment = TextBlob(content).sentiment

        return summary, extracted_keywords, sentiment

    def get_profile_by_user_id(self, user_id):
        # Retrieve the EmployeeProfile for a specific user
        return EmployeeProfile.query.filter_by(user_id=user_id).first()

    def update_profile_summary(self, user_id, new_summary):
        # Update the summary for the EmployeeProfile of a specific user
        profile = self.get_profile_by_user_id(user_id)
        if profile:
            profile.summary = new_summary
            db.session.commit()
            return profile
        return None

    def generate_tsne_visualization(self, content):
        # Preprocess the content (you might want to add more preprocessing steps)
        processed_content = content.lower().split()

        # Vectorize the text
        vector = self.vectorizer.fit_transform([' '.join(processed_content)])

        # Apply t-SNE
        tsne_result = self.tsne.fit_transform(vector.toarray())

        return {
            "x": float(tsne_result[0][0]),
            "y": float(tsne_result[0][1])
        }

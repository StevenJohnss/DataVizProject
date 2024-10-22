from ..extension import db
from ..models.core import EmployeeProfile, User
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
import numpy as np

class TextService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=100)
        self.tsne = TSNE(n_components=2, random_state=42, perplexity=1)

    def analyze_text(self, content, user_id):
        # Save text data to the database
        # text_data = self.update_profile_summary(user_id=user_id, new_summary=content)

        # Perform text analysis
        summary = summarize(content)
        extracted_keywords = keywords(content, words=5, lemmatize=True)
        sentiment = TextBlob(content).sentiment

        return summary, extracted_keywords, sentiment

    def get_profile_by_user_id(self, user_id):
        # Retrieve the User and their associated EmployeeProfile for a specific user
        user = User.query.filter_by(id=user_id).first()
        return user, user.profile

    def update_profile_summary(self, user_id, new_summary):
        # Update the summary for the EmployeeProfile of a specific user
        user, profile = self.get_profile_by_user_id(user_id)
        if profile:
            profile = profile[0]
            profile.summary = new_summary
        else:
            # Create a new profile if it does not exist
            profile = EmployeeProfile(user_id=user_id, summary=new_summary)
            db.session.add(profile)
        db.session.commit()
        return profile
        

    def generate_text_visualization(self, content):
        # Preprocess the content (you might want to add more preprocessing steps)
        processed_content = content.lower().split()

        # Vectorize the text
        vector = self.vectorizer.fit_transform([' '.join(processed_content)])

        # For single samples, return a random point in 2D space
        if vector.shape[0] == 1:
            return {
                "x": float(np.random.uniform(-1, 1)),
                "y": float(np.random.uniform(-1, 1))
            }

        # Apply t-SNE only if we have multiple samples
        tsne_result = self.tsne.fit_transform(vector.toarray())

        return {
            "x": float(tsne_result[0][0]),
            "y": float(tsne_result[0][1])
        }

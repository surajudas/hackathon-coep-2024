from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

def docs_content_reader(file_paths: list) -> list:

    # Read the contents of the files
    documents = [open(file_path, 'r').read() for file_path in file_paths]

    # Initialize TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()

    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    # Compute cosine similarity between all pairs of documents
    cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Calculate average similarity scores
    average_similarities = cosine_similarities.mean(axis=0)

    # Create a bar plot
    sns.barplot(x=range(len(file_paths)), y=average_similarities)
    plt.savefig('static/barplot.png')

    # Plot the similarity matrix as a heatmap
    sns.heatmap(cosine_similarities, annot=True, cmap='coolwarm')
    plt.savefig('static/heatmap.png')

    return ['static/heatmap.png', 'static/barplot.png']

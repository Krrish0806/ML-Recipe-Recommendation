import tkinter as tk
from tkinter import ttk, scrolledtext
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import pandas as pd

# =========================
#  Load your dataset
# =========================
# Make sure 'dataframe' is already loaded, or load it here:
# dataframe = pd.read_csv("your_dataset.csv")

# Vectorize ingredients
vectorizer = TfidfVectorizer()
X_ingredients = vectorizer.fit_transform(dataframe['Ingredients'])

# Train KNN model
knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=5)
knn.fit(X_ingredients)

# =========================
#  Tkinter UI setup
# =========================
root = tk.Tk()
root.title("Recipe Recommender")
root.geometry("700x500")
root.configure(bg="#f5f5f5")

title_label = tk.Label(
    root, 
    text="🍳 Recipe Recommender", 
    font=("Helvetica", 20, "bold"), 
    bg="#f5f5f5", 
    fg="#333"
)
title_label.pack(pady=15)

# Input box
input_label = tk.Label(root, text="Enter ingredients you have:", font=("Helvetica", 12), bg="#f5f5f5")
input_label.pack()

input_box = tk.Entry(root, width=70, font=("Helvetica", 12))
input_box.pack(pady=10)

# Result box
result_box = scrolledtext.ScrolledText(root, width=80, height=15, font=("Helvetica", 11), wrap=tk.WORD)
result_box.pack(pady=10)

# =========================
#  Recommendation function
# =========================
def recommend_recipes():
    user_input = input_box.get()
    if not user_input.strip():
        result_box.delete(1.0, tk.END)
        result_box.insert(tk.END, "Please enter at least one ingredient.")
        return

    # Transform input and get nearest recipes
    user_vec = vectorizer.transform([user_input])
    distances, indices = knn.kneighbors(user_vec, n_neighbors=5)

    result_box.delete(1.0, tk.END)
    result_box.insert(tk.END, f"Top recipe matches for: '{user_input}'\n\n")

    for i in range(len(indices[0])):
        title = dataframe.iloc[indices[0][i]]['Title']
        ingredients = dataframe.iloc[indices[0][i]]['Ingredients']
        result_box.insert(tk.END, f"{i+1}. {title}\n")
        result_box.insert(tk.END, f"   Ingredients: {ingredients[:150]}...\n\n")

# Button
search_button = ttk.Button(root, text="Find Recipes", command=recommend_recipes)
search_button.pack(pady=10)


root.mainloop()


from surprise import KNNWithMeans

# To use item-based cosine similarity
sim_options = {
    "name": "pearson",
    "user_based": False,  # Compute  similarities between items
}
algo = KNNWithMeans(sim_options=sim_options)

if __name__ == "__main__":
    app.run(debug=False)

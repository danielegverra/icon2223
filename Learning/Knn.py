from sklearn.neighbors import KNeighborsRegressor
from ModelInitializer import modelInitializer
from KFold import kFoldCrossValidation


import pickle as pk


# Initialize the input features X and target values
X, y = modelInitializer()


# Create an instance of KNeighborsRegressor with specified parameters
model = KNeighborsRegressor(n_neighbors=3, weights="distance", algorithm="brute", p=2)


# Train the model
model.fit(X, y)


# Model serialization: Save the trained model to a file using pickle
with open("Storage/knn.pickle", "wb") as f:
    pk.dump(model, f)


# Perform k-fold cross-validation and compute evaluation metrics
kFoldCrossValidation(model, X, y)

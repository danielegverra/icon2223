import pickle as pk
from sklearn.tree import DecisionTreeRegressor
from ModelInitializer import modelInitializer
from KFold import kFoldCrossValidation

# Initialize the input features X and target values y
X, y = modelInitializer()

# Create an instance of DecisionTreeRegressor with specified parameters
model = DecisionTreeRegressor(max_depth=6, min_samples_leaf=2, min_samples_split=5, random_state=4, criterion="friedman_mse")

# Train the model
model.fit(X, y)

# Model serialization: Save the trained model to a file using pickle
with open("Storage/regressionTree.pickle", "wb") as f:
    pk.dump(model, f)

# Perform k-fold cross-validation and compute evaluation metrics
kFoldCrossValidation(model, X, y)

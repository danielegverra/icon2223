import pickle as pk
from sklearn.neighbors import KNeighborsRegressor
from ModelInitializer import modelInitializer
from KFold import kFoldCrossValidation


X, y = modelInitializer()

model = KNeighborsRegressor(n_neighbors=7, metric="euclidean", weights="uniform")
model.fit(X, y)

# Model serialization
with open("Storage/knn.pickle", "wb") as f:
    pk.dump(model, f)

kFoldCrossValidation(model, X, y)

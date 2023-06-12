import pickle as pk
from sklearn.tree import DecisionTreeRegressor
from ModelInitializer import modelInitializer
from KFold import kFoldCrossValidation


X, y = modelInitializer()

model = DecisionTreeRegressor(max_depth=15, min_samples_leaf=15)
model.fit(X, y)

# Model serialization
with open("Storage/regressionTree.pickle", "wb") as f:
    pk.dump(model, f)

kFoldCrossValidation(model, X, y)

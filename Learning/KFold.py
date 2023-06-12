from numpy import mean
from sklearn.model_selection import ShuffleSplit, cross_val_score


def kFoldCrossValidation(model, X, y):
    folds = ShuffleSplit(n_splits=3, random_state=0)

    r2 = mean(cross_val_score(model, X, y, cv=folds, scoring="r2"))
    print("r2: ", r2)
    abs = -mean(
        cross_val_score(model, X, y, cv=folds, scoring="neg_mean_absolute_error")
    )
    print("neg_mean_absolute_error: ", abs)
    mse = -mean(
        cross_val_score(model, X, y, cv=folds, scoring="neg_mean_squared_error")
    )
    print("neg_mean_squared_error: ", mse)
    max_error = -mean(cross_val_score(model, X, y, cv=folds, scoring="max_error"))
    print("max_error: ", max_error)

from numpy import mean
from sklearn.model_selection import ShuffleSplit, cross_val_score


# Perform k-fold cross-validation and compute evaluation metrics
# for the given model and dataset.
def kFoldCrossValidation(model, X, y):
    # Creating a data splitting strategy
    folds = ShuffleSplit(n_splits=3, random_state=0)

    # Compute the mean R-squared score using cross-validation
    r2 = mean(cross_val_score(model, X, y, cv=folds, scoring="r2"))
    print("r2: ", r2)

    # Compute the mean negative mean absolute error using cross-validation
    abs = -mean(
        cross_val_score(model, X, y, cv=folds, scoring="neg_mean_absolute_error")
    )
    print("neg_mean_absolute_error: ", abs)

    # Compute the mean negative mean squared error using cross-validation
    mse = -mean(
        cross_val_score(model, X, y, cv=folds, scoring="neg_mean_squared_error")
    )
    print("neg_mean_squared_error: ", mse)

    # Compute the mean negative max error using cross-validation
    max_error = -mean(cross_val_score(model, X, y, cv=folds, scoring="max_error"))
    print("max_error: ", max_error)

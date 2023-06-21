from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder


import pandas as pd


# Initialize the model by preprocessing the dataset
def modelInitializer():
    # Read the dataset from a CSV file
    dataset = pd.read_csv("Storage/Dataframe.csv")

    # Define columns to be normalized
    normalizeCol = [
        "Rating",
        "Rating Count",
        "Centre Distance",
        "Tourism Rate",
        "Age",
        "Surface",
        "Height",
        "Density",
    ]

    # Scale the selected columns using Min-Max scaling
    scaler = MinMaxScaler()
    dataset[normalizeCol] = scaler.fit_transform(dataset[normalizeCol])

    # Prepare the input features (X) and target values (y)
    X = dataset.drop("Tourism Priority", axis=1)

    y = dataset["Tourism Priority"]

    return X, y

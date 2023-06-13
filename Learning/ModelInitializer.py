from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder

import pandas as pd


# Initialize the model by preprocessing the dataset
def modelInitializer():
    # Read the dataset from a CSV file
    dataset = pd.read_csv("Storage/Dataframe.csv")

    # Convert specific columns to integer type
    dataset["Handicap Accessability"] = dataset["Handicap Accessability"].astype(int)
    dataset["Impressive"] = dataset["Impressive"].astype(int)

    # Convert strings attributes in continous attributes
    encoder = OneHotEncoder()
    encoded = encoder.fit_transform(dataset["Type"].values.reshape(-1, 1))
    typeCols = pd.DataFrame(
        encoded.toarray(),
        columns=encoder.get_feature_names_out(["Type"]),
    )
    dataset = dataset.drop("Type", axis=1)
    dataset = pd.concat([dataset, typeCols], axis=1)

    # Prepare the input features (X) and target values (y)
    X = dataset.drop("Rating", axis=1)
    y = dataset["Rating"]

    # Define columns to be normalized
    normalizeCol = [
        "Rating Count",
        "Centre Distance",
        "Tourism Rate",
        "Age",
        "Surface",
        "Height",
        "Price",
        "Density",
        "Time to Visit",
    ]

    # Scale the selected columns using Min-Max scaling
    scaler = MinMaxScaler()
    X[normalizeCol] = scaler.fit_transform(X[normalizeCol])

    return X, y

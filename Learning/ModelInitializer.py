from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder

import pandas as pd


def modelInitializer():
    dataset = pd.read_csv("Storage/Dataframe.csv")

    dataset["Handicap Accessability"] = dataset["Handicap Accessability"].astype(int)
    dataset["Impressive"] = dataset["Impressive"].astype(int)

    encoder = OneHotEncoder()
    encoded = encoder.fit_transform(dataset["Type"].values.reshape(-1, 1))
    typeCols = pd.DataFrame(
        encoded.toarray(),
        columns=encoder.get_feature_names_out(["Type"]),
    )
    dataset = dataset.drop("Type", axis=1)
    dataset = pd.concat([dataset, typeCols], axis=1)

    X = dataset.drop("Rating", axis=1)
    y = dataset["Rating"]

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

    scaler = MinMaxScaler()

    X[normalizeCol] = scaler.fit_transform(X[normalizeCol])

    return X, y

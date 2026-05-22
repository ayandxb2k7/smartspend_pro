from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

def categorize_expense(title):
    title = title.lower()
    keywords = {
        "Food": ["food","restaurant","cafe"],
        "Transport": ["uber","petrol","bus","metro"],
        "Entertainment": ["movie","netflix","game"]
    }

    for category, words in keywords.items():
        if any(word in title for word in words):
            return category
    return "Other"

def predict_expense(df):
    if len(df) < 2:
        return 0

    df["day"] = pd.to_datetime(df["date"]).dt.day
    X = df[["day"]]
    y = df["amount"]

    model = LinearRegression()
    model.fit(X,y)

    next_day = np.array([[df["day"].max()+1]])
    return round(model.predict(next_day)[0],2)
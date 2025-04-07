from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

data_file = "filtered_stackoverflow_2015_2025_clean.csv"
df = pd.read_csv(data_file)
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year

@app.route("/")
def home():
    return {
        "message": "🔥 Welcome to StackOverflow JSON API!",
        "endpoints": {
            "/questions": "Get all data",
            "/questions?year=2023": "Filter by year",
            "/questions?language=python": "Filter by language",
            "/questions?year=2023&language=python": "Both filters"
        }
    }

@app.route("/questions", methods=["GET"])
def get_questions():
    year = request.args.get("year", type=int)
    language = request.args.get("language", type=str)

    filtered = df

    if year:
        filtered = filtered[filtered["Year"] == year]

    if language:
        filtered = filtered[filtered["Language"].str.lower() == language.lower()]

    result = filtered[["Question ID", "Language", "Date"]].to_dict(orient="records")
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app) 

df = pd.read_csv("merged_stackoverflow.csv")

@app.route('/')
def home():
    return jsonify({"message": "Welcome to StackOverflow JSON API!"})
    
@app.route('/languages', methods=['GET'])
def get_languages():
    unique_languages = df['Language'].dropna().unique()
    return jsonify(sorted(unique_languages))

@app.route('/data', methods=['GET'])
def get_data():
    year = request.args.get('year')
    language = request.args.get('language')

    filtered_df = df.copy()

    if year:
        filtered_df = filtered_df[filtered_df['Date'].str.startswith(year)]

    if language:
        filtered_df = filtered_df[filtered_df['Language'].str.lower() == language.lower()]

    result = filtered_df.to_dict(orient='records')
    return jsonify(result)

@app.route('/trend', methods=['GET'])
def get_trend():
    df['Year'] = pd.to_datetime(df['Date']).dt.year
    trend_data = df.groupby(['Year', 'Language']).size().reset_index(name='Count')
    
    result = trend_data.to_dict(orient='records')
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

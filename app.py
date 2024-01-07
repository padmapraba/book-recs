from flask import Flask, render_template, request
import pandas as pd
from get_recs import get_recommendations


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_book = request.form['book_title']
    print(selected_book)
    recommendations = get_recommendations(selected_book)
    print(recommendations, '*****')
    recs = recommendations[['original_title', 'authors']]
    return render_template('recommendations.html', recommendations=recs)


if __name__ == '__main__':
    app.run(debug=True)


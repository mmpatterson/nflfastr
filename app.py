from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"
    
@app.route("/api/v1.0/play-by-play/<year>", methods = ['GET', 'POST'])
def play_by_play(year):
    """Fetch nflfastR gameplay data for the given year."""
    if request.method == 'GET':
        year_df = pd.read_csv(f'https://github.com/nflverse/nflfastR-data/blob/master/data/play_by_play_{year}.csv.gz?raw=true', compression = 'gzip')
        year_dict = year_df.to_dict(orient="records")
        return jsonify(year_dict)
    elif request.method == 'POST':
        # Column must be in list form
        columns = request.json['columns']
        year_df = pd.read_csv(f'https://github.com/nflverse/nflfastR-data/blob/master/data/play_by_play_{year}.csv.gz?raw=true', compression = 'gzip', usecols=columns)
        year_dict = year_df.to_dict(orient="records")
        return jsonify(year_dict)
if __name__ == "__main__":
    app.run(debug=True)
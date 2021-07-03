from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"
    
@app.route("/api/v1.0/play-by-play/<year>", methods = ['GET', 'POST'])
def play_by_play(year, orient = 'records'):
    """Fetch nflfastR gameplay data for the given year."""
    if request.method == 'GET':
        year_df = pd.read_csv(f'https://github.com/nflverse/nflfastR-data/blob/master/data/play_by_play_{year}.csv.gz?raw=true', compression = 'gzip')
        year_dict = year_df.to_dict(orient="records")
        return jsonify(year_dict)
    elif request.method == 'POST':
        # Column must be in list form
        columns = request.json['columns']
        try:
            orient = request.json['orient']
        except:
            orient = orient
        year_df = pd.read_csv(f'https://github.com/nflverse/nflfastR-data/blob/master/data/play_by_play_{year}.csv.gz?raw=true', compression = 'gzip', usecols=columns)
        year_dict = year_df.to_json(orient=orient)
        return year_dict

@app.route("/api/v1.0/roster/aggregate", methods = ['GET', 'POST'])
def roster_agg(orient = 'records'):
    """Fetch all nflfastR roster data."""
    if request.method == 'GET':
        roster_df = pd.read_csv(f'https://github.com/nflverse/nflfastR-roster/blob/master/data/nflfastR-roster.csv.gz?raw=true', compression = 'gzip')
        roster_dict = roster_df.to_dict(orient="records")
        return jsonify(roster_dict)
    elif request.method == 'POST':
        # Column must be in list form
        columns = request.json['columns']
        try:
            orient = request.json['orient']
        except:
            orient = orient
        roster_df = pd.read_csv(f'https://github.com/nflverse/nflfastR-roster/blob/master/data/nflfastR-roster.csv.gz?raw=true', compression = 'gzip', usecols=columns)
        roster_dict = roster_df.to_json(orient=orient)
        return roster_dict

@app.route("/api/v1.0/roster/<year>", methods = ['GET', 'POST'])
def roster_year(year, orient = 'records'):
    """Fetch nflfastR roster data for the given year."""
    if request.method == 'GET':
        roster_df = pd.read_csv(f'https://github.com/nflverse/nflfastR-roster/blob/master/data/seasons/roster_{year}.csv?raw=true')
        roster_dict = roster_df.to_dict(orient="records")
        return jsonify(roster_dict)
    elif request.method == 'POST':
        # Column must be in list form
        columns = request.json['columns']
        try:
            orient = request.json['orient']
        except:
            orient = orient
        roster_df = pd.read_csv(f'https://github.com/nflverse/nflfastR-roster/blob/master/data/seasons/roster_{year}.csv?raw=true', usecols=columns)
        roster_dict = roster_df.to_json(orient=orient)
        return roster_dict

if __name__ == "__main__":
    app.run(debug=True)
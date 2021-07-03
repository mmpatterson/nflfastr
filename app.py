from flask import Flask, render_template, jsonify, request, redirect, url_for
import pandas as pd

app = Flask(__name__)
@app.route('/')
def index():
    return render_template("templates/index.html")
    
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

# ******************************************
# ENDPOINT CURRENTLY NOT IN USE DUE TO TIMEOUT ERROR
# ******************************************

# @app.route("/api/v1.0/roster/aggregate", methods = ['GET', 'POST'])
# def roster_agg(orient = 'records'):
#     """Fetch all nflfastR roster data."""
#     if request.method == 'GET':
#         roster_df = pd.read_csv(f'https://github.com/nflverse/nflfastR-roster/blob/master/data/nflfastR-roster.csv.gz?raw=true', compression = 'gzip')
#         roster_dict = roster_df.to_dict(orient="records")
#         return jsonify(roster_dict)
#     elif request.method == 'POST':
#         # Column must be in list form
#         columns = request.json['columns']
#         try:
#             orient = request.json['orient']
#         except:
#             orient = orient
#         roster_df = pd.read_csv(f'https://github.com/nflverse/nflfastR-roster/blob/master/data/nflfastR-roster.csv.gz?raw=true', compression = 'gzip', usecols=columns)
#         roster_dict = roster_df.to_json(orient=orient)
#         return roster_dict

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

@app.route("/api/v1.0/logos", methods = ['GET'])
def logos(orient = 'records'):
    """Fetch nflfastR logo data."""
    logo_df = pd.read_csv(f'https://github.com/nflverse/nfldata/blob/master/data/logos.csv?raw=true')
    logo_dict = logo_df.to_dict(orient="records")
    return jsonify(logo_dict)


@app.route("/api/v1.0/draft_picks", methods = ['GET', 'POST'])
def draft_picks(orient = 'records'):
    """Fetch nflfastR draft data."""
    if request.method == 'GET':
        draft_df = pd.read_csv(f'https://github.com/nflverse/nfldata/blob/master/data/draft_picks.csv?raw=true')
        draft_dict = draft_df.to_dict(orient="records")
        return jsonify(draft_dict)
    elif request.method == 'POST':
        # Make years a list
        years = request.json['years']
        try:
            orient = request.json['orient']
        except:
            orient = "records"
        draft_df = pd.read_csv(f'https://github.com/nflverse/nfldata/blob/master/data/draft_picks.csv?raw=true')
        draft_df = draft_df[draft_df.season.isin([int(year) for year in years])]
        draft_dict = draft_df.to_dict(orient=orient)
        return jsonify(draft_dict)




if __name__ == "__main__":
    app.run(debug=True)
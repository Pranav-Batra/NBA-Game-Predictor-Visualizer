from flask import Flask, url_for, request, render_template, redirect
from datetime import datetime
from datetime import date
import temp
import pandas as pd
from nba_api.stats.static import teams


app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        date = request.form['date']
        date = datetime.strptime(date, '%Y-%m-%d')
        time_delta = (date - datetime.today()).days
        return redirect(url_for('display_games', time_delta = time_delta))
    return render_template('dates.html')

@app.route('/games', methods = ['GET', 'POST'])
def display_games():
    time_delta = request.args.get('time_delta', None)
    games = temp.get_nba_games_for_today(int(time_delta) + 1)
    home_teams = []
    away_teams = []
    dates = []
    for home in games['HOME_TEAM_ID']:
        home_teams.append(teams.find_team_name_by_id(home)['abbreviation'])
    for away in games['VISITOR_TEAM_ID']:
        away_teams.append(teams.find_team_name_by_id(away)['abbreviation'])
    for date_str in games['GAME_DATE_EST']:
        date_str = date_str.split('T')[0]
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').strftime('%b %d, %Y')
        dates.append(date_obj)
    data = {'Date': dates, 'Home Team': home_teams, 'Away Team': away_teams}
    clean_df = pd.DataFrame(data).set_index('Date')
    return render_template('picked_date.html', tables = [clean_df.to_html(classes = 'data')], titles = clean_df.columns.values)


# will get methods
@app.route('/prediction', methods = ['GET'])
def predict():
    pass

    
if __name__ == '__main__':
    app.run(port = 8000, debug = True)

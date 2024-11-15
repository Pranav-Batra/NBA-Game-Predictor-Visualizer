import datetime
import pandas as pd
from nba_api.stats.endpoints import scoreboardv2

def get_nba_games_for_today(days_away: int):
    """Gets a list of NBA games for today."""

    chosen_day = datetime.date.today() + datetime.timedelta(days_away)
    games = scoreboardv2.ScoreboardV2(game_date=chosen_day.strftime("%m/%d/%Y"), league_id='00').get_data_frames()[0]
    return games



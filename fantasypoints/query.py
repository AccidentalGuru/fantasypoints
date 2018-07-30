import nfldb
from collections import deque, defaultdict
from nfldb import PlayPlayer

db = nfldb.connect()

def query(season_type=None, season_year=None, week=None, position=None, player_name=None, team=None):
    q = nfldb.Query(db)
    q.game()
    if season_type:
        q.game(season_type=season_type)
    if season_year:
        q.game(season_year=season_year)
    if week:
        q.game(week=week)
    if position:
        q.player(position=position)
    if player_name:
        q.player(full_name=player_name)
    if team:
        q.game(team=team)
    return q


def all_play_players(season_type=None, season_year=None, week=None, position=None, player_name=None, team=None):
    pps = defaultdict(deque)
    q = query(season_type=season_type, season_year=season_year, week=week, position=position, player_name=player_name, team=team)
    for pp in q.as_play_players():
        pps[pp.player_id].append(pp)
    return pps

def agg_play_players(season_type=None, season_year=None, week=None, position=None, player_name=None, team=None):
    pps = defaultdict(PlayPlayer)
    q = query(season_type=season_type, season_year=season_year, week=week, position=position, player_name=player_name, team=team)
    for pp in q.as_aggregate():
        pps[pp.player_id] = pp
    return pps

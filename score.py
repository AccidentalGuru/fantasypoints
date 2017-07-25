import nfldb
from pprint import pprint

def offense(player_name, team=None, pos=None, year=None, week=None, season_type=None):
    player_scores = {}
    q = create_query(player_name, team, pos, year, week, season_type)
    for pp in q.as_aggregate():
        score = 0

        # Passing
        score += pp.passing_tds * 4.0
        score += pp.passing_yds / 25.0
        score += pp.passing_twoptm * 2.0
        score += pp.passing_int * -2.0

        # Rushing
        score += pp.rushing_tds * 6.0
        score += pp.rushing_yds / 10.0
        score += pp.rushing_twoptm * 2.0

        # Recieving
        score += pp.receiving_tds * 6.0
        score += pp.receiving_yds / 10.0
        score += pp.receiving_twoptm * 2.0

        # Misc Offense
        score += pp.kickret_tds * 6.0
        score += pp.puntret_tds * 6.0
        score += pp.fumbles_rec_tds * 6.0
        score += pp.fumbles_lost * -2.0

        player_scores[pp.player.full_name] = score

    return player_scores

def kicker(player_name, team=None, pos=None, year=None, week=None, season_type=None):
    kicker_scores = {}

    # Extra points and missed FGs
    q = create_query(player_name, team, pos, year, week, season_type)
    for pp in q.as_aggregate():
        score = 0
        score += pp.kicking_xpmade * 1.0
        score += pp.kicking_fgmissed * -1.0
        kicker_scores[pp.player.full_name] = score

    # Feild goals made
    q = create_query(player_name, team, pos, year, week, season_type)
    q.play(kicking_fgm__ge=1)
    for pp in q.as_play_players():
        if pp.player.full_name not in kicker_scores:
            kicker_scores[pp.player.full_name] = 0
        if pp.kicking_fgm_yds >= 50:
            kicker_scores[pp.player.full_name] += 5.0
        elif pp.kicking_fgm_yds >= 40:
            kicker_scores[pp.player.full_name] += 4.0
        else:
            kicker_scores[pp.player.full_name] += 3.0

    return kicker_scores

def defense(team, year=None, week=None, season_type=None):
    defense_scores = {}
    teams = []

    if type(team) is not list:
        teams.append(team)
    else:
        teams = team

    for t in teams:

        # In-game stats
        q = create_query(team=t, year=year, week=week, season_type=season_type)
        for pp in q.as_aggregate():
            score = 0
            score += pp.kickret_tds * 6.0
            score += pp.puntret_tds * 6.0
            score += pp.defense_int_tds * 6.0
            score += pp.defense_frec_tds * 6.0
            score += pp.defense_misc_tds * 6.0
            score += pp.defense_int * 2.0
            score += pp.defense_frec * 2.0
            score += pp.defense_fgblk * 2.0
            score += pp.defense_puntblk * 2.0
            score += pp.defense_xpblk * 2.0
            score += pp.defense_safe * 2.0
            score += pp.defense_sk * 1.0
            if t not in defense_scores:
                defense_scores[t] = score
            else:
                defense_scores[t] += score

        # Game score
        q = create_query(team=t, year=year, week=week, season_type=season_type)
        for g in q.as_games():
            game_score = 0
            score = 0

            if g.home_team == t:
                game_score = g.away_score
            else:
                game_score = g.home_score

            if game_score == 0:
                score += 5.0
            elif game_score <= 6:
                score += 4.0
            elif game_score <= 13:
                score += 3.0
            elif game_score <= 17:
                score += 1.0
            elif game_score <= 27:
                score += 0.0
            elif game_score <= 34:
                score += -1.0
            elif game_score <= 45:
                score += -3.0
            elif game_score >= 46:
                score += -5.0

            if t not in defense_scores:
                defense_scores[t] = score
            else:
                defense_scores[t] += score

    return defense_scores

def offense_by_game(player_name, team=None, pos=None, year=None, week=None, season_type=None):
    player_scores = {}
    num_games = 0
    original_week = week
    season = ['Preseason', 'Regular', 'Postseason']
    if season_type is not None:
        if type(season_type) is list:
            season = season_type
        else:
            season = [season_type]
    if year is None:
        year = [i for i in range(2009,2017)]
    elif type(year) is not list:
        year = [year]
    for y in year:
        for s in season:
            if week is None:
                if s == 'Regular':
                    week = [i for i in range(1,18)]
                elif s == 'Preseason' and y == 2009:
                    week = [i for i in range(1,5)]
                elif s == 'Preseason':
                    week = [i for i in range(1,4)]
                elif s == 'Postseason':
                    week = [i for i in range(1,5)]
            for w in week:
                weekly_scores = offense(player_name, team, pos, y, w, s)
                for key in weekly_scores:
                    if key not in player_scores:
                        player_scores[key] = [0] * num_games
                for key in player_scores:
                    if key in weekly_scores:
                        player_scores[key].append(weekly_scores[key])
                    else:
                        player_scores[key].append(0)
                num_games += 1
            week = original_week
    return player_scores

def create_query(player_name=None, team=None, pos=None, year=None, week=None, season_type=None):
    db = nfldb.connect()
    q = nfldb.Query(db)
    q.game()
    if season_type:
        q.game(season_type=season_type)
    if player_name:
        q.player(full_name=player_name)
    if team:
        q.game(team=team)
    if pos:
        q.player(position=pos)
    if year:
        q.game(season_year=year)
    if week:
        q.game(week=week)
    return q

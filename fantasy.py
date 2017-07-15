import nfldb

players = [
    "Matt Ryan",
    "LeSean McCoy",
    "Adrian Peterson",
    "DeAndre Hopkins",
    "Michael Crabtree",
    "Rob Gronkowski",
    "Brandon Marshall",
    "Donte Moncrief",
    "Doug Martin",
    "Kenny Brit",
    "Duke Johnson Jr.",
    "Jack Doyle",
    "Eli Manning",
    "Shane Vereen"
]
kicker = "Dustin Hopkins"
defense = "KC"
year = 2016
week = 4

def offenseScore(player):
    score = 0

    # Passing
    score += player.passing_tds * 4
    score += player.passing_yds / 25
    score += player.passing_twoptm * 2
    score += player.passing_int * -2

    # Rushing
    score += player.rushing_tds * 6
    score += player.rushing_yds / 10
    score += player.rushing_twoptm * 2

    # Recieving
    score += player.receiving_tds * 6
    score += player.receiving_yds / 10
    score += player.receiving_twoptm * 2

    # Misc Offense
    score += player.kickret_tds * 6
    score += player.puntret_tds * 6
    score += player.fumbles_rec_tds * 6
    score += player.fumbles_lost * -2

    return score

def defenseScore(player):
    score = 0

    score += player.kickret_tds * 6
    score += player.puntret_tds * 6
    score += player.defense_int_tds * 6
    score += player.defense_frec_tds * 6
    score += player.defense_misc_tds * 6
    score += player.defense_int * 2
    score += player.defense_frec * 2
    score += player.defense_fgblk * 2
    score += player.defense_puntblk * 2
    score += player.defense_xpblk * 2
    score += player.defense_safe * 2
    score += player.defense_sk * 1

    return score

def defenseGameScore(game):
    score = 0
    gameScore = 0

    if game.home_team == defense:
        gameScore = game.away_score
    else:
        gameScore = game.home_score

    if gameScore == 0:
        score = 5
    elif gameScore <= 6:
        score = 4
    elif gameScore <= 13:
        score = 3
    elif gameScore <= 17:
        score = 1
    elif gameScore <= 27:
        score = 0
    elif gameScore <= 34:
        score = -1
    elif gameScore <= 45:
        score = -3
    elif gameScore >= 46:
        score = -5

    return score



db = nfldb.connect()

for player in players:
    q = nfldb.Query(db)
    q.game(season_year=year, season_type='Regular', week=week)
    q.player(full_name=player)
    for p in q.as_aggregate():
        print player, offenseScore(p)

kicker_score = 0

q = nfldb.Query(db)
q.game(season_year=year, season_type='Regular', week=week)
q.player(full_name=kicker)
q.play(kicking_fgm_yds__ge=50)
kicker_score += len(q.as_plays()) * 5

q = nfldb.Query(db)
q.game(season_year=year, season_type='Regular', week=week)
q.player(full_name=kicker)
q.play(kicking_fgm_yds__ge=40, kicking_fgm_yds__le=49)
kicker_score += len(q.as_plays()) * 4

q = nfldb.Query(db)
q.game(season_year=year, season_type='Regular', week=week)
q.player(full_name=kicker)
q.play(kicking_fgm_yds__le=39)
kicker_score += len(q.as_plays()) * 3

q = nfldb.Query(db)
q.game(season_year=year, season_type='Regular', week=week)
q.player(full_name=player)
for p in q.as_aggregate():
    kicker_score += p.kicking_xpmade * 1
    kicker_score += p.kicking_fgmissed * -1

print kicker, kicker_score

defense_score = 0

q = nfldb.Query(db)
q.game(season_year=year, season_type='Regular', week=week)
q.game(team=defense)
for p in q.as_aggregate():
    defense_score += defenseScore(p)

q = nfldb.Query(db)
q.game(season_year=year, season_type='Regular', week=week)
q.game(team=defense)
for game in q.as_games():
    defense_score += defenseGameScore(game)

print defense, defense_score

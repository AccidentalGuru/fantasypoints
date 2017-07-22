import nfldb
import score
import matplotlib.pyplot as plt
import numpy as np

# def game_time(player_name, year, week, team=None, pos=None):
#     q = score.create_query(player_name=player_name, year=year, week=week, team=team, pos=pos)
#     games = q.as_games()
#     return(games[0].start_time if len(games) >= 1 else None)

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    ret = ret[n - 1:] / n
    ret = np.append([np.nan] * (n/2), ret)
    return ret

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

kickers = ["Dustin Hopkins", "Matt Bryant"]

# pts = score.offense(players, year=2016)
# print pts
#
# pts = score.offense("Matt Ryan", year=2016)
# print pts
#
# pts = score.kicker(kickers, year=2016)
# print 'Dustin Hopkins', pts
#
# pts = score.defense('KC', year=2016)
# print pts

p1 = 'Matt Ryan'
p2 = 'Julio Jones'
pts1 = []
pts2 = []
for year in range(2009,2017):
    for week in range(1,17):
        pts = score.offense([p1, p2], year=year, week=week, season_type='Regular')
        if p1 in pts:
            pts1.append(pts[p1])
        else:
            pts1.append(0)
        if p2 in pts:
            pts2.append(pts[p2])
        else:
            pts2.append(0)

player1, = plt.plot(pts1, 'r-', label=p1, alpha=0.3)
player2, = plt.plot(pts2, 'b-', label=p2, alpha=0.3)
sma1_label = p1 + ' SMA-16'
sma2_label = p2 + ' SMA-16'
sma1, = plt.plot(moving_average(np.array([pts1]), 16), 'y-', label=sma1_label)
sma2, = plt.plot(moving_average(np.array([pts2]), 16), 'g-', label=sma2_label)
plt.legend([player1, player2, sma1, sma2], [p1, p2, sma1_label, sma2_label])
plt.xticks([(year - 2009) * 16 for year in range(2009,2017)], [year for year in range(2009,2017)])
plt.grid()
plt.title('Fantasy Points For Regular Season Games (2009 - 2016)')
plt.show()

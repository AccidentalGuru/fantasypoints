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

# pts = score.offense('Matt Ryan', year=2016)
# print 'Matt Ryan', pts
#
# pts = score.kicker('Dustin Hopkins', year=2016)
# print 'Dustin Hopkins', pts
#
# pts = score.defense('KC', year=2016)
# print 'Cheifs', pts

pts1 = []
pts2 = []
for year in range(2009,2017):
    for week in range(1,17):
        pts = score.offense('Matt Ryan', year=year, week=week, season_type='Regular')
        pts1.append(pts)
        pts = score.offense('LeSean McCoy', year=year, week=week, season_type='Regular')
        pts2.append(pts)

player1, = plt.plot(pts1, 'r-', label='Matt Ryan', alpha=0.3)
player2, = plt.plot(pts2, 'b-', label='LeSean McCoy', alpha=0.3)
sma1, = plt.plot(moving_average(np.array([pts1]), 16), 'y-', label='Matt Ryan SMA')
sma2, = plt.plot(moving_average(np.array([pts2]), 16), 'g-', label='LeSean McCoy SMA')
plt.legend([player1, player2, sma1, sma2], ['Matt Ryan', 'LeSean McCoy', 'Matt Ryan SMA-16', 'LeSean McCoy SMA-16'])
plt.xticks([(year - 2009) * 16 for year in range(2009,2017)], [year for year in range(2009,2017)])
plt.grid()
plt.title('Fantasy Points For Regular Season Games (2009 - 2016)')
plt.show()

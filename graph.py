import score
import colorsys
import matplotlib.pyplot as plt
import numpy as np

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    ret = ret[n - 1:] / n
    ret = np.append([np.nan] * (n/2), ret)
    return ret

def generate_gradient(num_colors):
    colors = []
    for hue in range(0, num_colors):
        colors.append(colorsys.hsv_to_rgb(float(hue) / num_colors, 0.75, 1))
    return colors

def carreer_scores(players):
    scores = score.offense_by_game(players, season_type='Regular')
    colors = generate_gradient(len(players))
    color_count = 0
    for key, value in scores.iteritems():
        # plt.plot(value, color=colors[color_count], alpha=0.3)
        plt.plot(moving_average(np.array([value]), 16), color=colors[color_count], label=key)
        color_count += 1
    plt.legend()
    plt.xticks([(year - 2009) * 17 for year in range(2009,2017)], [year for year in range(2009,2017)])
    plt.grid()
    plt.title('Fantasy Points For Regular Season Games (2009 - 2016)')
    plt.show()

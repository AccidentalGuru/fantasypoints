import score
import graph

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

graph.carreer_scores(players)

# print score.offense_by_game(["Matt Ryan", "Tom Brady"], year=2016)

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

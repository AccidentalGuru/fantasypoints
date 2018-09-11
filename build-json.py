import nfldb
import json
import time
import sys

# Safe division
def safe_div(a, b):
    a = float(a)
    b = float(b)
    return a / b if b != 0 else 0


# Start timer
start_time = time.time()

# Get arguments
name = sys.argv[1]
sql_file = name + '.sql'
out_file = name + '.json'

# Connect to database
db = nfldb.connect()

# Open sql query
with open(sql_file, 'r') as file:
    sql_query = file.read()

# Run sql query
play_players = []
with nfldb.Tx(db) as cursor:
    cursor.execute(sql_query)
    for row in cursor.fetchall():
        play_players.append(row)

# Calculate replacements
qbs = [pp['fantasy_points'] / pp['games_played'] for pp in play_players if pp['position'] == 'QB']
qbs.sort(reverse=True)
rbs = [pp['fantasy_points'] / pp['games_played'] for pp in play_players if pp['position'] == 'RB']
rbs.sort(reverse=True)
wrs = [pp['fantasy_points'] / pp['games_played'] for pp in play_players if pp['position'] == 'WR']
wrs.sort(reverse=True)
tes = [pp['fantasy_points'] / pp['games_played'] for pp in play_players if pp['position'] == 'TE']
tes.sort(reverse=True)
flexes = rbs[24:] + wrs[24:] + tes[12:]
flexes.sort(reverse=True)

replacements = {
    'QB': qbs[12],
    'RB': rbs[24],
    'WR': wrs[24],
    'TE': tes[12],
    'FLEX': flexes[12]
}

# Add calculated data
for index, pp in enumerate(play_players):

    play_players[index]['points_per_play'] = safe_div(pp['fantasy_points'], pp['plays'])

    play_players[index]['passing_yards_per_attempt'] = safe_div(pp['passing_yards'], pp['passing_attempts'])

    play_players[index]['receiving_yards_per_target'] = safe_div(pp['receiving_yards'], pp['receiving_targets'])

    play_players[index]['rushing_yards_per_attempt'] = safe_div(pp['rushing_yards'], pp['rushing_attempts'])

    play_players[index]['value_over_replacement_player'] = pp['fantasy_points'] / pp['games_played'] - replacements[pp['position']]

    play_players[index]['value_over_replacement_flex'] = pp['fantasy_points'] / pp['games_played'] - replacements['FLEX']

# Save results to json file
with open(out_file, 'w') as outfile:
    json.dump(play_players, outfile)

# Print execution time
print('Retreived %s results in %s seconds' % (len(play_players), time.time() - start_time))

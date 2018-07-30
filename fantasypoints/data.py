import math
from collections import deque, defaultdict, namedtuple
from query import all_play_players, agg_play_players
from score import score
from utils import namedtuple_with_defaults, _numDigits, _formatBlock, _longestPlayerName


def _gamesPlayed(all_pps):
    games_played = defaultdict(int)
    for player_id, pps in all_pps.items():
        games = set()
        for pp in pps:
            games.add(pp.gsis_id)
        games_played[player_id] = len(games)
    return games_played

def _yards(pp, play_type=['passing', 'rushing', 'receiving']):
    if isinstance(play_type, str):
        play_type = [play_type]
    yards = 0
    if 'passing' in play_type:
        yards += pp.passing_yds
    if 'receiving' in play_type:
        yards += pp.receiving_yds
    if 'rushing' in play_type:
        yards += pp.rushing_yds
    return yards


def _attempts(pp, play_type=['passing', 'rushing', 'receiving']):
    if isinstance(play_type, str):
        play_type = [play_type]
    attempts = 0
    if 'passing' in play_type:
        attempts += pp.passing_att
    if 'receiving' in play_type:
        attempts += pp.receiving_tar
    if 'rushing' in play_type:
        attempts += pp.rushing_att
    return attempts

def _yardsPerAttempt(yards, attempts):
    return float(yards) / attempts if attempts > 0 else 0

def _touchdowns(pp):
    return pp.passing_tds + pp.receiving_tds + pp.rushing_tds + \
        pp.kickret_tds + pp.puntret_tds + pp.fumbles_rec_tds + \
        pp.defense_int_tds + pp.kicking_rec_tds + pp.defense_misc_tds


Field = namedtuple_with_defaults('Field', [
    'abbreviation',
    'percision'
], ['', 1])


class data:
    def __init__(self, rawdata, players=deque(), fields=defaultdict(Field)):
        self.raw = rawdata
        self.players = players
        self.fields = fields

    def display(self, sort_by=''):

        # Return if empty
        if len(self.raw) == 0:
            return

        # Titles
        titles = []
        for row_field in self.raw[0]._fields:
            abbreviation = self.fields[row_field].abbreviation
            titles.append(abbreviation)
        titles = ['RNK', 'PLAYER'] + titles

        # Field widths
        field_widths = [0 for i in range(len(titles))]
        field_widths[0] = max(_numDigits(len(self.raw)), len(titles[0]))
        field_widths[1] = max(_longestPlayerName(self.players), len(titles[1]))
        for i in range(len(self.raw[0])):
            field_widths[i + 2] = len(titles[i])
        for row in self.raw:
            for index, field_data in enumerate(row._asdict().items()):
                name, stat = field_data
                length = _numDigits(int(stat)) + self.fields[name].percision + 2
                field_widths[index + 2] = max(field_widths[index + 2], length)

        # Formatters
        row_formatter = ''
        title_formatter = ''
        row_formatter += _formatBlock(width=field_widths[0], alignment='>') + ' '
        title_formatter += _formatBlock(replacement='0[0]', width=field_widths[0], alignment='>') + ' '
        if len(self.raw) == len(self.players):
            row_formatter += _formatBlock(width=field_widths[1], alignment='<') + ' '
            title_formatter += _formatBlock(replacement='0[1]', width=field_widths[1]) + ' '
        for index, row_field in enumerate(self.raw[0]._fields):
            width = field_widths[index + 2]
            percision = self.fields[row_field].percision
            replacement = 'field[' + str(index) + ']'
            title_replacement = '0[' + str(index + 2) + ']'
            row_formatter += _formatBlock(replacement=replacement, width=width, percision=percision, alignment='>') + ' '
            title_formatter += _formatBlock(replacement=title_replacement, width=width, alignment='>') + ' '
        print row_formatter
        print title_formatter

        # Data
        if sort_by in self.raw[0]._fields:
            sort_index = self.raw[0]._fields.index(sort_by)
        else:
            sort_index = 0
        rank = len(self.raw)
        if len(self.raw) == len(self.players):
            for row, player in sorted(zip(self.raw, self.players), key=lambda x: x[0][sort_index]):
                print row_formatter.format(rank, player, field=row)
                rank -= 1
        else:
            for row, player in sorted(zip(self.raw, self.players), key=lambda x: x[0][sort_index]):
                print row_formatter.format(rank, field=row)
                rank -= 1
        print title_formatter.format(titles)

def players(season_type=None, season_year=None, week=None, position=None, player_name=None, team=None):
    Row = namedtuple('Row', [
        'total_points',
        'points_per_play',
        'number_of_plays',
        'touchdowns',
        'yards',
        'attempts',
        'yards_per_attempt',
        'passing_yards',
        'passing_attempts',
        'passing_yards_per_attempt',
        'receiving_yards',
        'receiving_attempts',
        'receiving_yards_per_attempt',
        'rushing_yards',
        'rushing_attempts',
        'rushing_yards_per_attempt',
        'games_played'
    ])

    fields = defaultdict(Field)
    fields['total_points'] = Field('PTS', 1)
    fields['points_per_play'] = Field('PPP', 2)
    fields['number_of_plays'] = Field('PLY', 0)
    fields['touchdowns'] = Field('TD', 0)
    fields['yards'] = Field('YDS', 0)
    fields['attempts'] = Field('ATT', 0)
    fields['yards_per_attempt'] = Field('YPA', 1)
    fields['passing_yards'] = Field('PY', 0)
    fields['passing_attempts'] = Field('PA', 0)
    fields['passing_yards_per_attempt'] = Field('PYPA', 1)
    fields['receiving_yards'] = Field('RxY', 0)
    fields['receiving_attempts'] = Field('RxA', 0)
    fields['receiving_yards_per_attempt'] = Field('RxYPA', 1)
    fields['rushing_yards'] = Field('RY', 0)
    fields['rushing_attempts'] = Field('RA', 0)
    fields['rushing_yards_per_attempt'] = Field('RYPA', 1)
    fields['games_played'] = Field('GP', 0)

    all_pps = all_play_players(season_type=season_type, season_year=season_year, week=week, position=position, player_name=player_name, team=team)

    agg_pps = agg_play_players(season_type=season_type, season_year=season_year, week=week, position=position, player_name=player_name, team=team)

    games_played = _gamesPlayed(all_pps)

    rawdata = deque()
    players = deque()

    for player_id, pp in agg_pps.items():
        total_pts = score(pp)
        num_plays = len(all_pps[player_id])
        ppp = total_pts / len(all_pps[player_id]) if num_plays > 0 else 0
        tds = _touchdowns(pp)
        yards = _yards(pp)
        atts = _attempts(pp)
        ypa = _yardsPerAttempt(yards, atts)
        pass_yards = _yards(pp, play_type='passing')
        pass_atts = _attempts(pp, play_type='passing')
        pass_ypa = _yardsPerAttempt(pass_yards, pass_atts)
        receive_yards = _yards(pp, play_type='rushing')
        receive_atts = _attempts(pp, play_type='rushing')
        receive_ypa = _yardsPerAttempt(receive_yards, receive_atts)
        rush_yards = _yards(pp, play_type='receiving')
        rush_atts = _attempts(pp, play_type='receiving')
        rush_ypa = _yardsPerAttempt(rush_yards, rush_atts)
        gp = games_played[player_id]
        row = Row(
            total_points=total_pts,
            points_per_play=ppp,
            number_of_plays=num_plays,
            touchdowns=tds,
            yards=yards,
            attempts=atts,
            yards_per_attempt=ypa,
            passing_yards=pass_yards,
            passing_attempts=pass_atts,
            passing_yards_per_attempt=pass_ypa,
            receiving_yards=receive_yards,
            receiving_attempts=receive_atts,
            receiving_yards_per_attempt=receive_ypa,
            rushing_yards=rush_yards,
            rushing_attempts=rush_atts,
            rushing_yards_per_attempt=rush_ypa,
            games_played=gp
        )
        rawdata.append(row)
        players.append(pp.player)

    return data(rawdata, players, fields)

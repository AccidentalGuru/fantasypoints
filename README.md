# fantasypoints

This library attempts to provide an easy way to get stats of NFL players and teams for fantasy football.

Fantasypoints heavily relies on the [nfldb](https://github.com/BurntSushi/nfldb) project. Due to this, this project only works with python 2.7 and requires a postgres database.

## Setup

Most of the setup for this project is [setting up nfldb](https://github.com/BurntSushi/nfldb#installation-and-dependencies). Once nfldb is setup, any python files in the repo directory can use fantasypoints through an import statment.

```python
import fantasypoints as fp
```

Eventually, this project will be on PyPI and you can install via pip or your favorite python package manager.


## Usage

Running this:

```python
import fantasypoints as fp

data = fp.players(
    season_type='Regular',
    season_year='2017',
    position='RB'
)

data.display()
```

Outputs this:

```
 10 Jordan Howard (CHI, RB)         176.5   0.57   309    9   1245   308   4.0    0   0   0.0   1120   276   4.1   125    32   3.9   16
  9 Ezekiel Elliott (DAL, RB)       177.2   0.63   281    9   1252   280   4.5    0   0   0.0    983   242   4.1   269    38   7.1   10
  8 Leonard Fournette (JAC, RB)     197.2   0.62   319   10   1372   317   4.3    0   0   0.0   1070   269   4.0   302    48   6.3   13
  7 LeSean McCoy (BUF, RB)          204.7   0.56   367    8   1587   364   4.4    0   0   0.0   1139   287   4.0   448    77   5.8   16
  6 Mark Ingram (NO, RB)            220.0   0.73   302   12   1540   301   5.1    0   0   0.0   1124   230   4.9   416    71   5.9   16
  5 Melvin Gordon (SD, RB)          230.1   0.62   369   12   1581   367   4.3    0   0   0.0   1105   284   3.9   476    83   5.7   16
  4 Alvin Kamara (NO, RB)           239.4   1.03   233   14   1554   221   7.0    0   0   0.0    728   120   6.1   826   101   8.2   16
  3 Kareem Hunt (KC, RB)            242.2   0.72   337   11   1782   335   5.3    0   0   0.0   1327   272   4.9   455    63   7.2   16
  2 Le'Veon Bell (PIT, RB)          257.4   0.60   431   11   1954   428   4.6    0   0   0.0   1291   321   4.0   663   107   6.2   15
  1 Todd Gurley (LA, RB)            319.2   0.87   365   19   2092   365   5.7    0   0   0.0   1304   278   4.7   788    87   9.1   15
RNK PLAYER                            PTS    PPP   PLY   TD    YDS   ATT   YPA   PY  PA  PYPA    RxY   RxA RxYPA    RY    RA  RYPA   GP  
```

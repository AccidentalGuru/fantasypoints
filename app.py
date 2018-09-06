from flask import Flask
from flask import render_template
import fantasypoints as fp
import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

data = fp.players(
    season_type='Regular',
    season_year='2017',
    position=['RB']
)

# Update football data
def update_data():
    global data
    data = fp.players(
        season_type='Regular',
        season_year='2017',
        position=['RB']
    )


# Create scheduler to update data
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=update_data,
    trigger=IntervalTrigger(seconds=5),
    id='printing_job',
    name='Print date and time every five seconds',
    replace_existing=True)

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# Start app
app = Flask(__name__)

# Flask routes
@app.route("/")
def scores():
    global data
    return render_template('scores.html', data=zip(data.players, data.raw))

# endorse-bot
Track endorsements posted on twitter


# setup
```shell
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
sudo apt-get install redis-server

export TWITTER_API_CONSUMER="CONSUMER_KEY"
export  TWITTER_API_SECRET="CONSUMER_SECRET"
```

# running

You will need to run flask as well as celery. And have redis installed and up and running.

The basic idea here is this:
we create a flask application, which makes an instance of endorse-bot. The bot is where the twitter stuff happens.
The bot searches for its given query, and tracks tweets that match it. It keeps a leaderboard of the hits (based on how many followers said tweet reached)

The goal is to have the bot build the leaderboard up in the background, using celery. And then flask will serve the result of the build.

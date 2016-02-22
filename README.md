# endorse-bot
Track endorsements posted on twitter

# Running Locally
```shell
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
sudo apt-get install postgresql postgresql-contrib postgresql-client

# create psql user
sudo createuser --interactive
# it will ask for a username, give it your linux account name
# make it a super user

# Set the env variables for twitter
export TWITTER_API_CONSUMER="CONSUMER_KEY"
export  TWITTER_API_SECRET="CONSUMER_SECRET"

# run the server
python run.py
```


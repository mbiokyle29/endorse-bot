from endorse import db

class Tweet(db.Model):
    
    tweet_id = db.Column(db.BigInteger, primary_key=True)
    text = db.Column(db.String)
    followers = db.Column(db.Integer)
    author = db.Column(db.String)
    added = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, id, text, followers, author):
        self.tweet_id = id
        self.text = text
        self.followers = followers
        self.author = author

    def to_json(self): 
        return {
            'tweet_id': self.tweet_id,
            'text': self.text,
            'followers': self.followers,
            'author': self.author
        }

import tweepy
import json
from flask import Flask, session, redirect, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():

    if 'access_token' not in session:
        return 'Please Login'

    auth = tweepy.OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
    token = session.get('access_token')
    auth.set_access_token(token[0], token[1])
    api = tweepy.API(auth)
    
    text = []
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        text.append(tweet.text)

    return jsonify({'tweets': text})

@app.route('/login')
def login():
    if not ('access_token' in session):
        auth = tweepy.OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
        redirect_url = auth.get_authorization_url()

        print auth.request_token
        session['request_token'] = auth.request_token

    return redirect('/', code=302)

@app.route('/logout')
def logout():
    session.clear()
    return 'Logged Out'

@app.route('/verify')
def oauth_callback():
    verifier = request.args.get('oauth_verifier', '')
    auth = tweepy.OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
    token = session.get('request_token')
    session.pop('request_token', None)
    
    auth.request_token = token
    try: 
        #TODO: Is this a good idea?
        session['access_token'] = auth.get_access_token(verifier)
    except tweepy.TweepError:
        print 'Error! Failed to get access token.'

    return redirect('/', code=302)

if __name__ == '__main__':
    app.config.from_object('config')
    app.run()

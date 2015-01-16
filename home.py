import tweepy
import json
from flask import Flask, session, redirect, request, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/login')
def login():
    if not ('oauth_token' in session and 'oauth_verifier' in session):
        auth = tweepy.OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
        return redirect(auth.get_authorization_url(), code=302)
    else:
        return render_template('/frontend/app/index.html')
        #return 'Logged In!'

@app.route('/logout')
def logout():
    session.pop('oauth_token', None)
    session.pop('oauth_verifier', None)
    return 'Logged Out'

@app.route('/loginsuccess')
def oauth_callback():
    session['oauth_token'] = request.args.get('oauth_token', '')
    session['oauth_verifier'] = request.args.get('oauth_verifier', '')
    return 'This is the OAuth Callback Handler'

if __name__ == '__main__':
    app.config.from_object('config')
    app.run()

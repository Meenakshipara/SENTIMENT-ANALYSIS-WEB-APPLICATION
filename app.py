from flask import Flask, redirect, url_for, render_template, request, session, send_file
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
	return render_template("sample1.html")

@app.route("/home")
def home1():
	return render_template("sample1.html")


@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		session.permanent = True
		user = request.form["nm"]
		session["user"] = user
		return redirect(url_for("user"))
	else:
		if "user" in session:
			return redirect(url_for("user"))
		return render_template("login.html")

@app.route("/login1", methods=["POST", "GET"])
def login1():
	if request.method == "POST":
		session.permanent = True
		user1 = request.form["op"]
		session["user"] = user1
		return redirect(url_for("user1"))
	else:
		if "user" in session:
			return redirect(url_for("user1"))
		return render_template("login2.html")


@app.route("/user")
def user():
	if "user" in session:
		user = session["user"]
		y = user
		from textblob import TextBlob
		edu = TextBlob(y)
		x=edu.sentiment.polarity
		z = x*100
		z = str(z) 
		if x<0:
			b = "Negative"
			return render_template('login1.html', value1=z, value2=b,value3=y)
		elif x == 0:
			d = "Neutral"
			return render_template('login1.html', value1=z, value2=d,value3=y)
		elif x>0 and x<=1:
			f = "Positive"
			return render_template('login1.html', value1=z, value2=f,value3=y)
	else:
		return redirect(url_for("login"))

@app.route("/user1")
def user1():
	if "user" in session:
		user = session["user"]
		import tweepy
		from textblob import TextBlob
		consumer_key = 'YPyCQ50LpE7qDJJf7pKPtbNTg'
		consumer_key_secret = '6jf3xFI6qghRbhS1NYfUE8gHG5YThZ6axqN1dcGlXtGBeLrUDR'
		access_token = '1333107433552506882-YHASmsWdHamoWKL1fP8hLtWPzeXhrR'
		access_token_secret = 'W1OoHb4eaBAMp5fCbMIunbRdfdJfqwiXJSYHQhZutj5OD'
		auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = tweepy.API(auth)
		public_tweets = api.search(user)
		p=0
		n=0
		for tweet in public_tweets:
			edu = TextBlob(tweet.text)
			x=edu.sentiment.polarity
			if x>0:
				p +=1
			else:
				n +=1
		a = ((p)/(p+n))*100
		b = 100-a
		return render_template('login3.html', value1=a, value2=b,value3=user)
	else:
		return redirect(url_for("login"))


@app.route("/back")
def logout():
	session.pop("user", None)
	return redirect(url_for("home"))


if __name__ == "__main__":
	app.debug = True
	app.run()
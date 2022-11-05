from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session,jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("layout.html")

    
@app.route("/game")
@login_required
def game():
    flash('You were successfully logged in')
    return render_template("test.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash('must provide username')
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('must provide password')
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"],request.form.get("password")):
            flash('invalid username and/or password')
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return redirect("/")

@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            flash('must provide username')
            return apology('must provide username')
        elif not request.form.get("password"):
            flash("must provide password", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("password doesnt match", 400)
            return apology('password doesnt match')
        #check if username taken
        rows = db.execute("SELECT username FROM users WHERE username = ?",request.form.get("username"))
        print(rows)
        if len(rows)==1:
            flash('username already exist')
            return apology('username already exist')
        #checks all the input now genrate hash
        hash=generate_password_hash(request.form.get("password"),method='pbkdf2:sha256',salt_length=8)

        db.execute('INSERT INTO users (username,hash) values(?,?)',request.form.get("username"),hash)
        flash('You were successfully registered in')
        return redirect("/")
    # User reached route via GET
    else:
        return redirect("/")

#fetch friend request
@app.route("/frequest",methods=["GET", "POST"]) 
@login_required
def frequest():
    if request.method== "POST":
        if not request.form.get("username"):
            flash('must provide username')
            return redirect("/frequest")
        if not request.form.get("action"):
            flash('must provide action')
            return apology("no action",400)
        #accept friend request
        if request.form.get("action")=="1":
            db.execute("UPDATE relation SET status=1 WHERE uid_ac=? AND uid_in=?",session["user_id"],request.form.get("username"))
            flash('friend added')
        #delete friend or request 
        elif request.form.get("action")=="0":
            db.execute("DELETE FROM relation WHERE  uid_ac=? AND uid_in=?",session["user_id"],request.form.get("username"))
            flash('friend delted')
        else:
            flash('must provide action')
            return apology("no action",400)
        return redirect("/frequest")
    else:
        rows=db.execute("SELECT id,username FROM users WHERE id IN (SELECT uid_in FROM relation WHERE uid_ac=? AND status=0)",session["user_id"])
        #list of names of friend request from
        if len(rows)<1:
            flash("no requests")
            return apology("no requests",400)
        return render_template("frequest.html",rows=rows)

#to show available friends on search and not self
@app.route("/searchfriend")
@login_required
def showfriend():
    rows = db.execute("SELECT username FROM users WHERE username LIKE ? and NOT id=? LIMIT 10","%"+request.args.get("q")+"%",session["user_id"])
    print(rows)
    return jsonify(rows) 

#to addfriend to relation make request not to same existing friend also
@app.route("/addfriend",methods=["GET", "POST"])
@login_required
def addfriend():
    if request.method== "POST":
        if not request.form.get("username"):
            flash('must provide username')
            return redirect("/addfriend")
        #add id not username
        rows=db.execute("SELECT id FROM users WHERE username=?",request.form.get("username"))
        if len(rows) != 1 :
            flash('invalid username')
            return redirect("/addfriend")
        if session["user_id"]==rows[0]["id"]:
            flash("self not allowed")
            return redirect("/addfriend")
        #check if not a pre-existing friend
        check=db.execute("SELECT username FROM users WHERE id in(SELECT uid_in FROM relation WHERE uid_ac=? UNION SELECT uid_ac FROM relation WHERE uid_in=?) ",session["user_id"],session["user_id"])
        for c in check:
            if request.form.get("username") in c["username"]:
                flash("already a friend or friend request has been made go check my friend or request")
                return redirect("/addfriend")

        db.execute("INSERT INTO relation (uid_in,uid_ac)VALUES(?,?);",session["user_id"],rows[0]["id"])
        flash('friend request intiated')
        return redirect("/addfriend")
    else:
        return render_template("friends.html")
@app.route("/myfriend")
@login_required
def myfriend():   
    #get all ids of friend and from that get names
    rows=db.execute("SELECT id,username FROM users WHERE id in(SELECT uid_in FROM relation WHERE uid_ac=? AND status=1 UNION SELECT uid_ac FROM relation WHERE uid_in=? AND status=1) ",session["user_id"],session["user_id"])
    if len(rows)<1:
        flash("no friends go and add some")
        return apology("no friends",400)      
    return render_template("myfriend.html",rows=rows)


    

import os
import requests

from flask import Flask,redirect,session, render_template,request,url_for,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "BcJRK3JhaVV3hJKgdTu0hg", "isbns": "0441172717"})
#print(res.json())
app = Flask(__name__)

# # Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(# TODO: enter database url here)
db = scoped_session(sessionmaker(bind=engine))

@app.route("/searchpage")
def index():
    if'username' in session:
        username = session['username']
    return render_template("index.html",username=username,login=login)

@app.route("/", methods=["POST","GET"])
def login():
    if request.method == "POST":
        #values for log in
        username = request.form.get('username')
        password = request.form.get('password')

        userdata = db.execute("SELECT * FROM users WHERE username=:username AND password=:password",{"username":username,"password":password})
        if(userdata.rowcount != 0):
            session['username'] = username
            return redirect(url_for("index"))
        else:
            return redirect(url_for("register"))
    else:
        return render_template("login.html")

@app.route("/register", methods=["POST","GET"])
def register():
    if(request.method == "POST"):
        regusername = request.form.get('regusername')
        regemail = request.form.get('regemail')
        regpassword = request.form.get('regpassword')
        confirmpassword = request.form.get('confirmpassword')

        if regpassword == confirmpassword and db.execute("SELECT username FROM users WHERE username=:username AND email=:email",{"username":regusername,"email":regemail}).rowcount == 0:
            db.execute("INSERT INTO users (username, email, password, datecreated) VALUES (:username, :email, :password, NOW())",
            {"username": regusername, "email": regemail, "password": regpassword})
            db.commit()
            return redirect(url_for("login"))
        else:
            return redirect(url_for("login"))
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop('username',None)
    return redirect(url_for('login'))

@app.route("/bookresults", methods=["POST"])
def bookresults():
    if request.method == "POST":
        booksearch = "%"+request.form.get("book")+"%"

        bookresults = db.execute("SELECT * FROM books WHERE isbn LIKE :booksearch OR title LIKE :booksearch OR author LIKE :booksearch OR year LIKE :booksearch",
        {"booksearch":booksearch})
        isResults = False;

        if "username" in session:
            username = session["username"]

        if bookresults.rowcount != 0:
            isResults = True
            return render_template("results.html",bookresults=bookresults, isResults=isResults,username=username)
        return render_template("results.html",isResults=isResults,username=username)

@app.route("/book", methods=["POST","GET"])
def book():
    if "username" in session:
        username = session["username"]

    if request.method == "POST":
        isbn = request.form.get("isbn")
        try:
            db.execute("INSERT INTO reviews(username , isbn , bookrating , comment) VALUES(:username, :isbn, :bookrating, :comment)",
            {"username":username, "isbn":isbn, "bookrating":request.form.get("rating"), "comment":request.form.get("review")})
            error = False
        except:
            error = True
        db.commit()
        bookdetails = db.execute("SELECT * FROM books WHERE isbn = :isbn",
        {"isbn":isbn})

        bookreviews = db.execute("SELECT * FROM reviews WHERE isbn = :isbn",
        {"isbn":isbn})

        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "BcJRK3JhaVV3hJKgdTu0hg", "isbns":isbn})
        data = res.json()

        averagerating = data['books'][0]['average_rating']
        noofratings = data['books'][0]['work_ratings_count']

        return render_template("book.html",username = username, bookdetails = bookdetails, bookreviews = bookreviews, averagerating = averagerating, noofratings = noofratings, error=error)

    if request.method == "GET":
        isbn =request.args.get("bookname")

        bookdetails = db.execute("SELECT * FROM books WHERE isbn = :isbn",
        {"isbn":isbn})

        bookisbn = db.execute("SELECT isbn FROM books WHERE isbn = :isbn",
        {"isbn":isbn})

        for i in bookisbn:
            bookno = i.isbn

        bookreviews = db.execute("SELECT * FROM reviews WHERE isbn = :isbn",
        {"isbn":isbn})

        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "BcJRK3JhaVV3hJKgdTu0hg", "isbns":isbn})
        data = res.json()

        averagerating = data['books'][0]['average_rating']
        noofratings = data['books'][0]['work_ratings_count']

        if bookreviews.rowcount ==0:
            info = "no reviews yet"
        return render_template("book.html",username = username, bookdetails = bookdetails, bookno = bookno, bookreviews = bookreviews, averagerating = averagerating, noofratings = noofratings)


@app.route("/api/<string:isbn>")
def api(isbn):
    bookdetail = db.execute("SELECT * FROM books WHERE isbn = :isbn",
    {"isbn":isbn})

    if bookdetail.rowcount == 0:
        return jsonify({"error": "No isbn"}),404

    #prints out the info
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "BcJRK3JhaVV3hJKgdTu0hg", "isbns":isbn})

    if 'json' in res.headers.get('Content-Type'):
        data = res.json()
    else:
        print('Response content is not in JSON format.')
        js = 'spam'

    averagerating = data['books'][0]['average_rating']
    noofratings = data['books'][0]['work_ratings_count']

    for i in bookdetail:
        return jsonify({
        "title":i.title,
        "author":i.author,
        "publication date":i.year,
        "ISBN number":i.isbn,
        "review count":noofratings,
        "average score": averagerating
        })

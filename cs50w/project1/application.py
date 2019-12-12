import os
import requests
import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
goodreads_key = os.getenv("GOODREADS_KEY")
db = scoped_session(sessionmaker(bind=engine))

################################### landing

@app.route("/", methods=["GET", "POST"])
def landing_page():
	if session.get("buddy") is None:
		return redirect(url_for("login"))
	else:	
		return redirect(url_for("dashboard"))

################################### log in

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "GET":
		return render_template("door.html", submit_page="login", submit_text="Log In", link_page="signup", link_text="New User? Sign Up!")
	
	if get_login_data(request.form) == False:
		clear_buddy()
		txt = "User name and password should be at least 3 characters! Only letters and numbers are accepted!"
		return render_template("problem.html", goto_page="login", message = txt)

	try:
		qtext = text("select id, name, pwd from users where name = :user")
		qresult = db.execute(qtext, {"user":session.get("buddy")["user"]}).fetchone()
		if qresult is None:
			clear_buddy()
			txt = "No such user!"
			return render_template("problem.html", goto_page="login", message = txt)
		if qresult.pwd != session.get("buddy")["pwd"]:
			clear_buddy()
			txt = "Incorrect password!"
			return render_template("problem.html", goto_page="login", message = txt)
		session["buddy"]["id"] = qresult.id
		return render_template("dashboard.html", user = session.get("buddy")["user"], keys = init_search_keys(), results = False)
	except Exception as exc:
		clear_buddy()
		return render_template("problem.html", goto_page="login", message = str(exc))

################################### sign up

@app.route("/signup", methods=["GET", "POST"])
def signup():
	if request.method == "GET":
		return render_template("door.html", submit_page="signup", submit_text="Sign Up", link_page="login", link_text="Returning User? Log in!")
	
	if get_login_data(request.form) == False:
		clear_buddy()
		txt = "User name and password should be at least 3 characters! Only letters and numbers are accepted!"
		return render_template("problem.html", goto_page="signup", message = txt)

	try:
		qtext = text("select name, pwd from users where name = :user")
		qresult = db.execute(qtext, {"user":session.get("buddy")["user"]}).fetchone()
		if qresult is not None:
			clear_buddy()
			txt = "User name already taken!"
			return render_template("problem.html", goto_page="signup", message = txt)
		qtext = text("insert into users (name, pwd) values (:user, :pwd)")
		db.execute(qtext, {"user":session.get("buddy")["user"], "pwd":session.get("buddy")["pwd"]})
		db.commit()
		clear_buddy()
		return redirect(url_for("login"))
	except Exception as exc:
		clear_buddy()
		return render_template("problem.html", goto_page="signup", message = str(exc))

################################### log out

@app.route("/logout", methods=["GET", "POST"])
def logout():
	clear_buddy()
	return redirect(url_for("login"))

################################### search keys for books and result list

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
	if session.get("buddy") is None:
		clear_buddy()
		return redirect(url_for("login"))	

	if session.get("search_keys") is None:
		session["search_keys"] = init_search_keys()
		session["search_results"] = False	

	if session.get("search_results") is None:
		session["search_results"] = False
		set_mess(False)

	return render_template("dashboard.html", keys = session.get("search_keys"), results = session.get("search_results"))	

################################### do book search using search keys

@app.route("/search", methods=["POST"])
def search():
	if session.get("buddy") is None:
		clear_buddy()
		return redirect(url_for("login"))	

	if get_search_keys(request.form) == False:
		txt = "Keys should be empty or at least 3 characters; ISBN should be a number; please use at least a key!"
		return render_template("problem.html", goto_page="dashboard", message = txt)

	try:
		qtext = text(get_query_text())
		qpars = {}
		qpars["isbn"] = session.get('search_keys')['isbn']
		qpars["author"] = session.get('search_keys')['author']
		qpars["title"] = session.get('search_keys')['title']
		rows = db.execute(qtext, qpars).fetchall()
		if len(rows) < 1:
			session["search_results"] = False	
			set_mess(True)
			return render_template("dashboard.html", user = session.get("buddy")["user"], keys = session.get("search_keys"), results = False)
		else:
			session["search_results"] = rows
			set_mess(False)
			return render_template("dashboard.html", user = session.get("buddy")["user"], keys = session.get("search_keys"), results = rows)
	except Exception as exc:
		session["search_results"] = False
		set_mess(False)			
		return render_template("problem.html", goto_page="dashboard", message = str(exc))
	
################################### display detail page about a book

@app.route("/bookpage/<book_id>", methods=["GET", "POST"])
def bookpage(book_id):
	if session.get("buddy") is None:
		clear_buddy()
		return redirect(url_for("login"))

	nid = get_nid(book_id)
	if nid < 1:
		set_mess(False)
		txt = "Invalid book identifier!"
		return render_template("problem.html", goto_page="dashboard", message = txt)

	try:
		qtext = text("select id, isbn, author, title, year, revtot, revcount from books where id = :book_id;")
		details = db.execute(qtext, {"book_id":nid}).fetchone()
		if details is None:
			set_mess(False)
			txt = "The book is missing from the database!"
			return render_template("problem.html", goto_page="dashboard", message = txt)

		ntot = details.revtot
		ncount = details.revcount
		isbn = details.isbn

		dets = {}
		oklr = True if ncount > 0 else False
		ntot = ntot / ncount if ncount > 0 else 0.0
		ntot = round(ntot, 2)

		if oklr:
			dets["lcount"] = ncount
			dets["ltot"] = ntot

		qtext = text("select iduser, rating, comment, stamp from reviews where idbook = :book_id order by stamp desc limit 50;")
		reviews = db.execute(qtext, {"book_id":nid}).fetchall()

		oklist = True
		oknew = True
		if len(reviews) < 1:
			oklist = False
		else:
			nuser = session.get('buddy')['id']
			for elem in reviews:
				if elem.iduser == nuser:
					oknew = False
					break

		okgr = False
		res = requests.get("https://www.goodreads.com/book/review_counts.json", {"key":goodreads_key, "isbns":isbn})
		if res.status_code == 200:
			dres = res.json()
			lres = dres.get("books")
			if lres is not None:
				r1 = lres[0].get("average_rating")
				r2 = lres[0].get("work_ratings_count")
				if r1 is not None and r2 is not None:
					okgr = True
					dets["gtot"] = r1
					dets["gcount"] = r2

		return render_template("detail.html", book = details, bookex = dets,  revs = reviews, oklist = oklist, oknew = oknew, okgr = okgr, oklr = oklr)

	except Exception as exc:
		set_mess(False)			
		return render_template("problem.html", goto_page="dashboard", message = str(exc))

################################### insert review

@app.route("/addreview/<book_id>", methods=["POST"])
def addreview(book_id):
	if session.get("buddy") is None:
		clear_buddy()
		return redirect(url_for("login"))
		
	nid = get_nid(book_id)
	if nid < 1:
		txt = "Invalid book identifier!"
		return render_template("problem.html", goto_page="dashboard", message = txt)

	if get_review(request.form) == False:
		txt = "The Rating should be between 1 and 5; the Comment length should be between 2 and 1000 characters!"
		return render_template("problem.html", goto_page="dashboard", message = txt)

	try:
		nuser = session.get("buddy")["id"]
		new_rating = session.get("review")["rating"]

		qtext = text("select rating, comment, stamp from reviews where idbook = :book_id and iduser = :user_id;")
		row = db.execute(qtext, {"book_id":nid, "user_id":nuser}).fetchone()
		if row is not None:
			txt = "Already added Rating: " + str(row.rating) + " Comment: " + row.comment + " at: " + str(row.stamp)
			return render_template("problem.html", goto_page="dashboard", message = txt)

		qtext1 = "insert into reviews (iduser, idbook, rating, comment) values (:user_id, :book_id, :rating, :comment)"
		db.execute(qtext1, {"user_id":nuser, "book_id":nid, "rating":new_rating, "comment":session.get("review")["comment"]})

		qtext2 = text("update books set revtot = revtot + :new_rating, revcount = revcount + 1 where id = :book_id;")
		db.execute(qtext2, {"new_rating":new_rating, "book_id":nid})
		# do transaction: insert + update
		db.commit()
		return redirect(url_for("dashboard"))

	except Exception as exc:
		set_mess(False)			
		return render_template("problem.html", goto_page="dashboard", message = str(exc))

###################################

@app.route("/api/<isbn>", methods=["GET"])
def api_isbn(isbn):
	code = isbn.strip()
	if len(code) < 10 or len(code) > 20:
		return jsonify({"error":"ISBN code too short or too long!"}), 422
	
	qtext = text("select title, author, year, isbn, revtot, revcount from books where isbn = :code")
	row = db.execute(qtext, {"code":code}).fetchone()
	if row is None:
		return jsonify({"error":"ISBN code not found in our database!"}), 404

	nrating = row.revtot
	ncount = row.revcount
	nrating = nrating/ncount if ncount > 0 else 0.0
	return jsonify({"title":row.title, "author":row.author, "year":row.year, "isbn":row.isbn, "review_count":ncount, "average_score":nrating})

################################### helper functions
###################################
################################### validating login

def get_login_data(obj_form):
	user = obj_form.get("user")
	user = user.strip()
	pwd = obj_form.get("pwd")
	pwd = pwd.strip()

	if len(user)<=50 and len(pwd)<=50 and len(user)>=3 and len(pwd)>=3 and user.isalnum() and pwd.isalnum():
		session["buddy"] = {"user":user, "pwd":pwd, "id":0}
		return True
	else:
		return False
		
##################### validating search keys

def get_search_keys(obj_form):
	isbn = obj_form.get("isbn")
	isbn = isbn.strip()
	title = obj_form.get("title")
	title = title.strip()
	author = obj_form.get("author")
	author = author.strip()

	okay = True
	if len(isbn)<1 and len(title)<1 and len(author)<1:
		okay = False
	if len(isbn)>20 or len(title)>100 or len(author)>100:
		okay = False
	if len(isbn)>0 and len(isbn)<3:
		okay = False
	if len(title)>0 and len(title)<3:
		okay = False
	if len(author)>0 and len(author)<3:
		okay = False

	session["search_keys"] = {"isbn":isbn ,"title":title , "author":author, "results":okay}
	return okay	
	
###################################

def get_review(obj_form):	
	rating = obj_form.get("rating")
	if len(rating) > 10:
		return False
	rating = rating.strip()

	nrating = 0
	if len(rating) > 0:
		if len(rating) > 1 or rating.isdigit() == False:
			return False
		nrating = int(rating)
		if nrating < 1 or nrating > 5:
			return False

	comment = obj_form.get("comment")
	comment = comment.strip()
	if len(comment) < 2 or len(comment) > 1000:
		return False
	session["review"] = {"rating":nrating, "comment":comment}
	return True

###################################

def init_search_keys():
	session["search_keys"] = {"isbn":"", "title":"", "author":"", "results":False }

###################################

def clear_buddy():
	if session.get("buddy") is not None:
		del session["buddy"]
	if session.get("search_keys") is not None:
		del session["search_keys"]
	if session.get("search_results") is not None:
		del session["search_results"]

###################################

def set_mess(status):
	if session.get("search_keys") is None:
		session["search_keys"] = init_search_keys()
	else:
		session["search_keys"]["results"] = status

###################################

def get_query_text():
	qtext = "select id, isbn, title, author, year from books where"
	counter = 0
	if len(session.get('search_keys')['isbn']) > 0:
		qtext += " position(:isbn in isbn)>0" 
		counter += 1
	if len(session.get('search_keys')['author']) > 0:
		if counter > 0:
			qtext += " and "
		qtext += " position(:author in author)>0" 
		counter += 1
	if len(session.get('search_keys')['title']) > 0:
		if counter > 0:
			qtext += " and "
		qtext += " position(:title in title)>0" 
		counter += 1
	qtext += " order by year desc limit 50;"
	return qtext

################################### validating row ID (PostGres sequence on 32 bits)

def get_nid(string_id):
	if string_id is None or len(string_id)>20:
		return 0
	string_id = string_id.strip()
	if len(string_id)>9 or string_id.isdigit() == False:
		return 0
	return int(string_id)

###################################


import os
import string

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

depts = db.execute("SELECT * FROM departments")

def check_session():
    if 'user_id' not in session:
        return redirect("/login.html")
    else:
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        session['username'] = username[0]['username']

@app.before_request
def before_request():
    check_session()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("/index.html")


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """create a job post"""

    if request.method == 'POST':
        jobtitle = request.form.get("jobtitle")
        jobdesc = request.form.get("jobdesc")
        department = request.form.get("department")
        status = request.form.get("status")

        if not jobtitle:
            return apology("Invalid Job Title", 400)
        elif not jobdesc:
            return apology("Please input a job description", 400)
        elif not department:
            return apology("Please select a department", 400)

        db.execute("INSERT INTO jobs (title, description, dept_id) VALUES(?, ?, ?)", jobtitle, jobdesc, department)

        return redirect("/")

    return render_template("/create.html", depts=depts)


@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    """update job post"""

    if request.args:
        job_id = request.args['job-edit']

        job = db.execute("SELECT * FROM jobs WHERE id=?", job_id)

    if request.method == 'POST':
        id = request.form.get("job_id")
        title = request.form.get("job_title")
        desc = request.form.get("job_desc")
        status = request.form.get("status")
        dept = request.form.get("department")

        db.execute("UPDATE jobs SET title = ?, description = ?, status = ?, dept_id = ? WHERE id = ?", title, desc, status, dept, id)

        return redirect("/")

    return render_template("/update.html", job=job, depts=depts)


@app.route("/job")
def job():
    if request.args:
        job_id = request.args['job-read-more']

        job = db.execute("SELECT * FROM jobs WHERE id=?", job_id)
    else:
        return apology("Invalid URL", 404)

    return render_template("/job.html", job=job, depts=depts)


@app.route("/careers")
def careers():
    """Show all job posts"""
    # filter job by dept

    if request.args:
        filter_dept_id = request.args.get('dept_id')

        if filter_dept_id == 'all':
            jobs = db.execute("SELECT * FROM jobs")
            # filteredDept = depts
        else:
            jobs = db.execute("SELECT * FROM jobs WHERE dept_id = ?", (filter_dept_id,))
            # filteredDept = db.execute("SELECT name FROM departments WHERE id = ?", (filter_dept_id,))
    else:
        jobs = db.execute("SELECT * FROM jobs")


    # ajax
    if request.headers.get("X-Requested-With") == 'XMLHttpRequest':
        return jsonify(jobs=[dict(row) for row in jobs], depts=depts)
        # return jobs

    # for content update
    job_edit_id = request.form.get('job-edit')

    for row in jobs:
        if job_edit_id == row['id']:
            return render_template("/update.html")

    return render_template("/careers.html", results=jobs, depts=depts)


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    """delete job post"""

    if request.method == 'POST':
        id = request.form.get("job-id")

        db.execute("DELETE FROM jobs WHERE id = ?", id)

        return redirect("/")

    return render_template("/index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


def validation_username(input):
    special_chars_user = set("@.")
    error_count = 0

    # allow only 8-64 chars
    if len(input) >= 8 and len(input) <= 64:
        if input.isalnum():
            return error_count
        else:
            for c in input:
                # if has punctuations
                if c not in special_chars_user and not c.isalnum():
                    error_count += 1
                    break

            if error_count > 0:
                return error_count
            else:
                return error_count
    else:
        error_count += 1
        return error_count

def validation_pw(input):
    error_count = 0
    special_chars_pw = set("!@#$%^&*.")

    # allow only 8-64 chars
    if len(input) >= 8 and len(input) <= 64:
        if input.isalnum():
            return error_count
        else:
            for c in input:
                # if has punctuations
                if c not in special_chars_pw and not c.isalnum():
                    error_count += 1
                    break

            if error_count > 0:
                return error_count
            else:
                return error_count
    else:
        error_count += 1
        return error_count


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == 'POST':
        regcode = request.form.get("regcode")
        user = request.form.get("username")
        pw = request.form.get("password")
        pw2 = request.form.get("confirmation")

        usernames = db.execute("SELECT username FROM users")

        is_valid_user = validation_username(user)
        is_valid_pw = validation_pw(pw)

        # if is_valid_user > 0:
        #     return apology("Username must be at least 8 alphanumeric characters long, no spaces, and may only contain . and/or @", 400)

        if regcode != '':
            return apology("Invalid Registration Code", 400)
        elif is_valid_user > 0:
            return apology("Invalid Username", 400)
        elif is_valid_pw > 0:
            return apology("Invalid Password", 400)
        elif pw != pw2:
            return apology("Password did not match", 400)

        # if users table is not empty
        if usernames:
            for username in usernames:
                # check if user already exists
                if user == username['username']:
                    return apology("user already exists", 400)

        # insert to db
        pwhash = generate_password_hash(pw)
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", user, pwhash)

        return render_template("/login.html")

    return render_template("/register.html")


@app.route("/apply")
def apply():
    return apology("TODO")

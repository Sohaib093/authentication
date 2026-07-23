from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/")
def home():
    return redirect("/login")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_post():

    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users(username,password,role) VALUES(?,?,?)",
            (username, password, role)
        )
        conn.commit()
    except:
        return "Username already exists"

    conn.close()

    return redirect("/login")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():

    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT username, role FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cur.fetchone()

    conn.close()

    if user is None:
        return "Invalid Username or Password"

    username = user[0]
    role = user[1]

    if role == "admin":
        return render_template("admin.html",
                               username=username,
                               role=role)

    else:
        return render_template("user.html",
                               username=username,
                               role=role)


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/user")
def user():
    return render_template("user.html")

if __name__ == "__main__":
    app.run(debug=True)
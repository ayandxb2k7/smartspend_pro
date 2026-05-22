from flask import Flask, render_template, request, redirect, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import pandas as pd
from model import categorize_expense, predict_expense

app = Flask(__name__)
app.secret_key = "secret123"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
                )""")

    c.execute("""CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT,
                amount REAL,
                category TEXT,
                date TEXT
                )""")

    c.execute("""CREATE TABLE IF NOT EXISTS goals (
                user_id INTEGER,
                monthly_goal REAL
                )""")

    conn.commit()
    conn.close()

init_db()

# ---------------- LOGIN ----------------

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return redirect("/login")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect("database.db")
        conn.execute("INSERT INTO users (username,password) VALUES (?,?)",
                     (username,password))
        conn.commit()
        conn.close()
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        user = conn.execute("SELECT id,password FROM users WHERE username=?",
                            (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            login_user(User(user[0]))
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    conn = sqlite3.connect("database.db")
    df = pd.read_sql_query(
        f"SELECT * FROM expenses WHERE user_id={current_user.id}", conn)

    total = df["amount"].sum() if not df.empty else 0
    prediction = predict_expense(df)

    goal_data = conn.execute(
        "SELECT monthly_goal FROM goals WHERE user_id=?",
        (current_user.id,)
    ).fetchone()

    goal = goal_data[0] if goal_data else 0
    progress = (total/goal)*100 if goal else 0

    conn.close()

    return render_template("dashboard.html",
                           total=total,
                           prediction=prediction,
                           goal=goal,
                           progress=progress)

@app.route("/add", methods=["POST"])
@login_required
def add():
    title = request.form["title"]
    amount = float(request.form["amount"])
    date = request.form["date"]
    category = categorize_expense(title)

    conn = sqlite3.connect("database.db")
    conn.execute("""INSERT INTO expenses
                 (user_id,title,amount,category,date)
                 VALUES (?,?,?,?,?)""",
                 (current_user.id,title,amount,category,date))
    conn.commit()
    conn.close()
    return redirect("/dashboard")

@app.route("/set_goal", methods=["POST"])
@login_required
def set_goal():
    goal = float(request.form["goal"])
    conn = sqlite3.connect("database.db")
    conn.execute("DELETE FROM goals WHERE user_id=?",
                 (current_user.id,))
    conn.execute("INSERT INTO goals VALUES (?,?)",
                 (current_user.id,goal))
    conn.commit()
    conn.close()
    return redirect("/dashboard")

@app.route("/export")
@login_required
def export():
    conn = sqlite3.connect("database.db")
    df = pd.read_sql_query(
        f"SELECT * FROM expenses WHERE user_id={current_user.id}", conn)
    df.to_csv("expenses.csv", index=False)
    conn.close()
    return send_file("expenses.csv", as_attachment=True)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
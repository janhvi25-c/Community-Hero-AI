from flask import Flask, render_template, request, redirect, send_from_directory, session
import sqlite3
import os
from detector import analyze_report 


app = Flask(__name__)
app.secret_key = "communityhero123"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("communityhero.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        connection.close()

        if user:
         session["user"] = user[2]   # stores user's email
         return redirect("/dashboard")
        else:
            return "Invalid Email or Password"

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("communityhero.db")
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )

        connection.commit()
        connection.close()

        return redirect("/login")

    return render_template("signup.html")

@app.route("/report")
def report():
    return render_template("report.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
     return redirect("/login")
    connection = sqlite3.connect("communityhero.db")
    cursor = connection.cursor()

    search = request.args.get("search")
    filter = request.args.get("filter")

    query = "SELECT * FROM reports WHERE user_email=?"
    params = [session["user"]]

    if search:
        query += " AND (title LIKE ? OR location LIKE ? OR ai_result LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])

    if filter == "Submitted":
        query += " AND status='Submitted'"
    elif filter == "Resolved":
        query += " AND status='Resolved'"
    elif filter == "Highest":
        query += " AND ai_result LIKE '%Highest%'"
    elif filter == "High":
        query += " AND ai_result LIKE '%High%'"
    elif filter == "Medium":
        query += " AND ai_result LIKE '%Medium%'"
    elif filter == "Low":
        query += " AND ai_result LIKE '%Low%'"

    cursor.execute(query, params)


    reports = cursor.fetchall()
    print(reports)


    total_reports = len(reports)
    submitted = sum(1 for report in reports if report[7] == "Submitted")
    resolved = sum(1 for report in reports if report[7] == "Resolved")
    highest_priority = sum(
    1 for report in reports
    if "Priority: Highest" in report[6]
)

    high = sum(1 for report in reports if "Priority: High" in report[6])
    medium = sum(1 for report in reports if "Priority: Medium" in report[6])
    low = sum(1 for report in reports if "Priority: Low" in report[6])

    connection.close()

    return render_template(
    "dashboard.html",
    reports=reports,
    total_reports=total_reports,
    submitted=submitted,
    resolved=resolved,
    highest_priority=highest_priority,
    search=search,
    filter=filter,
    high=high,
    medium=medium,
    low=low
)

@app.route("/upload", methods=["POST"])

def upload():
    title = request.form["title"]
    location = request.form["location"]
    description = request.form["description"]
    image = request.files["image"]
    user_email = session["user"]

    filename = image.filename
    image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    ai_result = analyze_report(title, location, description)
    connection = sqlite3.connect("communityhero.db")
    cursor = connection.cursor()

    cursor.execute(
    """
    INSERT INTO reports
    (user_email, title, location, description, image, ai_result, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (user_email, title, location, description, filename, ai_result, "Submitted")
)

    connection.commit()
    connection.close()

    return redirect("/dashboard")
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
@app.route("/resolve/<int:id>", methods=["POST"])
def resolve(id):
    connection = sqlite3.connect("communityhero.db")
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE reports SET status='Resolved' WHERE id=?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect("/dashboard")
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    connection = sqlite3.connect("communityhero.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM reports WHERE id=?", (id,))

    connection.commit()
    connection.close()

    return redirect("/dashboard")
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
if __name__ == "__main__":
    app.run(debug=True)
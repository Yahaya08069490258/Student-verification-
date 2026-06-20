from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Create database
def init_db():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matric TEXT UNIQUE,
        name TEXT,
        department TEXT,
        level INTEGER,
        cgpa REAL,
        email TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# Home Page
@app.route('/')
def home():
    return """
    <h2>Student Verification System</h2>

    <form action="/verify" method="post">
        <label>Matric Number</label><br>
        <input type="text" name="matric"><br><br>

        <label>Full Name</label><br>
        <input type="text" name="name"><br><br>

        <button type="submit">Verify Student</button>
    </form>

    <br><hr>
    <a href="/admin">Admin Panel</a>
    """

# Verify Student
@app.route('/verify', methods=['POST'])
def verify():

    matric = request.form['matric']
    name = request.form['name']

    conn = sqlite3.connect("students.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT matric,name,department,level,cgpa,email FROM students WHERE matric=?",
        (matric,)
    )

    student = cur.fetchone()
    conn.close()

    if student and student[1].lower() == name.lower():

        return f"""
        <h2 style='color:green;'>VERIFIED ✅</h2>

        <b>Name:</b> {student[1]}<br>
        <b>Matric:</b> {student[0]}<br>
        <b>Department:</b> {student[2]}<br>
        <b>Level:</b> {student[3]}<br>
        <b>CGPA:</b> {student[4]}<br>
        <b>Email:</b> {student[5]}<br><br>

        <a href="/">Back</a>
        """

    return """
    <h2 style='color:red;'>NOT FOUND ❌</h2>
    <a href="/">Back</a>
    """

# Admin Panel
@app.route('/admin')
def admin():

    return """
    <h2>Add Student</h2>

    <form action="/add_student" method="post">

        Matric Number:<br>
        <input type="text" name="matric"><br><br>

        Full Name:<br>
        <input type="text" name="name"><br><br>

        Department:<br>
        <input type="text" name="department"><br><br>

        Level:<br>
        <input type="number" name="level"><br><br>

        CGPA:<br>
        <input type="text" name="cgpa"><br><br>

        Email:<br>
        <input type="email" name="email"><br><br>

        <button type="submit">Add Student</button>

    </form>

    <br>
    <a href="/">Home</a>
    """

# Save Student
@app.route('/add_student', methods=['POST'])
def add_student():

    matric = request.form['matric']
    name = request.form['name']
    department = request.form['department']
    level = request.form['level']
    cgpa = request.form['cgpa']
    email = request.form['email']

    try:
        conn = sqlite3.connect("students.db")
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO students
        (matric,name,department,level,cgpa,email)
        VALUES (?,?,?,?,?,?)
        """,
        (matric,name,department,level,cgpa,email))

        conn.commit()
        conn.close()

        return """
        <h2 style='color:green;'>Student Added Successfully ✅</h2>
        <a href='/admin'>Add Another</a>
        """

    except:
        return """
        <h2 style='color:red;'>Matric Number Already Exists ❌</h2>
        <a href='/admin'>Back</a>
        """

if __name__ == '__main__':
    app.run(debug=True) 

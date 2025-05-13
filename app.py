from flask import Flask, request, render_template, redirect, url_for, flash
import pyodbc

app = Flask(__name__)
app.secret_key = 'super-secret-key'

# Full Azure SQL connection string
conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=sql-server-cs188-washington-xavier.database.windows.net;"
    "DATABASE=cs188-washington-xavier;"
    "UID=cs188admin;"
    "PWD=CS188-spring-2025;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

def get_db_connection():
    return pyodbc.connect(conn_str)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return f"Welcome, {user.display_name}!"
        else:
            flash("Invalid username or password.")
            return redirect(url_for('home'))

    except Exception as e:
        return f"Error connecting to DB: {e}"

if __name__ == '__main__':
    app.run(debug=True)

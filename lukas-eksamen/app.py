from flask import Flask, render_template, redirect, session, request
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from forms import RegisterForm

app = Flask(__name__)
# importert fra presentasjon
app.secret_key = "hemmelig-nok"

# funksjon som oppretter en tilkobling til databasen 'login' med brukeren 'lukas'
def get_conn():
    return mysql.connector.connect(
        host="localhost",
        user="lukas",
        password="messi123",
        database="login"
    )

@app.route('/')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
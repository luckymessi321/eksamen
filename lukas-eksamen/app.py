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

# rute med kode som kjører KUN når register.html henter data fra app.py (GET), eller sender data til app.py (POST)
@app.route("/register", methods=["GET", "POST"])
def register():
    # oppretter et nytt objekt 'form' av 'RegisterForm' klassen importert fra forms.py
    form = RegisterForm()
    # kode som KUN kjører når brukeren sender inn data (submit)
    if form.validate_on_submit():
        # definerer brukernavn og passord i variabler
        username = form.username.data
        password = form.password.data
        password_hash = generate_password_hash(password)

        # oppretter tilkobling til MySQL databasen og lagrer tilkoblingen som en variabel 'conn'. dette lar meg bruke methods som .commit()
        conn = get_conn()
        # oppretter et cursor objekt 'cur' koblet til databasen. dette objektet kan kjøre MySQL kode på serveren.
        cur = conn.cursor()

         # sjekker om det allerede finnes en bruker med samme navn som den registrerte
        cur.execute('SELECT username FROM users where username=%s', (username,))

        user = cur.fetchone()
        cur.close()
        conn.close()
        # gir spilleren en feilmelding om bruker med samme navn finnes
        if user:
            form.username.errors.append('This username is already taken. Please choose a new username')
        else:
            conn = get_conn()
            cur = conn.cursor()
            # kjører MySQL kode på serveren som lagrer brukernavn og passord hentet fra '/register' ruten i databasen.
            cur.execute(
                "INSERT INTO users (username, password, score) VALUES (%s, %s, %s)",
                (username, password_hash, 0)
            )
            # lagrer endringene gjort i cur.execute og lukker tilkoblingen til databasen
            conn.commit()
            cur.close()
            conn.close()
            form.password.errors.append(f'Successfully registered user {username}')

    return render_template("register.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
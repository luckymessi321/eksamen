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

# rute med kode som kjører KUN når login.html henter data fra app.py (GET), eller sender data til app.py (POST)
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        conn = get_conn()
        cur = conn.cursor()
        # kjører MySQL kode på serveren som henter brukernavnet, scoren og passordet til brukeren spilleren logget inn med
        cur.execute(
            "SELECT username, score, password FROM users WHERE username=%s",
            (username,)
        )
        # lagrer brukernavn og score som variablen 'user'
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        # kode som KUN kjører om brukeren eksisterer
        if user:
            # lagrer passord fra cur.execute som en variabel 'password_db'
            password_db = user[2]
            # sjekker om passordet stemmer med passord-hashen i databasen
            if check_password_hash(password_db, password):
                # lagrer brukernavn og score i session-data
                session['username'] = user[0]
                session['score'] = user[1]
                form.password.errors.append(f'Successfully logged in as {username}')
            # returnerer feilmelding om passord ikke stemmer med lagret passord
            else:
                form.username.errors.append('Invalid password')
        # returnerer feilmelding om brukernavn ikke finnes
        else:
            form.username.errors.append("User doesn't exist")

    return render_template("login.html", form=form)

# oppretter ruten '/save_score' slik at app.py kan sende data til 'script.js' og motta data fra 'script.js'
@app.route('/save_score', methods=["POST"]) # methods=["POST"] får koden til å KUN aktivere når ruten får en POST-request (mottar data)
# funksjon som henter score fra 'script.js' og lagrer det i MySQL databasen
def save_score():
    # henter brukernavnet og highscore til brukeren lagret i '/login' ruten (linje 77 og 78)
    username = session.get('username')
    highscore = session.get('score', 0)
    #  utfører en GET-request til script.js, leser resultatet som en JSON fil, konverterer resultatet til python format (.py), og lagrer resultatet som variablen 'data'. dette lar dataen bli brukt med metoder som .get(). 
    data = request.get_json()
    # lagrer verdien av nøkkelen 'score' i GET-requesten definert over som variablen score
    score = data.get('score')

    if int(score) > int(highscore):
        conn = get_conn()
        cur = conn.cursor()
        # kjører MySQL kode på serveren som oppdaterer 'score' verdien under den innloggede til å være scoren hentet fra script.js 
        cur.execute('UPDATE users SET score = %s WHERE username = %s', (score, username))
        conn.commit()
        cur.close()
        conn.close()

        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT score FROM users WHERE username = %s', (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session['score'] = user[0]

        return{'status': 'success'}
    else:
        # sender ordboken 'status : success' til script.js
        return{'status': 'score too low'}

if __name__ == "__main__":
    app.run(debug=True)
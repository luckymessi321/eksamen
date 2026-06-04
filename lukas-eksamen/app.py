from flask import Flask, render_template, redirect, session, request
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from forms import RegisterForm, LoginForm, LogoutForm, EditForm, DeleteForm


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
    #sjekker om spilleren er logget inn
    if session.get('username'):
        # sender brukeren til spillet
        return render_template('index.html', highscore=session.get('score'), username = session.get('username'))
    else:
        # sender brukeren til en avlogget versjon av spillet
        return render_template('index2.html') 

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

@app.route("/manage", methods=["GET", "POST"])
def manage():
    username = session.get('username')
    form = LogoutForm()
    form2 = EditForm()
    form3 = DeleteForm()

    # Logout form
    if form.submit.data and form.validate_on_submit():
        if session.get('username'):
            # sletter session dataen til brukeren
            session.pop('username')
            session.pop('score')
        redirect('/')

    # Edit User form
    if form2.submitEdit.data and form2.validate_on_submit():
        username1 = form2.username1.data
        password1 = form2.password1.data
        editUsername = form2.editUsername.data
        editPassword = form2.editPassword.data
        password_hash = generate_password_hash(editPassword)
        
        # sjekker om brukernavnet spilleren fylte inn stemmer med brukernavnet lagret i session. dette gjøres for å sikre at det ikke er mulig å endre en bruker uten å være logget inn med den
        if username1 == username:
            conn = get_conn()
            cur = conn.cursor()

            # kjører kode som henter info lagret om brukeren i databasen
            cur.execute('SELECT username, password FROM users where username=%s', (username1,))
            user = cur.fetchone()
            cur.close()
            conn.close()

            # sjekker om en bruker med brukernavnet brukeren skrev inn eksisterer
            if user:
                password_db = user[1]
                if check_password_hash(password_db, password1):
                    conn = get_conn()
                    cur = conn.cursor()

                    cur.execute('SELECT username FROM users where username=%s', (editUsername,))
                    user2 = cur.fetchone()

                    cur.close()
                    conn.close()

                    if user2:
                        form2.username1.errors.append('This username is already taken. Please choose a new username')
                    else:
                        conn = get_conn()
                        cur = conn.cursor()

                        # oppdaterer brukernavn og passord til brukeren i databasen
                        cur.execute('UPDATE users SET username=%s, password=%s WHERE username=%s', (editUsername, password_hash, username1))
                        conn.commit()
                        cur.close()
                        conn.close()
                    
                        conn = get_conn()
                        cur = conn.cursor()

                        # henter brukernavn og score til brukeren som nettopp ble endret og lagrer dataen i en variabel 'user3'
                        cur.execute('SELECT username, score FROM users WHERE username = %s', (editUsername,))
                        user3 = cur.fetchone()

                        cur.close()
                        conn.close()

                        # sjekker om data ble lagret i user3
                        if user3:
                            # oppdaterer session data til å matche brukernavn og score til den redigerte brukeren
                            session['username'] = user3[0]
                            session['score'] = user3[1]
                            form2.password1.errors.append(f'Succesfully saved changes made to user {username1}')
                else:
                    # gir brukeren en feilmelding
                    form2.username1.errors.append("Password doesnt match your current user's password")
        else:
            form2.username1.errors.append("Username doesnt match the current user's username")

    # Delete User form
    if form3.submitDelete.data and form3.validate_on_submit():
        username2 = form3.username2.data
        password2 = form3.password2.data

         # sjekker om brukernavnet spilleren fylte inn stemmer med brukernavnet lagret i session. dette gjøres for å sikre at det ikke er mulig å slette en bruker uten å være logget inn med den
        if username2 == username:
            conn = get_conn()
            cur = conn.cursor()

            # lagrer info til brukeren som en variabel 'user4'
            cur.execute('SELECT username, password FROM users WHERE username=%s', (username2,))
            user4 = cur.fetchone()

            cur.close()
            conn.close()

            # sjekker om en bruker med brukernavnet brukeren skrev inn eksisterer
            if user4:
                password_db2 = user4[1]
                if check_password_hash(password_db2, password2):
                    conn = get_conn()
                    cur = conn.cursor()

                    # kjører kode som sletter brukeren fra databasen
                    cur.execute('DELETE FROM users WHERE username=%s', (username2,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    # sletter session dataen til brukeren
                    session.pop('username')
                    session.pop('score')
                    form3.password2.errors.append(f'Successfully deleted user {username2}')
                else:
                    form3.username2.errors.append("Password doesnt match your current user's password")
        else:
            form3.username2.errors.append("Username doesnt match the current user's username")

    return render_template('manage.html', form=form, form2=form2, form3=form3)

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
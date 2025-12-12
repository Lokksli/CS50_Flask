from flask import Flask, render_template
import sqlite3


app = Flask(__name__)

nameOne = "BLIND"
speedOne = 10
turnOne = 10
distanceOne = 150 

nameTwo = "FAST"
speedTwo = 30
turnTwo = 0
distanceTwo = 100

nameThird = "SMART"
speedThird = 5
turnThird = 12
distanceThird = 80


def get_db():
    # Opens a connection to the SQLite file each request
    conn = sqlite3.connect("parameters.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def hello():
    nameOne = "BLIND"
    speedOne = 10
    turnOne = 10
    distanceOne = 150 

    nameTwo = "FAST"
    speedTwo = 30
    turnTwo = 0
    distanceTwo = 100

    nameThird = "SMART"
    speedThird = 5
    turnThird = 12
    distanceThird = 80
    with sqlite3.connect("parameters.db", check_same_thread=False) as conn:
        cursor = conn.cursor()

        # Insert only if not exists
        cursor.execute("SELECT id FROM robots WHERE name = ?", (nameOne,))
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO robots (name, speed, turn, fdistance) VALUES (?, ?, ?, ?)",
                (nameOne, speedOne, turnOne, distanceOne)
            )
        
        cursor.execute("SELECT id FROM robots WHERE name = ?", (nameTwo,))
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO robots (name, speed, turn, fdistance) VALUES (?, ?, ?, ?)",
                (nameTwo, speedTwo, turnTwo, distanceTwo)
            )

        cursor.execute("SELECT id FROM robots WHERE name = ?", (nameThird,))
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO robots (name, speed, turn, fdistance) VALUES (?, ?, ?, ?)",
                (nameThird, speedThird, turnThird, distanceThird)
            )


        # Fetch data
        cursor.execute("SELECT speed, turn, fdistance FROM robots WHERE name = ?", (nameOne,))
        row = cursor.fetchone()
        speedOne, turnOne, distanceOne = row

        cursor.execute("SELECT speed, turn, fdistance FROM robots WHERE name = ?", (nameTwo,))
        row2 = cursor.fetchone()
        speedTwo, turnTwo, distanceTwo = row2

        cursor.execute("SELECT speed, turn, fdistance FROM robots WHERE name = ?", (nameThird,))
        row3 = cursor.fetchone()
        speedThird, turnThird, distanceThird = row3

    return render_template('index.html', speedO=speedOne, turnO=turnOne, distanceO=distanceOne, speedT=speedTwo, turnT=turnTwo, distanceT=distanceTwo, speedTH=speedThird, turnTH=turnThird, distanceTH=distanceThird)



if __name__ == '__main__':
    app.run(debug=True)
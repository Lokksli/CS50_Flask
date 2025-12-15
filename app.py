from flask import Flask, render_template
import sqlite3
import serial
import threading

app = Flask(__name__)

DB_NAME = "parameters.db"

SERIAL_PORT = "COM5"
BAUD_RATE = 9600

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def serial_listener():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    conn = get_db()
    cursor = conn.cursor()

    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if not line:
            continue

        try:
            name, speed, turn, distance = line.split(",")
            speed = int(speed)
            turn = int(turn)
            distance = int(distance)

            cursor.execute(
                """
                INSERT INTO robots (name, speed, turn, fdistance)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(name)
                DO UPDATE SET
                    speed = excluded.speed,
                    turn = excluded.turn,
                    fdistance = excluded.fdistance
                """,
                (name, speed, turn, distance)
            )
            conn.commit()
            print("Updated:", name)

        except ValueError:
            print("Bad serial data:", line)

@app.route("/")
def index():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT name, speed, turn, fdistance FROM robots")
    rows = cursor.fetchall()

    robots = [
        {
            "name": row["name"],
            "speed": row["speed"],
            "turn": row["turn"],
            "distance": row["fdistance"],
        }
        for row in rows
    ]

    conn.close()
    return render_template("index.html", robots=robots)


if __name__ == "__main__":
    threading.Thread(target=serial_listener, daemon=True).start()
    app.run(debug=True)



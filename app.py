from flask import Flask, render_template
import sqlite3
import serial
import threading

app = Flask(__name__)

DB_NAME = "parameters.db"

SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def serial_listener():
    print("Starting serial listener...")

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print("CONNECTED TO:", ser.port)
    except Exception as e:
        print("SERIAL OPEN FAILED:", repr(e))
        return

    while True:
        try:
            raw = ser.readline()
            print("RAW BYTES:", raw)

            line = raw.decode("utf-8", errors="ignore").strip()
            print("LINE:", repr(line))

            if not line:
                continue

            parts = line.split(",")
            print("PARTS:", parts)

            if len(parts) != 4:
                print("BAD FORMAT")
                continue

            name, speed, turn, distance = parts

            conn = get_db()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO robots (name, speed, turn, fdistance)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(name)
                DO UPDATE SET
                    speed=excluded.speed,
                    turn=excluded.turn,
                    fdistance=excluded.fdistance
            """, (name, int(speed), int(turn), int(distance)))

            conn.commit()
            conn.close()

            print("DB UPDATED:", name)

        except Exception as e:
            print("LOOP ERROR:", repr(e))


@app.route("/")
def index():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT name, speed, turn, fdistance FROM robots")
    rows = cursor.fetchall()
    conn.close()

    robots = [
        {
            "name": row["name"],
            "speed": row["speed"],
            "turn": row["turn"],
            "distance": row["fdistance"],
        }
        for row in rows
    ]

    return render_template("index.html", robots=robots)


if __name__ == "__main__":
    threading.Thread(target=serial_listener, daemon=True).start()
    app.run(debug=True, use_reloader=False)

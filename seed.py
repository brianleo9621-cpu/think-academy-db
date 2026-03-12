import csv
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# ── Load credentials from .env ────────────────────────────────────────────────
load_dotenv()

DB_CONFIG = {
    "host":     os.getenv("DB_HOST"),
    "user":     os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

CSV_FILE = "sat_responses.csv"

# ── Insert student if not exists, return their ID ─────────────────────────────
def get_or_create_student(cursor, name, email, age):
    cursor.execute("SELECT student_id FROM students WHERE email = %s", (email,))
    result = cursor.fetchone()
    if result:
        return result[0]
    cursor.execute(
        "INSERT INTO students (name, email, age) VALUES (%s, %s, %s)",
        (name, email, age)
    )
    return cursor.lastrowid

# ── Main load function ────────────────────────────────────────────────────────
def load_csv_to_mysql(filepath):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        inserted = 0
        bad_rows = []

        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for i, row in enumerate(reader, start=2):

                # ── Validate ──────────────────────────────────────────────────
                if not row.get("name") or not row.get("email"):
                    bad_rows.append((i, "missing name or email", row))
                    continue
                try:
                    score = int(row["score"])
                    age   = int(row["age"])
                except (ValueError, KeyError):
                    bad_rows.append((i, "invalid score or age", row))
                    continue

                # ── Insert student, then their response ───────────────────────
                student_id = get_or_create_student(
                    cursor,
                    row["name"].strip(),
                    row["email"].strip().lower(),
                    age
                )

                cursor.execute(
                    """INSERT INTO sat_responses (student_id, score, submitted_at)
                       VALUES (%s, %s, %s)""",
                    (student_id, score, row.get("submitted_at", None))
                )

                inserted += 1

        conn.commit()

        # ── Summary ───────────────────────────────────────────────────────────
        print(f"Done! Inserted {inserted} responses.")
        if bad_rows:
            print(f"\nSkipped {len(bad_rows)} bad rows:")
            for line_num, reason, data in bad_rows:
                print(f"  Row {line_num}: {reason} → {data}")

    except Error as e:
        print(f"Database error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Connection closed.")

# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    load_csv_to_mysql(CSV_FILE)

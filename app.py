from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_database():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            type TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY id DESC")
    transactions = cursor.fetchall()
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Income'")
    income = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense'")
    expenses = cursor.fetchone()[0] or 0
    conn.close()

    return render_template(
        "index.html",
        transactions=transactions,
        income=income,
        expenses=expenses,
        balance=income-expenses
    )

@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    amount = float(request.form["amount"])
    category = request.form["category"]
    transaction_type = request.form["type"]

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (title, amount, category, type) VALUES (?, ?, ?, ?)",
        (title, amount, category, transaction_type)
    )
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    create_database()
    app.run(debug=True)
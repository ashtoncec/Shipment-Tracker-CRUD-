import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

# creates the Flask app and allows CORS requests (important so the frontend can talk to backend!)
app = Flask(__name__)
CORS(app)

DB_PATH = "shipments.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS shipments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
        """
    )
    # seed some starter data on first run so the app isn't empty
    count = conn.execute("SELECT COUNT(*) FROM shipments").fetchone()[0]
    if count == 0:
        conn.executemany(
            "INSERT INTO shipments (item, quantity) VALUES (?, ?)",
            [("Sweater", 50), ("Jeans", 30), ("Sneakers", 20)],
        )
    conn.commit()
    conn.close()


# Home route (just used to verify the server is running)
@app.route("/")
def home():
    return "Hello!"


# GET request (fetch all shipments)
@app.route("/api/shipments", methods=["GET"])
def get_shipments():
    conn = get_db()
    rows = conn.execute("SELECT * FROM shipments").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


# POST request (add a new shipment)
@app.route("/api/shipments", methods=["POST"])
def add_shipment():
    data = request.get_json()
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO shipments (item, quantity) VALUES (?, ?)",
        (data["item"], data["quantity"]),
    )
    conn.commit()
    new_shipment = {"id": cursor.lastrowid, "item": data["item"], "quantity": data["quantity"]}
    conn.close()
    return jsonify(new_shipment), 201


# PUT request to update an existing shipment by ID
@app.route("/api/shipments/<int:shipment_id>", methods=["PUT"])
def update_shipment(shipment_id):
    data = request.get_json()
    conn = get_db()
    existing = conn.execute("SELECT * FROM shipments WHERE id = ?", (shipment_id,)).fetchone()
    if existing is None:
        conn.close()
        return jsonify({"error": "Shipment not found"}), 404

    item = data.get("item", existing["item"])
    quantity = data.get("quantity", existing["quantity"])
    conn.execute(
        "UPDATE shipments SET item = ?, quantity = ? WHERE id = ?",
        (item, quantity, shipment_id),
    )
    conn.commit()
    conn.close()
    return jsonify({"id": shipment_id, "item": item, "quantity": quantity})


# DELETE request to remove a shipment by ID
@app.route("/api/shipments/<int:shipment_id>", methods=["DELETE"])
def delete_shipment(shipment_id):
    conn = get_db()
    conn.execute("DELETE FROM shipments WHERE id = ?", (shipment_id,))
    conn.commit()
    conn.close()
    return "", 204  # No content


# Run the server on port 5001, experienced issues with other ports
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)

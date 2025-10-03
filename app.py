from flask import Flask, jsonify, request
from flask_cors import CORS

# creates the Flask app and allows CORS requests (important so the frontend can talk to backend!)
app = Flask(__name__)
CORS(app)

# fake database (just stored in memory for now)
shipments = [
    {"id": 1, "item": "Sweater", "quantity": 50},
    {"id": 2, "item": "Jeans", "quantity": 30},
    {"id": 3, "item": "Sneakers", "quantity": 20}
]

# Home route (just used to verify the server is running)
@app.route("/")
def home():
    return "Hello!"

# GET request (fetch all shipments)
@app.route("/api/shipments", methods=["GET"])
def get_shipments():
    return jsonify(shipments)

# POST request (add a new shipment)
@app.route("/api/shipments", methods=["POST"])
def add_shipment():
    data = request.get_json()
    new_id = max([s["id"] for s in shipments], default=0) + 1
    new_shipment = {
        "id": new_id,
        "item": data["item"],
        "quantity": data["quantity"]
    }
    shipments.append(new_shipment)
    return jsonify(new_shipment), 201

# DELETE request to remove a shipment by ID
@app.route("/api/shipments/<int:shipment_id>", methods=["DELETE"])
def delete_shipment(shipment_id):
    global shipments
    shipments = [s for s in shipments if s["id"] != shipment_id]
    return "", 204  # No content

# Run the server on port 5001, experienced issues with other ports
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)




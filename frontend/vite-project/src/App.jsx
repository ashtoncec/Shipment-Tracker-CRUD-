import { useEffect, useState } from "react";

// the main UI 
function App() {
  // holds the list of shipments we get from the backend
  const [shipments, setShipments] = useState([]);

  // State for the form inputs (for adding a new shipment)
  const [newItem, setNewItem] = useState("");
  const [newQuantity, setNewQuantity] = useState("");

  // runs once when the component loads and it fetches all the current shipments
  useEffect(() => {
    console.log("Fetching shipments...");
    fetch("http://localhost:5001/api/shipments")
      .then((res) => res.json())
      .then((data) => {
        console.log("Data received:", data);
        setShipments(data);
      })
      .catch((err) => console.error("Failed to fetch shipments:", err));
  }, []);

  // handles form submission to add a shipment
  const handleAdd = () => {
    if (!newItem || !newQuantity) return;

    // POST request to the backend to add the new shipment
    fetch("http://localhost:5001/api/shipments", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        item: newItem,
        quantity: parseInt(newQuantity),
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        // add the new shipment to the list in the UI
        setShipments([...shipments, data]);
        setNewItem("");
        setNewQuantity("");
      })
      .catch((err) => console.error("Failed to add shipment:", err));
  };

  // function to delete a shipment by ID
  const handleDelete = (id) => {
    fetch(`http://localhost:5001/api/shipments/${id}`, {
      method: "DELETE",
    })
      .then((res) => {
        if (res.ok) {
          // filter out the deleted shipment from the list
          setShipments(shipments.filter((s) => s.id !== id));
        }
      })
      .catch((err) => console.error("Failed to delete shipment:", err));
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>RetailReady Shipment Tracker</h1>

      {/* form for adding a new shipment */}
      <div style={styles.form}>
        <input
          type="text"
          placeholder="Item name"
          value={newItem}
          onChange={(e) => setNewItem(e.target.value)}
          style={styles.input}
        />
        <input
          type="number"
          placeholder="Quantity"
          value={newQuantity}
          onChange={(e) => setNewQuantity(e.target.value)}
          style={styles.input}
        />
        <button onClick={handleAdd} style={styles.button}>
          Add Shipment
        </button>
      </div>

      {/* the shipment cards (aka the loading state) */}
      {shipments.length === 0 ? (
        <p style={styles.loading}>Loading shipments...</p>
      ) : (
        <div style={styles.cardContainer}>
          {shipments.map((s) => (
            <div key={s.id} style={styles.card}>
              <h2 style={styles.item}>{s.item}</h2>
              <p style={styles.details}>Quantity: {s.quantity}</p>
              <button onClick={() => handleDelete(s.id)} style={styles.delete}>
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// basic styling using inline styles
const styles = {
  container: {
    fontFamily: "Arial, sans-serif",
    padding: "2rem",
    backgroundColor: "#f4f4f4",
    minHeight: "100vh",
  },
  title: {
    textAlign: "center",
    color: "#222",
  },
  form: {
    display: "flex",
    justifyContent: "center",
    gap: "1rem",
    marginBottom: "2rem",
  },
  input: {
    padding: "0.5rem",
    fontSize: "1rem",
  },
  button: {
    padding: "0.5rem 1rem",
    fontSize: "1rem",
    backgroundColor: "#4CAF50",
    color: "white",
    border: "none",
    cursor: "pointer",
  },
  loading: {
    textAlign: "center",
    fontStyle: "italic",
  },
  cardContainer: {
    display: "flex",
    gap: "1rem",
    flexWrap: "wrap",
    justifyContent: "center",
    marginTop: "2rem",
  },
  card: {
    backgroundColor: "#fff",
    padding: "1rem 2rem",
    borderRadius: "8px",
    boxShadow: "0 0 10px rgba(0,0,0,0.1)",
    width: "200px",
    textAlign: "center",
  },
  item: {
    margin: 0,
    fontSize: "1.25rem",
    color: "#333",
  },
  details: {
    marginTop: "0.5rem",
    color: "#555",
  },
  delete: {
    marginTop: "0.75rem",
    padding: "0.25rem 0.5rem",
    backgroundColor: "#f44336",
    color: "white",
    border: "none",
    cursor: "pointer",
  },
};

export default App;



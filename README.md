# 🛰️ OSPF Protocol Simulator

A visually interactive **OSPF (Open Shortest Path First)** network simulator built using **Python (Tkinter + Dijkstra’s Algorithm)**.
Design, visualize, and simulate dynamic shortest-path routing between routers in real time.

---

## Overview

This project simulates the **OSPF routing protocol**, which is widely used in real-world networking to find the shortest path between routers dynamically.
The simulator provides an intuitive GUI to:

* Add routers and connect them with customizable link costs
* Run OSPF to compute shortest paths using **Dijkstra’s algorithm**
* Display all routers’ **routing tables**
* Visually highlight the **shortest path** between any two routers

All this in a **modern dark-themed interface**.

---

## 🖼️ Demo Preview

https://github.com/user-attachments/assets/1633abf5-3d90-4e12-a0f9-4813fc26ef25


---

## ⚙️ How It Works

1. **Add Routers**
   Enter a router ID (integer) and click “Add Router”.

2. **Add Links**
   Enter two router IDs and a link cost. This creates a bidirectional edge.

3. **Run OSPF**
   Click **Run OSPF** — each router runs **Dijkstra’s algorithm** to compute shortest paths to all others.

4. **Find Path**
   Specify a source and destination router. The simulator highlights the **shortest path** in green and displays total cost.

5. **View Routing Tables**
   See the OSPF routing tables for each router on the right panel.

6. **Clear All**
   Reset the entire network in one click.

---

## Tech Stack

| Component                   | Description                |
| --------------------------- | -------------------------- |
| 🐍 **Python 3.x**           | Programming language       |
| 🧮 **Dijkstra’s Algorithm** | Shortest path computation  |
| 🖥️ **Tkinter**              | GUI framework              |
| 🎨 **Custom ttk Styling**   | Dark mode + modern buttons |

---

## Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/OSPF-Simulator.git
cd OSPF-Simulator
```

### 2️⃣ Run the Application

```bash
python ospf_gui.py
```

That’s it! The GUI window should launch instantly.

---

## Concepts Demonstrated

* Graph Theory (Weighted Graphs)
* Shortest Path Algorithms (Dijkstra)
* Link-State Routing Protocols (OSPF)
* GUI Development with Tkinter
* Data Visualization

---

## Possible Extensions

🚧 Future improvements you can try:

* Animate OSPF updates in real time
* Save/load topologies to JSON
* Add dynamic link failures
* Visualize routing table changes step-by-step
* Support for different routing algorithms (e.g., Bellman-Ford)

---

## 📜 License

This project is open-source and available under the **MIT License**.

---

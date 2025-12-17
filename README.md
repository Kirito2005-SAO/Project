# Banker's Algorithm Simulation (Operating Systems Lab)

## 📌 Project Description
This project is a **Python-based simulation of the Banker's Algorithm**, developed as part of the **Operating Systems Laboratory** coursework.  
The application checks whether a system is in a **safe or unsafe state** by simulating multiple random test cases and visualizing the results.

The project uses:
- **Banker's Algorithm** for deadlock avoidance
- **Tkinter** for GUI
- **NumPy** for matrix operations
- **Matplotlib** for graphical visualization

---

## 🎯 Objectives
- Implement Banker's Algorithm for deadlock avoidance
- Analyze system safety based on resource allocation
- Provide a user-friendly GUI for simulation
- Display results using graphical charts

---

## 🛠️ Technologies Used
- **Python 3**
- **Tkinter** (GUI)
- **NumPy** (Matrix calculations)
- **Matplotlib** (Bar graph visualization)

---

## 📂 Project Structure

---

## ⚙️ How Banker's Algorithm Works
Banker's Algorithm determines whether the system is in a **safe state** by checking if all processes can complete execution with the available resources.

### Key Data Structures:
- **Max Demand Matrix** – Maximum resources required by each process
- **Allocation Matrix** – Resources currently allocated
- **Available Vector** – Resources currently available
- **Need Matrix** = Max Demand − Allocation

### Algorithm Steps:
1. Calculate the **Need** matrix
2. Check for a process whose need is less than or equal to available resources
3. Allocate resources temporarily and mark process as finished
4. Repeat until:
   - All processes finish → **Safe State**
   - No process can proceed → **Unsafe State**

---

## 🧠 Program Explanation

### 1️⃣ Safety Check Function
```python
def is_safe_state(max_demand, allocation, available):

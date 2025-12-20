# Banker's Algorithm Safety Analyzer

This project is a Python-based desktop application that simulates and analyzes two key operating system concepts: the **Banker's Algorithm** for deadlock avoidance and a **Deadlock Detection Algorithm**.

It provides a graphical user interface (GUI) to configure and run simulations, displaying the statistical probability of a system being in a "safe" state. The results are presented in both tabular and graphical formats.

---

## ⚙️ Features
- **Banker's Algorithm Simulation**: Determines if a random system state is safe or unsafe.
- **Deadlock Detection Simulation**: Checks for existing deadlocks in a random system state.
- **Configurable Inputs**: Set the maximum number of processes and the number of test cases to run.
- **Tabular Results**: Displays a detailed breakdown of safety probabilities for each process count.
- **Graphical Visualization**:
    - **Probability Plot**: A line graph comparing the safety probability of both algorithms as the number of processes increases.
    - **State Distribution Chart**: A bar chart showing the total count of safe vs. unsafe states across all test runs.
- **Sample Data Viewer**: Inspect the randomly generated matrices (`Max`, `Allocation`, `Available`) for a sample test case.

---

## 🛠️ Technologies Used
- **Python 3**: Core programming language.
- **Tkinter**: For the graphical user interface.
- **NumPy**: For efficient matrix and vector operations.
- **Pandas**: To structure and display results in a clear, tabular format.
- **Matplotlib**: For generating and displaying plots.

---

## 🚀 How to Run
1.  **Prerequisites**: Ensure you have Python 3 and the required libraries installed.
    ```bash
    pip install numpy pandas matplotlib
    ```
2.  **Execute the Script**: Run the `Bankers.py` file from your terminal.
    ```bash
    python Bankers.py
    ```
3.  **Use the Application**:
    - Enter the **Maximum Number of Processes** you want to simulate (e.g., `10`).
    - Enter the **Test Cases per Process Count** (e.g., `1000`). This is the number of random scenarios to generate for each process count (from 2 up to the maximum).
    - Click **Run Simulation**.
    - View the results in the table and the graphs that appear.

---

## 🧠 Core Algorithms Explained

### 1. Banker's Algorithm for Deadlock Avoidance
This algorithm checks if a system is in a **safe state**. A system is considered safe if there exists at least one sequence of process executions that allows all processes to complete without causing a deadlock.

**Key Data Structures:**
-   `max_demand`: A matrix where each row `i` represents the maximum number of resources of each type that process `i` may request.
-   `allocation`: A matrix representing the resources currently allocated to each process.
-   `available`: A vector indicating the number of available resources of each type.
-   `need`: A matrix calculated as `max_demand - allocation`, representing the remaining resources needed by each process.

**Implementation:**
The algorithm iteratively searches for a process `i` that is not yet finished and whose `need` can be satisfied by the `available` resources. If such a process is found, the system assumes it will run to completion and release its `allocation`, which is then added back to the `available` pool. If all processes can finish, the state is safe.

```python
def bankers_algorithm(max_demand, allocation, available):
    n, m = allocation.shape
    need = max_demand - allocation
    work = available.copy()
    finish = [False] * n

    while True:
        found = False
        for i in range(n):
            if not finish[i] and np.all(need[i] <= work):
                work += allocation[i]
                finish[i] = True
                found = True
        if not found:
            break

    return all(finish)
```

### 2. Deadlock Detection Algorithm
This algorithm determines if a deadlock already exists in the system. Unlike the Banker's Algorithm, it does not look ahead at future needs (`Max` demand) but instead works with current allocations and requests.

**Key Data Structures:**
-   `allocation`: The resources currently allocated.
-   `request`: A matrix representing the current pending resource requests for each process.
-   `available`: The currently available resources.

**Implementation:**
The algorithm checks if there are any processes that are not blocked (i.e., their `request` can be met by the `available` resources). It assumes such processes will eventually finish and release their `allocation`. If, after this process, there are still unfinished processes whose requests cannot be met, a deadlock is detected.

```python
def deadlock_detection(allocation, request, available):
    n, m = allocation.shape
    work = available.copy()
    finish = [False] * n

    while True:
        progress = False
        for i in range(n):
            if not finish[i] and np.all(request[i] <= work):
                work += allocation[i]
                finish[i] = True
                progress = True
        if not progress:
            break

    return all(finish)  # True = No Deadlock, False = Deadlock Exists
```

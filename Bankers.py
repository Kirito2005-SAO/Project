import tkinter as tk
from tkinter import messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- GLOBAL STORAGE ---------------- #
sample_matrices = {}
state_counts = {}

# ---------------- ALGORITHMS ---------------- #


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

    return all(finish)  # True = safe (no deadlock), False = deadlock exists

# ---------------- SIMULATION ---------------- #


def run_simulation():
    try:
        max_proc = int(proc_entry.get())
        trials = int(test_entry.get())
    except:
        messagebox.showerror("Error", "Enter valid numeric values")
        return

    resources = 3
    results = []
    sample_matrices.clear()
    state_counts.clear()

    total_safe = 0
    total_unsafe = 0

    for processes in range(2, max_proc + 1):
        banker_safe = 0
        deadlock_safe = 0
        banker_unsafe = 0

        for t in range(trials):
            max_demand = np.random.randint(1, 10, (processes, resources))
            allocation = np.random.randint(0, max_demand)
            available = np.random.randint(1, 10, resources)

            # Generate a random request for deadlock detection (≤ max demand)
            request = np.random.randint(0, max_demand - allocation + 1)

            # Save sample system state
            if processes == 2 and t == 0:
                sample_matrices["Max"] = max_demand
                sample_matrices["Allocation"] = allocation
                sample_matrices["Available"] = available

            # Banker check
            if bankers_algorithm(max_demand, allocation, available):
                banker_safe += 1
                total_safe += 1
            else:
                banker_unsafe += 1
                total_unsafe += 1

            # Deadlock Detection check
            if deadlock_detection(allocation, request, available):
                deadlock_safe += 1

        banker_prob = (banker_safe / trials) * 100
        deadlock_prob = (deadlock_safe / trials) * 100
        results.append([processes, banker_prob, deadlock_prob])

    state_counts["Safe"] = total_safe
    state_counts["Unsafe"] = total_unsafe

    df = pd.DataFrame(
        results,
        columns=["Processes", "Banker Safety %", "Deadlock Detection Safety %"]
    )

    display_results(df)
    plot_probability_graph(df)
    plot_safe_unsafe_graph()


# ---------------- DISPLAY FUNCTIONS ---------------- #

def display_results(df):
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, df.to_string(index=False))


def plot_probability_graph(df):
    plt.figure(figsize=(8, 5))
    plt.plot(df["Processes"], df["Banker Safety %"],
             marker='o', label="Banker's Algorithm")
    plt.plot(df["Processes"], df["Deadlock Detection Safety %"],
             marker='s', label="Deadlock Detection")
    plt.xlabel("Number of Processes")
    plt.ylabel("Safety Probability (%)")
    plt.title("Processes vs Safety Probability")
    plt.legend()
    plt.grid(True)
    plt.show(block=False)


def plot_safe_unsafe_graph():
    plt.figure(figsize=(6, 4))
    plt.bar(state_counts.keys(), state_counts.values(),
            color=["green", "red"])
    plt.xlabel("System State")
    plt.ylabel("Number of Test Cases")
    plt.title("Safe State vs Unsafe State Distribution")
    plt.show(block=False)


def show_sample_matrices():
    if not sample_matrices:
        messagebox.showinfo("Info", "Run simulation first")
        return

    text = (
        "SAMPLE RANDOM SYSTEM STATE\n\n"
        f"Max Matrix:\n{sample_matrices['Max']}\n\n"
        f"Allocation Matrix:\n{sample_matrices['Allocation']}\n\n"
        f"Available Vector:\n{sample_matrices['Available']}"
    )

    window = tk.Toplevel(root)
    window.title("Sample Random Matrices")
    window.geometry("450x350")

    txt = tk.Text(window, font=("Consolas", 10))
    txt.pack(expand=True, fill="both")
    txt.insert(tk.END, text)
    txt.config(state="disabled")


# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Banker's Algorithm Safety Analyzer")
root.geometry("680x540")

tk.Label(root, text="Maximum Number of Processes").pack(pady=5)
proc_entry = tk.Entry(root)
proc_entry.pack()

tk.Label(root, text="Test Cases per Process Count").pack(pady=5)
test_entry = tk.Entry(root)
test_entry.pack()

tk.Button(root, text="Run Simulation", command=run_simulation).pack(pady=10)
tk.Button(root, text="Show Sample Random Matrices",
          command=show_sample_matrices).pack(pady=5)

result_text = tk.Text(root, height=14, width=78, font=("Consolas", 10))
result_text.pack(pady=10)

root.mainloop()

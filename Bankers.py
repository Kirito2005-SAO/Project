import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt


def is_safe_state(max_demand, allocation, available):
    n, m = allocation.shape
    need = max_demand - allocation
    work = available.copy()
    finish = [False] * n

    while True:
        found = False
        for i in range(n):
            if not finish[i] and all(need[i] <= work):
                work += allocation[i]
                finish[i] = True
                found = True
        if not found:
            break

    return all(finish)


def run_simulation():
    try:
        processes = int(proc_entry.get())
        trials = int(test_entry.get())
    except:
        messagebox.showerror("Error", "Enter valid numbers")
        return

    safe_count = 0
    resources = 3

    for _ in range(trials):
        max_demand = np.random.randint(1, 10, (processes, resources))
        allocation = np.random.randint(0, max_demand)
        available = np.random.randint(1, 10, resources)

        if is_safe_state(max_demand, allocation, available):
            safe_count += 1

    unsafe_count = trials - safe_count
    probability = (safe_count / trials) * 100

    result_label.config(
        text=f"Safe States: {safe_count}\n"
        f"Unsafe States: {unsafe_count}\n"
        f"Safety Probability: {probability:.2f}%"
    )

    plt.figure()
    plt.bar(["Safe", "Unsafe"], [safe_count, unsafe_count])
    plt.title("Banker's Algorithm Safety Result")
    plt.show()

# ---------------- GUI ---------------- #


root = tk.Tk()
root.title("Banker's Algorithm Analyzer")
root.geometry("350x300")

tk.Label(root, text="Number of Processes").pack(pady=5)
proc_entry = tk.Entry(root)
proc_entry.pack()

tk.Label(root, text="Number of Test Cases").pack(pady=5)
test_entry = tk.Entry(root)
test_entry.pack()

tk.Button(root, text="Run Simulation", command=run_simulation).pack(pady=15)

result_label = tk.Label(root, text="", font=("Arial", 10))
result_label.pack()

root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# ---------------------------
# 0/1 Knapsack GUI Application
# ---------------------------

class KnapsackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("0/1 Knapsack - Product Bundle Optimization")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # Data storage: list of dicts {name, cost, profit}
        self.items = []

        self.build_ui()

    def build_ui(self):
        header = tk.Label(self.root, text="0/1 Knapsack — Product Bundle Optimization",
                          font=("Helvetica", 16, "bold"), bg="#2c3e50", fg="white", padx=10, pady=8)
        header.pack(fill=tk.X)

        main_frame = tk.Frame(self.root, padx=12, pady=12)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame — input & controls
        left = tk.Frame(main_frame)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0,12))

        # Input fields
        ttk.Label(left, text="Product Name:").pack(anchor="w")
        self.entry_name = ttk.Entry(left, width=28)
        self.entry_name.pack(pady=4)

        ttk.Label(left, text="Cost (weight / price) [Integer]:").pack(anchor="w")
        self.entry_cost = ttk.Entry(left, width=28)
        self.entry_cost.pack(pady=4)

        ttk.Label(left, text="Profit (value) [Integer]:").pack(anchor="w")
        self.entry_profit = ttk.Entry(left, width=28)
        self.entry_profit.pack(pady=4)

        add_btn = ttk.Button(left, text="Add Product", command=self.add_item)
        add_btn.pack(pady=(8,4), fill=tk.X)

        remove_btn = ttk.Button(left, text="Remove Selected", command=self.remove_selected)
        remove_btn.pack(pady=4, fill=tk.X)

        clear_btn = ttk.Button(left, text="Clear All", command=self.clear_all)
        clear_btn.pack(pady=4, fill=tk.X)

        # Capacity input and run
        ttk.Separator(left, orient="horizontal").pack(fill=tk.X, pady=8)
        ttk.Label(left, text="Budget / Capacity [Integer]:").pack(anchor="w")
        self.entry_capacity = ttk.Entry(left, width=28)
        self.entry_capacity.pack(pady=4)
        self.entry_capacity.insert(0, "50")  # default

        run_btn = tk.Button(left, text="Run Optimization", bg="#27ae60", fg="white",
                            font=("Helvetica", 11, "bold"), command=self.run_knapsack)
        run_btn.pack(pady=(12,6), fill=tk.X)

        # Info / totals
        self.total_items_label = ttk.Label(left, text="Total Products: 0")
        self.total_items_label.pack(anchor="w", pady=(10,2))

        self.result_label = ttk.Label(left, text="Last Run Result: N/A")
        self.result_label.pack(anchor="w")

        # Right frame — table + chart
        right = tk.Frame(main_frame)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Products table
        table_frame = tk.Frame(right)
        table_frame.pack(fill=tk.BOTH, expand=False)

        cols = ("Name", "Cost", "Profit")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="center", width=120)
        self.tree.pack(side=tk.LEFT, fill=tk.X, expand=True)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # Detail frame for results & chart
        detail_frame = tk.Frame(right, pady=12)
        detail_frame.pack(fill=tk.BOTH, expand=True)

        # Selected items table
        sel_label = tk.Label(detail_frame, text="Selected Items (Optimal Bundle):", font=("Helvetica", 12, "bold"))
        sel_label.pack(anchor="w")

        sel_cols = ("Name", "Cost", "Profit")
        self.sel_tree = ttk.Treeview(detail_frame, columns=sel_cols, show="headings", height=6)
        for c in sel_cols:
            self.sel_tree.heading(c, text=c)
            self.sel_tree.column(c, anchor="center", width=140)
        self.sel_tree.pack(fill=tk.X, pady=(4,10))

        # totals
        totals_frame = tk.Frame(detail_frame)
        totals_frame.pack(fill=tk.X, pady=(0,8))
        self.total_cost_var = tk.StringVar(value="Total Cost: 0")
        self.total_profit_var = tk.StringVar(value="Total Profit: 0")
        ttk.Label(totals_frame, textvariable=self.total_cost_var).pack(side=tk.LEFT, padx=(0,12))
        ttk.Label(totals_frame, textvariable=self.total_profit_var).pack(side=tk.LEFT)

        # Chart area (Matplotlib)
        chart_label = tk.Label(detail_frame, text="Chart: Profit of Selected Items", font=("Helvetica", 12))
        chart_label.pack(anchor="w")

        self.fig, self.ax = plt.subplots(figsize=(5,2.5))
        plt.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=detail_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # -------------------------
    # Item management methods
    # -------------------------
    def add_item(self):
        name = self.entry_name.get().strip()
        cost = self.entry_cost.get().strip()
        profit = self.entry_profit.get().strip()

        if not name or not cost or not profit:
            messagebox.showwarning("Input Error", "Please fill all fields (Name, Cost, Profit).")
            return

        # Only allow integer costs/profits
        try:
            cost_i = int(cost)
            profit_i = int(profit)
            if cost_i <= 0 or profit_i < 0:
                messagebox.showwarning("Input Error", "Cost must be > 0 and Profit must be >= 0 (integers).")
                return
        except ValueError:
            messagebox.showwarning("Input Error", "Cost and Profit must be integer numbers.")
            return

        # Add to internal list and update table
        self.items.append({"name": name, "cost": cost_i, "profit": profit_i})
        self.tree.insert("", tk.END, values=(name, cost_i, profit_i))

        # Clear inputs
        self.entry_name.delete(0, tk.END)
        self.entry_cost.delete(0, tk.END)
        self.entry_profit.delete(0, tk.END)

        self.update_totals_info()

    def remove_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Remove", "Please select a product in the product list to remove.")
            return
        for item_id in selected:
            vals = self.tree.item(item_id, "values")
            name, cost, profit = vals[0], int(vals[1]), int(vals[2])
            # remove first matching in internal list
            for i, it in enumerate(self.items):
                if it["name"] == name and it["cost"] == cost and it["profit"] == profit:
                    del self.items[i]
                    break
            self.tree.delete(item_id)
        self.update_totals_info()

    def clear_all(self):
        if messagebox.askyesno("Confirm", "Clear all products and results?"):
            self.items.clear()
            for i in self.tree.get_children():
                self.tree.delete(i)
            for i in self.sel_tree.get_children():
                self.sel_tree.delete(i)
            self.total_cost_var.set("Total Cost: 0")
            self.total_profit_var.set("Total Profit: 0")
            self.result_label.config(text="Last Run Result: N/A")
            self.ax.clear()
            self.canvas.draw()
            self.update_totals_info()

    def update_totals_info(self):
        self.total_items_label.config(text=f"Total Products: {len(self.items)}")

    # -------------------------
    # Knapsack solver (0/1 DP)
    # -------------------------
    def run_knapsack(self):
        if not self.items:
            messagebox.showinfo("No Items", "Please add some products first.")
            return
        cap_str = self.entry_capacity.get().strip()
        if not cap_str:
            messagebox.showwarning("Input Error", "Please enter budget / capacity (integer).")
            return
        try:
            capacity = int(cap_str)
            if capacity <= 0:
                messagebox.showwarning("Input Error", "Capacity must be a positive integer.")
                return
        except ValueError:
            messagebox.showwarning("Input Error", "Capacity must be an integer.")
            return

        n = len(self.items)
        weights = [it["cost"] for it in self.items]
        values = [it["profit"] for it in self.items]

        # DP table (n+1) x (capacity+1)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]

        # Fill DP table
        for i in range(1, n + 1):
            w = weights[i - 1]
            v = values[i - 1]
            for c in range(capacity + 1):
                if w <= c:
                    dp[i][c] = max(dp[i - 1][c], dp[i - 1][c - w] + v)
                else:
                    dp[i][c] = dp[i - 1][c]

        max_profit = dp[n][capacity]

        # Backtrack to find selected items
        selected_indices = []
        c = capacity
        for i in range(n, 0, -1):
            if dp[i][c] != dp[i - 1][c]:
                # item i-1 was included
                selected_indices.append(i - 1)
                c -= weights[i - 1]

        selected_indices.reverse()

        # Update result UI
        for i in self.sel_tree.get_children():
            self.sel_tree.delete(i)
        total_cost = 0
        total_profit = 0
        for idx in selected_indices:
            it = self.items[idx]
            self.sel_tree.insert("", tk.END, values=(it["name"], it["cost"], it["profit"]))
            total_cost += it["cost"]
            total_profit += it["profit"]

        self.total_cost_var.set(f"Total Cost: {total_cost}")
        self.total_profit_var.set(f"Total Profit: {total_profit}")
        self.result_label.config(text=f"Last Run Result: Profit = {max_profit} (Capacity {capacity})")

        # Draw bar chart of selected items' profits
        self.ax.clear()
        if selected_indices:
            names = [self.items[i]["name"] for i in selected_indices]
            profits = [self.items[i]["profit"] for i in selected_indices]
            bars = self.ax.bar(names, profits)
            self.ax.set_ylabel("Profit")
            self.ax.set_title("Profit of Selected Items")
            self.ax.bar_label(bars, padding=3)
            self.fig.tight_layout()
        else:
            self.ax.text(0.5, 0.5, "No items selected\n(infeasible or capacity 0)", ha='center')
        self.canvas.draw()

# ---------------------------
# Run the application
# ---------------------------
def main():
    root = tk.Tk()
    app = KnapsackApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
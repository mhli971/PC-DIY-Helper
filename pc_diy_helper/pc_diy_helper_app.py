# main.py
import tkinter as tk
from tkinter import ttk
import json
import sys
import getpass

sys.path.append(f"/Users/{getpass.getuser()}/git/mhli971/PC-DIY-Helper/")


class PCDIYHelperApp(tk.Tk):
    class PriceManager:
        def __init__(self, filename):
            with open(filename) as f:
                self.prices = json.load(f)

        def get_price(self, category, name):
            return self.prices.get(category, {}).get(name, 0)

    class Dropdown:
        def __init__(self, master, label_text, options, update_func, row, column):
            self.label = ttk.Label(master, text=label_text)
            self.label.grid(row=row, column=column, pady=5, padx=5)
            self.var = tk.StringVar(master)
            self.var.set(options[0])  # set the default option
            self.menu = ttk.Combobox(master, textvariable=self.var, values=options)
            self.menu.grid(row=row, column=column + 1, pady=5, padx=5)
            self.menu.bind("<<ComboboxSelected>>", update_func)

    class Updater:
        def __init__(self, data, from_dropdown, to_dropdown, next_updater=None):
            self.data = data
            self.from_dropdown = from_dropdown
            self.to_dropdown = to_dropdown
            self.next_updater = next_updater

        def update(self, event):
            key = self.from_dropdown.var.get()
            values = self.data.get(key, [])
            if values:  # check if values is not an empty list
                self.to_dropdown.var.set(values[0])  # set the default option
                self.to_dropdown.menu["values"] = values
                if self.next_updater is not None:
                    self.next_updater.update(None)

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("PC DIY Helper")
        self.geometry("1450x500")

        # Load configuration
        with open("pc_diy_helper/config.json") as f:
            config = json.load(f)
        self.cpus = config["CPUs"]
        self.gpus = config["GPUs"]
        self.motherboards = config["Motherboards"]
        self.rams = config["RAM"]
        self.ssds = config["SSD"]
        self.coolings = config["Cooling"]
        self.fans = config["Fans"]
        self.psus = config["PSU"]
        self.cases = config["Case"]

        # Price manager
        self.price_manager = PCDIYHelperApp.PriceManager("pc_diy_helper/prices.json")

        # Dropdowns
        self.gpu_dropdown = PCDIYHelperApp.Dropdown(
            self, "Select GPU:", list(self.gpus.keys()), None, 0, 0
        )
        self.cpu_dropdown = PCDIYHelperApp.Dropdown(
            self, "Select CPU:", self.gpus[self.gpu_dropdown.var.get()], None, 1, 0
        )
        self.motherboard_dropdown = PCDIYHelperApp.Dropdown(
            self,
            "Select Motherboard:",
            self.cpus.get(self.cpu_dropdown.var.get(), []),
            None,
            2,
            0,
        )
        self.ram_dropdown = PCDIYHelperApp.Dropdown(
            self, "Select RAM:", self.rams, self.do_nothing, 0, 2
        )
        self.ssd_dropdown = PCDIYHelperApp.Dropdown(
            self, "Select SSD:", self.ssds, self.do_nothing, 1, 2
        )
        self.cooling_dropdown = PCDIYHelperApp.Dropdown(
            self, "Select Cooling:", self.coolings, self.do_nothing, 2, 2
        )
        self.fans_dropdown = PCDIYHelperApp.Dropdown(
            self, "Select Fans:", self.fans, self.do_nothing, 3, 2
        )
        self.psu_dropdown = PCDIYHelperApp.Dropdown(
            self, "Select PSU:", self.psus, self.do_nothing, 4, 2
        )
        self.case_dropdown = PCDIYHelperApp.Dropdown(
            self, "Select Case:", self.cases, self.do_nothing, 5, 2
        )

        # Updaters
        self.motherboard_updater = PCDIYHelperApp.Updater(
            self.cpus, self.cpu_dropdown, self.motherboard_dropdown
        )
        self.cpu_updater = PCDIYHelperApp.Updater(
            self.gpus, self.gpu_dropdown, self.cpu_dropdown, self.motherboard_updater
        )

        # Set update functions for dropdowns
        self.gpu_dropdown.menu.bind("<<ComboboxSelected>>", self.cpu_updater.update)
        self.cpu_dropdown.menu.bind(
            "<<ComboboxSelected>>", self.motherboard_updater.update
        )

        # Button to display selected components
        build_button = ttk.Button(
            self,
            text="Build PC",
            command=self.display_selected_components,
            style="TButton",
        )
        build_button.grid(row=0, column=4, pady=10, padx=30)

        # Text box to display selected components
        self.result_text = tk.Text(self, height=30, width=100)  # Adjusted size
        self.result_text.grid(row=1, rowspan=5, column=4, pady=10, padx=30)

    def display_selected_components(self):
        gpu = self.gpu_dropdown.var.get()
        cpu = self.cpu_dropdown.var.get()
        motherboard = self.motherboard_dropdown.var.get()
        ram = self.ram_dropdown.var.get()
        ssd = self.ssd_dropdown.var.get()
        cooling = self.cooling_dropdown.var.get()
        fans = self.fans_dropdown.var.get()
        psu = self.psu_dropdown.var.get()
        case = self.case_dropdown.var.get()
        result = f"GPU: {gpu}\nCPU: {cpu}\nMotherboard\n{motherboard}\nRAM: {ram}\nSSD: {ssd}\nCooling: {cooling}\nFans: {fans}\nPSU: {psu}\nCase: {case}."
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

        # Calculate total price and price decomposition
        total_price = 0
        price_decomposition = []
        categories = [
            "GPU",
            "CPU",
            "Motherboard",
            "RAM",
            "SSD",
            "Cooling",
            "Fans",
            "PSU",
            "Case",
        ]
        dropdowns = [
            self.gpu_dropdown,
            self.cpu_dropdown,
            self.motherboard_dropdown,
            self.ram_dropdown,
            self.ssd_dropdown,
            self.cooling_dropdown,
            self.fans_dropdown,
            self.psu_dropdown,
            self.case_dropdown,
        ]

        for category, dropdown in zip(categories, dropdowns):
            name = dropdown.var.get()
            price = self.price_manager.get_price(category, name)
            total_price += price

        for category, dropdown in zip(categories, dropdowns):
            name = dropdown.var.get()
            price = self.price_manager.get_price(category, name)
            percent = (price / total_price) * 100 if total_price > 0 else 0
            price_decomposition.append(f"{name}: ${price} ({percent:.2f}%)")

        result += (
            f"\n\n{'=' * 50}\n\nTotal Price: ${total_price}\n\nPrice Decomposition:\n"
            + "\n".join(price_decomposition)
        )
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

    def do_nothing(self, event):
        pass


def main():
    app = PCDIYHelperApp()
    app.mainloop()


if __name__ == "__main__":
    main()

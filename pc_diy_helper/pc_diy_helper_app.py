import tkinter as tk
from tkinter import ttk
import json
import sys
import getpass

sys.path.append(f"/Users/{getpass.getuser()}/git/mhli971/PC-DIY-Helper/")


class PCDIYHelperApp(tk.Tk):
    class Dropdown:
        # Do not change anything here, all default
        def __init__(self, master, label_text, options, update_func, row, column):
            self.label = ttk.Label(master, text=label_text)
            self.label.grid(row=row, column=column, pady=5, padx=5)
            self.var = tk.StringVar(master)
            if options != []:
                self.var.set(options[0])  # set the default option
            else:
                self.var.set("")
            self.menu = ttk.Combobox(master, textvariable=self.var, values=options)
            self.menu.grid(row=row, column=column + 1, pady=5, padx=5)
            self.menu.bind("<<ComboboxSelected>>", update_func)

    class VersionManager:
        def __init__(self, version_config):
            with open(version_config) as f:
                self.version_dict = json.load(f)

        def get_versions(self, model: str) -> dict:
            # model could be RTX 4090, could be PSU
            # returns a dict of versions with reference prices
            return self.version_dict.get(model, {})

        def get_version_price(self, model, version):
            return self.get_versions(model).get(version, 0)

    class ModelUpdater:
        def __init__(
            self, dependent_dict, prev_dropdown, cur_dropdown, next_model_updater=None
        ):
            self.dependent_dict = dependent_dict
            self.prev_dropdown = prev_dropdown
            self.cur_dropdown = cur_dropdown
            self.next_model_updater = next_model_updater

        def update_model_dropdown(self, event):
            prev_model = self.prev_dropdown.var.get()
            dependent_ls = self.dependent_dict.get(prev_model, [])
            self.cur_dropdown.var.set(dependent_ls[0])  # set the default option
            self.cur_dropdown.menu["values"] = dependent_ls
            # chain the updates
            if self.next_model_updater is not None:
                self.next_model_updater.update_model_dropdown(event=None)

        def bind_update(self):
            self.prev_dropdown.menu.bind(
                "<<ComboboxSelected>>", lambda event: self.update_model_dropdown(event)
            )

    class VersionUpdater:
        def __init__(self, model_dropdown, version_dropdown, version_manager):
            self.model_dropdown = model_dropdown
            self.version_dropdown = version_dropdown
            self.version_manager = version_manager

        def update_version_dropdown(self, event):
            model = self.model_dropdown.var.get()
            version_ls = list(self.version_manager.get_versions(model).keys())
            self.version_dropdown.var.set(version_ls[0])  # set the default option
            self.version_dropdown.menu["values"] = version_ls
            self.version_dropdown.label[
                "text"
            ] = f"Select a specific version for {model}:"

        def bind_update(self):
            # event must be passed in
            self.model_dropdown.menu.bind(
                "<<ComboboxSelected>>",
                lambda event: self.update_version_dropdown(event),
            )

    class CombinedUpdater:
        def __init__(self, model_updater, version_updater):
            self.model_updater = model_updater
            self.version_updater = version_updater

        def bind_update(self):
            self.version_updater.model_dropdown.menu.bind(
                "<<ComboboxSelected>>", self.wrapper_function
            )

        def wrapper_function(self, event):
            if self.model_updater is not None:
                self.model_updater.update_model_dropdown(event)
            self.version_updater.update_version_dropdown(event)

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("PC DIY Helper")
        self.geometry("2500x600")

        # Load configuration
        with open("pc_diy_helper/dependents.json") as f:
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

        # Managers
        # self.price_manager = PCDIYHelperApp.PriceManager("pc_diy_helper/versions.json")
        self.version_manager = PCDIYHelperApp.VersionManager(
            "pc_diy_helper/versions.json"
        )

        # Dropdowns
        self.gpu_dropdown = PCDIYHelperApp.Dropdown(
            self, "Select GPU:", list(self.gpus.keys()), None, 0, 0
        )
        self.gpu_version_dropdown = PCDIYHelperApp.Dropdown(
            self,
            f"Select a specific model for GPU:",
            [],
            None,
            0,
            4,
        )
        self.cpu_dropdown = PCDIYHelperApp.Dropdown(
            self, "Select CPU:", self.gpus[self.gpu_dropdown.var.get()], None, 1, 0
        )
        self.cpu_version_dropdown = PCDIYHelperApp.Dropdown(
            self,
            f"Select a specific model for CPU:",
            [],
            None,
            1,
            4,
        )
        self.motherboard_dropdown = PCDIYHelperApp.Dropdown(
            self,
            "Select Motherboard:",
            self.cpus.get(self.cpu_dropdown.var.get(), []),
            None,
            2,
            0,
        )
        self.motherboard_version_dropdown = PCDIYHelperApp.Dropdown(
            self,
            f"Select a specific model for Motherboard:",
            [],
            None,
            2,
            4,
        )
        self.ram_dropdown = PCDIYHelperApp.Dropdown(
            self, "Select RAM:", self.rams, self.do_nothing, 0, 2
        )
        self.ram_version_dropdown = PCDIYHelperApp.Dropdown(
            self,
            f"Select a specific model for RAM:",
            [],
            None,
            3,
            4,
        )
        self.ssd_dropdown = PCDIYHelperApp.Dropdown(
            self, "Select SSD:", self.ssds, self.do_nothing, 1, 2
        )
        self.ssd_version_dropdown = PCDIYHelperApp.Dropdown(
            self,
            f"Select a specific model for SSD:",
            [],
            None,
            4,
            4,
        )
        self.cooling_dropdown = PCDIYHelperApp.Dropdown(
            self, "Select Cooling:", self.coolings, self.do_nothing, 2, 2
        )
        self.cooling_version_dropdown = PCDIYHelperApp.Dropdown(
            self,
            "Select a specific model for Cooling:",
            [],
            None,
            5,
            4,
        )

        self.fans_dropdown = PCDIYHelperApp.Dropdown(
            self, "Select Fans:", self.fans, self.do_nothing, 3, 2
        )
        self.fans_version_dropdown = PCDIYHelperApp.Dropdown(
            self,
            "Select a specific model for Fans:",
            [],
            None,
            0,
            6,
        )

        self.psu_dropdown = PCDIYHelperApp.Dropdown(
            self, "Select PSU:", self.psus, self.do_nothing, 4, 2
        )
        self.psu_version_dropdown = PCDIYHelperApp.Dropdown(
            self,
            "Select a specific model for PSU:",
            [],
            None,
            1,
            6,
        )

        self.case_dropdown = PCDIYHelperApp.Dropdown(
            self, "Select Case:", self.cases, self.do_nothing, 5, 2
        )
        self.case_version_dropdown = PCDIYHelperApp.Dropdown(
            self,
            "Select a specific model for Case:",
            [],
            None,
            2,
            6,
        )

        # Updaters
        self.motherboard_updater = PCDIYHelperApp.ModelUpdater(
            self.cpus, self.cpu_dropdown, self.motherboard_dropdown
        )
        self.cpu_updater = PCDIYHelperApp.ModelUpdater(
            self.gpus, self.gpu_dropdown, self.cpu_dropdown, self.motherboard_updater
        )

        # VersionUpdaters
        self.gpu_version_updater = PCDIYHelperApp.VersionUpdater(
            self.gpu_dropdown, self.gpu_version_dropdown, self.version_manager
        )
        self.cpu_version_updater = PCDIYHelperApp.VersionUpdater(
            self.cpu_dropdown, self.cpu_version_dropdown, self.version_manager
        )
        self.motherboard_version_updater = PCDIYHelperApp.VersionUpdater(
            self.motherboard_dropdown,
            self.motherboard_version_dropdown,
            self.version_manager,
        )

        # CombinedUpdaters
        self.gpu_combined_updater = PCDIYHelperApp.CombinedUpdater(
            self.cpu_updater, self.gpu_version_updater
        )
        self.cpu_combined_updater = PCDIYHelperApp.CombinedUpdater(
            self.motherboard_updater, self.cpu_version_updater
        )
        self.motherboard_combined_updater = PCDIYHelperApp.CombinedUpdater(
            None, self.motherboard_version_updater
        )

        # Other VersionUpdaters
        self.ram_version_updater = PCDIYHelperApp.VersionUpdater(
            self.ram_dropdown, self.ram_version_dropdown, self.version_manager
        )

        self.ssd_version_updater = PCDIYHelperApp.VersionUpdater(
            self.ssd_dropdown, self.ssd_version_dropdown, self.version_manager
        )

        self.cooling_version_updater = PCDIYHelperApp.VersionUpdater(
            self.cooling_dropdown, self.cooling_version_dropdown, self.version_manager
        )

        self.fans_version_updater = PCDIYHelperApp.VersionUpdater(
            self.fans_dropdown, self.fans_version_dropdown, self.version_manager
        )

        self.psu_version_updater = PCDIYHelperApp.VersionUpdater(
            self.psu_dropdown, self.psu_version_dropdown, self.version_manager
        )

        self.case_version_updater = PCDIYHelperApp.VersionUpdater(
            self.case_dropdown, self.case_version_dropdown, self.version_manager
        )

        # UPDATE ALL
        self.gpu_combined_updater.bind_update()
        self.cpu_combined_updater.bind_update()
        self.motherboard_combined_updater.bind_update()
        self.ram_version_updater.bind_update()
        self.ssd_version_updater.bind_update()
        self.cooling_version_updater.bind_update()
        self.fans_version_updater.bind_update()
        self.psu_version_updater.bind_update()
        self.case_version_updater.bind_update()

        # Button to display selected components
        build_button = ttk.Button(
            self,
            text="Build PC",
            command=self.report_build_and_price,
            style="TButton",
        )
        build_col = 8
        build_button.grid(row=0, column=build_col, pady=10, padx=30)

        # Text box to display selected components
        self.result_text = tk.Text(self, height=30, width=100)  # Adjusted size
        self.result_text.grid(row=1, rowspan=5, column=build_col, pady=10, padx=30)

    def report_build_and_price(self):
        gpu_version = self.gpu_version_dropdown.var.get()
        cpu_version = self.cpu_version_dropdown.var.get()
        motherboard_version = self.motherboard_version_dropdown.var.get()
        ram_version = self.ram_version_dropdown.var.get()
        ssd_version = self.ssd_version_dropdown.var.get()
        cooling_version = self.cooling_version_dropdown.var.get()
        fans_version = self.fans_version_dropdown.var.get()
        psu_version = self.psu_version_dropdown.var.get()
        case_version = self.case_version_dropdown.var.get()

        gpu = self.gpu_dropdown.var.get()
        cpu = self.cpu_dropdown.var.get()
        motherboard = self.motherboard_dropdown.var.get()
        ram = self.ram_dropdown.var.get()
        ssd = self.ssd_dropdown.var.get()
        cooling = self.cooling_dropdown.var.get()
        fans = self.fans_dropdown.var.get()
        psu = self.psu_dropdown.var.get()
        case = self.case_dropdown.var.get()

        result = "Selected Components:\n"
        result += f"GPU: {gpu_version}\n"
        result += f"CPU: {cpu_version}\n"
        result += f"Motherboard: {motherboard_version}\n"
        result += f"RAM: {ram_version}\n"
        result += f"SSD: {ssd_version}\n"
        result += f"Cooling: {cooling_version}\n"
        result += f"Fans: {fans_version}\n"
        result += f"PSU: {psu_version}\n"
        result += f"Case: {case_version}.\n"
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

        # Calculate total price and price decomposition
        total_price = 0
        price_decomposition = []
        models = [gpu, cpu, motherboard, ram, ssd, cooling, fans, psu, case]
        versions = (
            gpu_version,
            cpu_version,
            motherboard_version,
            ram_version,
            ssd_version,
            cooling_version,
            fans_version,
            psu_version,
            case_version,
        )

        price_ls = [
            self.version_manager.get_version_price(model, version)
            for model, version in zip(models, versions)
        ]
        total_price = sum(price_ls)
        for version, price in zip(versions, price_ls):
            percent = (price / total_price) * 100 if total_price > 0 else 0
            price_decomposition.append(f"{version}: ${price} ({percent:.2f}%)")

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

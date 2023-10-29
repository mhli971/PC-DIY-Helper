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
        self.version_dropdown.label["text"] = f"Select a specific version for {model}:"

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

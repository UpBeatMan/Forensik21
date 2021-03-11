from Model.FirefoxModel.Cache.cache2entries import Cache2Handler
from importlib import import_module
from Model.log_util import log_message


class DataSourcesCache:
    def __init__(self, profile_path: str, cache_path: str):
        self.sources = {}
        source_names = []

        source_names.append(["Model.FirefoxModel.Cache.cache2entries", "Cache2Handler"])

        for source_name in source_names:
            module_name = source_name[0]
            class_name = source_name[1]

            try:
                module = import_module(module_name)
                Class_ = getattr(module, class_name)
                instance = Class_(profile_path=profile_path, cache_path=cache_path)
            except Exception as e:
                message = "Fehler in SQlite, Klasse " + str(class_name) + ": " + str(e) + ". Überspringe"
                self.log_message(message, "info")
                continue
            self.sources[class_name] = instance

    def get_data(self):
        data = {}
        for source in self.sources:
            try:
                data[source] = self.sources[source].get_all_id_ordered()
            except Exception as e:
                log_message("Fehler in " + source + ": " + str(e), "info")

        return data

    def get_data_header(self):
        data_header = []
        for source in self.sources:
            data_header.append(source.attr_names)
        return data_header

    def get_names(self):
        name_list = []
        for source in self.sources:
            name_list.append(source.name)
        return name_list

    def rollback(self, name):
        """Undo changes for only one source or all"""
        if name:
            try:
                self.sources[name].rollback()
            except:
                self.log_message("Fehler beim Rollback von: " + str(name), "error")
        else:
            for source in self.sources:
                try:
                    self.sources[source].rollback()
                except:
                    self.log_message("Fehler beim Rollback von: " + str(source), "error")


    def commit(self, name):
        """Save changes for only one source or all"""
        if name:
            try:
                self.sources[name].commit()
            except:
                self.log_message("Fehler beim Speichern von: "  + str(name), "error")
        else:
            for source in self.sources:
                try:
                    self.sources[source].commit()
                except:
                    self.log_message("Fehler beim Speichern von: "  + str(source), "error")

    def close(self):
        """Close all connections"""
        for source in self.sources:
            self.sources[source].close()

    def log_message(self, message, lvl):
        pub.sendMessage("logging", message=message, lvl=lvl)
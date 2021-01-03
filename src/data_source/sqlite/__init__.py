from importlib import import_module


class DataSourcesSQLite:
    def __init__(self, profile_path: str, cache_path: str):
        self.sources = []
        source_names = []

        # Create list of module names and handlers, that we need
        source_names.append(["data_source.sqlite.content_prefs", "ContentPrefHandler"])
        source_names.append(["data_source.sqlite.cookie", "CookieHandler"])
        source_names.append(["data_source.sqlite.favicons", "FaviconsHandler"])
        source_names.append(["data_source.sqlite.formhistory", "FormHistoryHandler"])
        source_names.append(["data_source.sqlite.permissions", "PermissionHandler"])
        source_names.append(["data_source.sqlite.places", "HistoryVisitHandler"])
        source_names.append(["data_source.sqlite.places", "BookmarkHandler"])

        for source_name in source_names:
            module_name = source_name[0]
            class_name = source_name[1]

            # With import_module it is possible to create class handler. If it fails we can skip it.
            # If successfully add it to the list
            try:
                module = import_module(module_name)
                Class_ = getattr(module, class_name)
                instance = Class_(profile_path=profile_path, cache_path=cache_path)
            except Exception as e:
                print(
                    "Fehler in Datenquelle SQlite, Modul %s, Klasse %s: %s. Überspringe"
                    % (module_name, class_name, e)
                )
                continue
            self.sources.append(instance)

    def get_data(self):
        """Collect data from hanlders"""
        data = []
        for source in self.sources:
            data.append(source.get_all_id_ordered())

        return data

    def get_data_header(self):
        """Collect names of the fields from the data"""
        data_header = []
        for source in self.sources:
            data_header.append(source.attr_names)
        return data_header

    def get_names(self):
        """Collect names of the classes"""
        name_list = []
        for source in self.sources:
            name_list.append(source.name)
        return name_list

    def rollback(self, name):
        """Undo changes for only one source or all"""
        if name is None:
            for source in self.sources:
                source.rollback()
        else:
            for source in self.sources:
                if source.name == name:
                    source.rollback()

    def commit(self, name):
        """Save changes for only one source or all"""
        if name is None:
            for source in self.sources:
                source.commit()
        else:
            for source in self.sources:
                if source.name == name:
                    source.commit()

    def close(self):
        """Close all connections"""
        for source in self.sources:
            source.close()

from Model.FirefoxModel.JSON import DataSourcesJSON
from Model.FirefoxModel.SQLite import DataSourcesSQLite
from Model.FirefoxModel.Cache import DataSourcesCache

class FirefoxModel:

    def __init__(self, profile_path: str = None, cache_path: str = None):
        if profile_path is None:
            return

        if cache_path is None:
            cache_path = profile_path

        self.data_list = []
        self.sources = {}

        self.sources["SQLite"] = DataSourcesSQLite(profile_path, cache_path)
        self.sources["JSON"] = DataSourcesJSON(profile_path, cache_path)
        self.sources["Cache"] = DataSourcesCache(cache_path, cache_path)

        #

    def get_data(self):
        for source in self.sources:
            for data_list in self.sources[source].get_data():
                self.data_list.append(data_list)

        return self.data_list
    
    def get_history(self):
        return self.sources["SQLite"].get_history()

    def get_data_header(self):
        data_header = []
        for source in self.sources:
            for header in source.get_data_header():
                data_header.append(header)

        return data_header

    def get_names(self):
        name_list = []
        for source in self.sources:
            for name in source.get_names():
                name_list.append(name)
        return name_list

    def rollback(self, name: str = None):
        for source in self.sources:
            source.rollback(name)

    def commit(self, name: str = None):
        for source in self.sources:
            source.commit(name)

    def init_obj(self, list_=None):
        if list_ is None:
            return

        for data in list_:
            for obj in data:
                obj.init()

    def close(self):
        for source in self.sources:
            source.close()
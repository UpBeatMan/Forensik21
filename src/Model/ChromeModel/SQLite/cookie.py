from sqlalchemy import Column, Integer, String, orm

from Model.ChromeModel.SQLite.base import *

ID = "ID"
HOST = "Host"
NAME = "Name"
PATH = "Pfad"
EXPIRYAT = "Ungueltig ab"
LASTACCESSAT = "Letzter Zugriff"
CREATEDAT = "Erstellt am"


class Cookie(BaseSession, BaseSQLiteClass):
    __tablename__ = "cookies"

    host = Column("host_key", String)
    name = Column("name", String)
    path = Column("path", String)
    expiry_timestamp = Column("expires_utc", Integer)
    last_accessed_timestamp = Column("last_access_utc", Integer)
    creation_timestamp = Column("creation_utc", Integer, primary_key=True)

    @orm.reconstructor
    def init(self):
        self.attr_list = []
        self.attr_list.append(BaseAttribute(HOST, OTHER, self.host))
        self.attr_list.append(BaseAttribute(NAME, OTHER, self.name))
        self.attr_list.append(BaseAttribute(PATH, OTHER, self.path))
        self.attr_list.append(BaseAttribute(EXPIRYAT, DT_WEBKIT, self.expiry_timestamp))
        self.attr_list.append(BaseAttribute(LASTACCESSAT, DT_WEBKIT, self.last_accessed_timestamp))
        self.attr_list.append(BaseAttribute(CREATEDAT, DT_WEBKIT, self.creation_timestamp))

    def update(self):
        for attr in self.attr_list:
            if attr.name == EXPIRYAT:
                self.expiry_timestamp = attr.timestamp
            elif attr.name == LASTACCESSAT:
                self.last_accessed_timestamp = attr.timestamp
            elif attr.name == CREATEDAT:
                self.creation_timestamp = attr.timestamp

        self.init()


class CookieHandler(BaseSQliteHandler):
    name = "Cookies"

    attr_names = [ID, HOST, PATH, EXPIRYAT, LASTACCESSAT, CREATEDAT]

    def __init__(
        self,
        profile_path: str,
        file_name: str = "Cookies",
        logging: bool = False,
    ):
        super().__init__(profile_path, file_name, logging)

    def get_all_id_ordered(self):
        query = self.session.query(Cookie)
        return query.all()
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

__version__ = '0.1.0'

# global variables
DT_MILLI_ZEROED_MICRO = "datetime_milliseconds_zeroed_microseconds"
IDENTIFIER = ""

# objects
Base = declarative_base()


class FormHistory(Base):
    ID = "ID"
    FIELDNAME = "Feldname"
    VALUE = "Eingabewert"
    FIRSTUSED = "Zum ersten mal verwendet"
    LASTUSED = "Zuletzt genutzt"

    __tablename__ = 'moz_formhistory'  # HISTORY

    id = Column("id", Integer, primary_key=True)
    field_name = Column("fieldname", String)
    value = Column("value", String)
    first_used_timestamp = Column("firstUsed", Integer)
    last_used_timestamp = Column("lastUsed", Integer)

    IDENTIFIER = id

    # @orm.reconstructor - throws error, not knowing orm name
    def __init__(self):
        self.attr_list = []
        self.attr_list.append(BaseAttribute(FIELDNAME, OTHER, self.field_name))
        self.attr_list.append(BaseAttribute(VALUE, OTHER, self.value))
        self.attr_list.append(
            BaseAttribute(FIRSTUSED, DT_MILLI_ZEROED_MICRO, self.first_used_timestamp)
        )
        self.attr_list.append(
            BaseAttribute(LASTUSED, DT_MILLI_ZEROED_MICRO, self.last_used_timestamp)
        )

    def __repr__(self):
        return "<FormHistory(field_name='%s', value='%s', first_used_timestamp='%d', last_used_timestamp='%d')>" % (
            self.field_name, self.value, self.first_used_timestamp, self.last_used_timestamp)

    def get_count(self, q):
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count
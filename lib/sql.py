import json
from contextlib import contextmanager

from sqlalchemy import INTEGER, String, Column, create_engine, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()

with open("config.json") as fp:
    data = json.load(fp)["sql"]


class DataTable(Base):
    __tablename__ = 'partner'
    server_id = Column(BigInteger, primary_key=True, autoincrement=False)
    text = Column(String(2000))
    author = Column(String(500))
    img_url = Column(String(500))
    count = Column(INTEGER, nullable=False)
    channel_id = Column(BigInteger)
    server_invite = Column(String(200))

    def __init__(self, server_id, text, author, img_url, count, channel_id, server_invite):
        self.server_id = server_id
        self.text = text
        self.author = author
        self.img_url = img_url
        self.count = count
        self.channel_id = channel_id
        self.server_invite = server_invite

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])


def init_db(uri):
    engine = create_engine(uri, pool_recycle=3600, pool_pre_ping=True, pool_use_lifo=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,
                                             bind=engine))
    Base.metadata.create_all(bind=engine)
    return db_session




@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = init_db(f'mysql+pymysql://{data["user"]}:{data["password"]}@localhost/{data["database"]}')
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

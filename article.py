from sqlalchemy import Column, String, Integer
from base import Base


class Article(Base):
    __tablename__ = 'articles'

    id = Column(String, primary_key=True)
    body = Column(String)
    host = Column(String)
    title = Column(String)
    site_id = Column(String)
    n_tokens_title = Column(Integer)
    n_tokens_body = Column(Integer)
    url = Column(String, unique=True)

    def __init__(self, uid, body, host, title, site_id, n_tokens_title, n_tokens_body, url):
        self.id = uid
        self.body = body
        self.host = host
        self.title = title
        self.site_id = site_id
        self.n_tokens_title = n_tokens_title
        self.n_tokens_body = n_tokens_body
        self.url = url

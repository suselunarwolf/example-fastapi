from enum import unique
from time import timezone
#from tkinter import CASCADE
import sys
if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk
from tk import CASCADE
from xmlrpc.client import Boolean

from psycopg2 import Timestamp
from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer,primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default='True',nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False , server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete=CASCADE),nullable = False)
    owner = relationship('User')

class User(Base):
    __tablename__ = "users"
    email = Column(String,nullable = False,unique = True)
    password = Column(String,nullable = False)
    id = Column(Integer,primary_key = True, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False , server_default=text('now()'))


class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(Integer,ForeignKey("posts.id",ondelete=CASCADE),primary_key=True,nullable=False)
    user_id = Column(Integer,ForeignKey("users.id",ondelete=CASCADE),primary_key=True,nullable=False)
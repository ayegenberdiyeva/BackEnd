from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, func
# from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key= True, nullable= False)
    title = Column(String, nullable= False)
    content = Column(String, nullable= False)
    status = Column(Boolean, server_default= 'True', nullable= False)
    created_at = Column(TIMESTAMP(timezone= True), nullable= False, server_default= func.now())

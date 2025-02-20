from pydantic import ConfigDict
from sqlalchemy import Column, ForeignKey, Integer, String

from source.database_service.database_config import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    from_user_uid = Column(String, ForeignKey("users.user_uid"))
    to_user_uid = Column(String, ForeignKey("users.user_uid"))
    reply_to_message = Column(Integer, nullable=True)
    body = Column(String, nullable=False)

    model_config = ConfigDict(from_attributes=True)

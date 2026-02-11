# import uuid
# from datetime import datetime

# from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
# from sqlalchemy.dialects.sqlite import CHAR
# from sqlalchemy.orm import relationship

# from app.db import Base


# def generate_uuid():
#     return str(uuid.uuid4())


# class Slot(Base):
#     __tablename__ = "slots"

#     id = Column(CHAR(36), primary_key=True, default=generate_uuid)
#     code = Column(String(32), unique=True, nullable=False, index=True)
#     capacity = Column(Integer, nullable=False)
#     current_item_count = Column(Integer, nullable=False, default=0)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     items = relationship("Item", back_populates="slot", cascade="save-update, merge")


# class Item(Base):
#     __tablename__ = "items"

#     id = Column(CHAR(36), primary_key=True, default=generate_uuid)
#     name = Column(String(255), nullable=False)
#     price = Column(Integer, nullable=False)
#     slot_id = Column(CHAR(36), ForeignKey("slots.id", ondelete="SET NULL"), nullable=True)
#     quantity = Column(Integer, nullable=False, default=0)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     slot = relationship("Slot", back_populates="items")



from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Slot(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(32), unique=True, nullable=False, index=True)
    capacity = Column(Integer, nullable=False)
    current_item_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = relationship("Item", back_populates="slot", cascade="save-update, merge")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    slot_id = Column(Integer, ForeignKey("slots.id", ondelete="SET NULL"), nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    slot = relationship("Slot", back_populates="items")

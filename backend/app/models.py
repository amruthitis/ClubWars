from sqlalchemy import Column, Integer, Float, String, ForeignKey
from .database import Base

class Container(Base):
    __tablename__ = "containers"

    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String)
    destination = Column(String)
    departure_date = Column(String)
    total_capacity = Column(Float)
    booked_capacity = Column(Float)
    cost = Column(Float)

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    container_id = Column(Integer, ForeignKey("containers.id"))
    volume = Column(Float)
    booking_date = Column(String)

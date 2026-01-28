from sqlalchemy.orm import Session
from datetime import datetime
from .models import Container, Booking

def get_feasible_containers(db: Session, origin, destination, date, volume):
    return db.query(Container).filter(
        Container.origin == origin,
        Container.destination == destination,
        Container.departure_date >= date,
        (Container.total_capacity - Container.booked_capacity) >= volume
    ).all()

def reserve_space(db: Session, container_id: int, volume: float):
    container = db.query(Container).filter(Container.id == container_id).first()
    if not container:
        return None

    available = container.total_capacity - container.booked_capacity
    if volume > available:
        return None

    container.booked_capacity += volume

    booking = Booking(
        container_id=container_id,
        volume=volume,
        booking_date=str(datetime.utcnow())
    )

    db.add(booking)
    db.commit()
    db.refresh(container)
    return booking

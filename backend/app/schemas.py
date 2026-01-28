from pydantic import BaseModel

class ShipmentRequest(BaseModel):
    origin: str
    destination: str
    departure_date: str
    volume: float

class ReservationRequest(BaseModel):
    container_id: int
    volume: float

class ContainerResponse(BaseModel):
    container_id: int
    available_capacity: float
    reliability_score: float
    cost: float
    final_score: float

class BookingResponse(BaseModel):
    id: int
    container_id: int
    volume: float
    booking_date: str

class ProviderContainerResponse(BaseModel):
    container_id: int
    route: str
    total_capacity: float
    booked_capacity: float
    utilization_percent: float
    cost: float

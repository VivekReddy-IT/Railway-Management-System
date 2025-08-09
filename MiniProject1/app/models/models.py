from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Numeric, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base

class Train(Base):
    __tablename__ = "Trains"

    train_id = Column(String(20), primary_key=True)
    train_name = Column(String(100), nullable=False)
    train_type = Column(Enum('express', 'passenger', 'special', 'devotional'), nullable=False)
    total_capacity = Column(Integer, nullable=False)
    frequency = Column(Enum('daily', 'weekly', 'bi-weekly', 'special'), nullable=False)
    special_attributes = Column(String(255))

    # Define relationships later as needed
    # coaches = relationship("Coach", back_populates="train")
    # train_schedules = relationship("TrainSchedule", back_populates="train")
    # operational_status = relationship("OperationalStatus", back_populates="train")
    # delay_patterns = relationship("DelayPattern", back_populates="train")
    # seat_inventory = relationship("SeatInventory", back_populates="train")
    # quota_allocation = relationship("QuotaAllocation", back_populates="train")
    # dynamic_pricing = relationship("DynamicPricing", back_populates="train")
    # crew_assignments = relationship("CrewAssignment", back_populates="train")

class Station(Base):
    __tablename__ = "Stations"

    station_code = Column(String(10), primary_key=True)
    station_name = Column(String(100), nullable=False)
    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))
    total_platforms = Column(Integer, nullable=False)
    facilities = Column(Text)

    # Define relationships later as needed
    # platforms = relationship("Platform", back_populates="station")
    # route_stations = relationship("RouteStation", back_populates="station")
    # station_schedules = relationship("StationSchedule", back_populates="station")
    # delay_patterns = relationship("DelayPattern", back_populates="station")
    # ticket_collectors = relationship("TicketCollector", back_populates="station")

class Reservation(Base):
    __tablename__ = "Reservations"

    pnr = Column(String(20), primary_key=True)
    booking_date = Column(DateTime, server_default=func.now())
    train_id = Column(String(20), ForeignKey("Trains.train_id"), nullable=False)
    journey_date = Column(DateTime, nullable=False)
    source_station = Column(String(10), ForeignKey("Stations.station_code"), nullable=False)
    destination_station = Column(String(10), ForeignKey("Stations.station_code"), nullable=False)
    booking_status = Column(Enum('confirmed', 'waitlisted', 'RAC', 'cancelled'), nullable=False)
    total_fare = Column(Numeric(10, 2), nullable=False)
    quota_id = Column(Integer, ForeignKey("Quotas.quota_id"))
    booking_agent = Column(String(50))
    booking_flexibility = Column(Enum('Rigid', 'Flexible', 'Super Flexible'), default='Rigid')
    alternative_contact = Column(String(20))
    special_instructions = Column(Text)

    # Define relationships later as needed
    # train = relationship("Train")
    # source_station_rel = relationship("Station", foreign_keys=[source_station])
    # destination_station_rel = relationship("Station", foreign_keys=[destination_station])
    # quota = relationship("Quota")
    # reservation_passengers = relationship("ReservationPassenger", back_populates="reservation")
    # issue_tickets = relationship("IssueTicket", back_populates="reservation")
    # reschedule_options = relationship("RescheduleOption", back_populates="original_reservation") 
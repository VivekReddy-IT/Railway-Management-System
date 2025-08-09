from app import db
from datetime import datetime
from enum import Enum

class TrainType(Enum):
    EXPRESS = 'express'
    PASSENGER = 'passenger'
    SPECIAL = 'special'
    DEVOTIONAL = 'devotional'

class Frequency(Enum):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    BI_WEEKLY = 'bi-weekly'
    SPECIAL = 'special'

class CoachType(Enum):
    SLEEPER = 'sleeper'
    AC1 = 'ac1'
    AC2 = 'ac2'
    AC3 = 'ac3'
    GENERAL = 'general'
    CHAIR = 'chair'
    EXECUTIVE = 'executive'

class DayOfWeek(Enum):
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'
    SPECIAL = 'Special'

class Gender(Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'

class SeatPreference(Enum):
    WINDOW = 'window'
    AISLE = 'aisle'
    LOWER = 'lower'
    MIDDLE = 'middle'
    UPPER = 'upper'
    SIDE_LOWER = 'side_lower'
    SIDE_UPPER = 'side_upper'

class FlexibilityPreference(Enum):
    RIGID = 'Rigid'
    FLEXIBLE = 'Flexible'
    SUPER_FLEXIBLE = 'Super Flexible'

class BookingStatus(Enum):
    CONFIRMED = 'confirmed'
    WAITLISTED = 'waitlisted'
    RAC = 'RAC'
    CANCELLED = 'cancelled'

class IssueType(Enum):
    BOOKING_PROBLEM = 'booking_problem'
    CANCELLATION = 'cancellation'
    RESCHEDULING = 'rescheduling'
    REFUND = 'refund'
    COMPLAINT = 'complaint'
    MEDICAL_EMERGENCY = 'medical_emergency'
    TRAVEL_RESTRICTION = 'travel_restriction'
    TECHNICAL_ISSUE = 'technical_issue'
    OVERBOOKING = 'overbooking'

class IssueStatus(Enum):
    PENDING = 'pending'
    UNDER_REVIEW = 'under_review'
    IN_PROGRESS = 'in_progress'
    RESOLVED = 'resolved'
    REJECTED = 'rejected'
    CLOSED = 'closed'

class IssuePriority(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'

class ResolutionType(Enum):
    REFUND = 'refund'
    REBOOK = 'rebook'
    RESCHEDULE = 'reschedule'
    ALTERNATE_TRAIN = 'alternate_train'
    COMPENSATION = 'compensation'
    OTHER = 'other'

class CrewType(Enum):
    DRIVER = 'driver'
    ASSISTANT_DRIVER = 'assistant_driver'
    GUARD = 'guard'
    CATERING = 'catering'
    CLEANER = 'cleaner'
    SECURITY = 'security'

class Train(db.Model):
    __tablename__ = 'trains'
    
    train_id = db.Column(db.String(20), primary_key=True)
    train_name = db.Column(db.String(100), nullable=False)
    train_type = db.Column(db.Enum(TrainType), nullable=False)
    total_capacity = db.Column(db.Integer, nullable=False)
    frequency = db.Column(db.Enum(Frequency), nullable=False)
    special_attributes = db.Column(db.String(255))
    
    # Relationships
    coaches = db.relationship('Coach', backref='train', cascade='all, delete-orphan')
    schedules = db.relationship('TrainSchedule', backref='train', cascade='all, delete-orphan')

class Coach(db.Model):
    __tablename__ = 'coaches'
    
    coach_id = db.Column(db.String(20), primary_key=True)
    train_id = db.Column(db.String(20), db.ForeignKey('trains.train_id', ondelete='CASCADE'), nullable=False)
    coach_type = db.Column(db.Enum(CoachType), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    special_features = db.Column(db.String(255))
    maintenance_status = db.Column(db.String(50))

class Station(db.Model):
    __tablename__ = 'stations'
    
    station_code = db.Column(db.String(10), primary_key=True)
    station_name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Numeric(10, 8))
    longitude = db.Column(db.Numeric(11, 8))
    total_platforms = db.Column(db.Integer, nullable=False)
    facilities = db.Column(db.Text)

class Platform(db.Model):
    __tablename__ = 'platforms'
    
    platform_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    station_code = db.Column(db.String(10), db.ForeignKey('stations.station_code', ondelete='CASCADE'), nullable=False)
    platform_number = db.Column(db.Integer, nullable=False)
    platform_type = db.Column(db.String(50))
    capabilities = db.Column(db.Text)
    
    __table_args__ = (
        db.UniqueConstraint('station_code', 'platform_number', name='unique_platform'),
    )

class Route(db.Model):
    __tablename__ = 'routes'
    
    route_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source_station = db.Column(db.String(10), db.ForeignKey('stations.station_code'), nullable=False)
    destination_station = db.Column(db.String(10), db.ForeignKey('stations.station_code'), nullable=False)
    total_distance = db.Column(db.Numeric(8, 2), nullable=False)
    
    # Relationships
    source = db.relationship('Station', foreign_keys=[source_station])
    destination = db.relationship('Station', foreign_keys=[destination_station])

class RouteStation(db.Model):
    __tablename__ = 'route_stations'
    
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id', ondelete='CASCADE'), primary_key=True)
    station_code = db.Column(db.String(10), db.ForeignKey('stations.station_code'), primary_key=True)
    sequence_number = db.Column(db.Integer, nullable=False)
    distance_from_source = db.Column(db.Numeric(8, 2), nullable=False)

class TrainSchedule(db.Model):
    __tablename__ = 'train_schedules'
    
    schedule_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_id = db.Column(db.String(20), db.ForeignKey('trains.train_id', ondelete='CASCADE'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id', ondelete='CASCADE'), nullable=False)
    day_of_operation = db.Column(db.Enum(DayOfWeek), nullable=False)

class StationSchedule(db.Model):
    __tablename__ = 'station_schedules'
    
    schedule_id = db.Column(db.Integer, db.ForeignKey('train_schedules.schedule_id', ondelete='CASCADE'), primary_key=True)
    station_code = db.Column(db.String(10), db.ForeignKey('stations.station_code'), primary_key=True)
    arrival_time = db.Column(db.Time)
    departure_time = db.Column(db.Time)
    platform_id = db.Column(db.Integer, db.ForeignKey('platforms.platform_id'))
    halt_duration = db.Column(db.Integer, default=5)

class DelayPattern(db.Model):
    __tablename__ = 'delay_patterns'
    
    delay_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_id = db.Column(db.String(20), db.ForeignKey('trains.train_id', ondelete='CASCADE'), nullable=False)
    station_code = db.Column(db.String(10), db.ForeignKey('stations.station_code'), nullable=False)
    average_delay = db.Column(db.Integer, nullable=False)
    day_of_week = db.Column(db.Enum(DayOfWeek), nullable=False)
    month = db.Column(db.SmallInteger)
    year = db.Column(db.SmallInteger)
    reason = db.Column(db.String(255))

class Passenger(db.Model):
    __tablename__ = 'passengers'
    
    passenger_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.Enum(Gender))
    address = db.Column(db.Text)
    special_requirements = db.Column(db.Text)

class PassengerPreference(db.Model):
    __tablename__ = 'passenger_preferences'
    
    preference_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    passenger_id = db.Column(db.Integer, db.ForeignKey('passengers.passenger_id', ondelete='CASCADE'), nullable=False)
    seat_preference = db.Column(db.Enum(SeatPreference))
    coach_preference = db.Column(db.Enum(CoachType))
    meal_preference = db.Column(db.String(50))
    flexibility_preference = db.Column(db.Enum(FlexibilityPreference), default=FlexibilityPreference.RIGID)
    flexibility_tolerance = db.Column(db.Integer)

class Quota(db.Model):
    __tablename__ = 'quotas'
    
    quota_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quota_name = db.Column(db.String(50), nullable=False)
    quota_description = db.Column(db.Text)
    priority_level = db.Column(db.Integer, nullable=False)

class Reservation(db.Model):
    __tablename__ = 'reservations'
    
    pnr = db.Column(db.String(20), primary_key=True)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    train_id = db.Column(db.String(20), db.ForeignKey('trains.train_id'), nullable=False)
    journey_date = db.Column(db.Date, nullable=False)
    source_station = db.Column(db.String(10), db.ForeignKey('stations.station_code'), nullable=False)
    destination_station = db.Column(db.String(10), db.ForeignKey('stations.station_code'), nullable=False)
    booking_status = db.Column(db.Enum(BookingStatus), nullable=False)
    total_fare = db.Column(db.Numeric(10, 2), nullable=False)
    quota_id = db.Column(db.Integer, db.ForeignKey('quotas.quota_id'))
    booking_agent = db.Column(db.String(50))
    booking_flexibility = db.Column(db.Enum(FlexibilityPreference), default=FlexibilityPreference.RIGID)
    alternative_contact = db.Column(db.String(20))
    special_instructions = db.Column(db.Text)

class ReservationPassenger(db.Model):
    __tablename__ = 'reservation_passengers'
    
    reservation_passenger_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pnr = db.Column(db.String(20), db.ForeignKey('reservations.pnr', ondelete='CASCADE'), nullable=False)
    passenger_id = db.Column(db.Integer, db.ForeignKey('passengers.passenger_id'), nullable=False)
    seat_number = db.Column(db.String(10))
    coach_id = db.Column(db.String(20), db.ForeignKey('coaches.coach_id'))
    ticket_status = db.Column(db.Enum(BookingStatus), nullable=False)
    waitlist_position = db.Column(db.Integer)
    fare = db.Column(db.Numeric(10, 2), nullable=False)

class SeatInventory(db.Model):
    __tablename__ = 'seat_inventory'
    
    inventory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_id = db.Column(db.String(20), db.ForeignKey('trains.train_id'), nullable=False)
    coach_id = db.Column(db.String(20), db.ForeignKey('coaches.coach_id'), nullable=False)
    journey_date = db.Column(db.Date, nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    waitlist_count = db.Column(db.Integer, default=0)
    rac_count = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('train_id', 'coach_id', 'journey_date', name='unique_inventory'),
    )

class QuotaAllocation(db.Model):
    __tablename__ = 'quota_allocations'
    
    allocation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_id = db.Column(db.String(20), db.ForeignKey('trains.train_id'), nullable=False)
    journey_date = db.Column(db.Date, nullable=False)
    quota_id = db.Column(db.Integer, db.ForeignKey('quotas.quota_id'), nullable=False)
    seats_allocated = db.Column(db.Integer, nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('train_id', 'quota_id', 'journey_date', name='unique_quota_allocation'),
    )

class DynamicPricing(db.Model):
    __tablename__ = 'dynamic_pricing'
    
    pricing_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_id = db.Column(db.String(20), db.ForeignKey('trains.train_id'), nullable=False)
    journey_date = db.Column(db.Date, nullable=False)
    coach_type = db.Column(db.Enum(CoachType), nullable=False)
    base_fare = db.Column(db.Numeric(10, 2), nullable=False)
    dynamic_fare = db.Column(db.Numeric(10, 2), nullable=False)
    reason = db.Column(db.String(255))
    
    __table_args__ = (
        db.UniqueConstraint('train_id', 'coach_type', 'journey_date', name='unique_pricing'),
    )

class OperationalStatus(db.Model):
    __tablename__ = 'operational_status'
    
    status_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_id = db.Column(db.String(20), db.ForeignKey('trains.train_id'), nullable=False)
    journey_date = db.Column(db.Date, nullable=False)
    current_station = db.Column(db.String(10), db.ForeignKey('stations.station_code'))
    next_station = db.Column(db.String(10), db.ForeignKey('stations.station_code'))
    current_status = db.Column(db.String(50), nullable=False)
    delay_minutes = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    expected_arrival = db.Column(db.DateTime)
    
    __table_args__ = (
        db.UniqueConstraint('train_id', 'journey_date', name='unique_operational_status'),
    )

class PlatformChange(db.Model):
    __tablename__ = 'platform_changes'
    
    change_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_id = db.Column(db.String(20), db.ForeignKey('trains.train_id'), nullable=False)
    station_code = db.Column(db.String(10), db.ForeignKey('stations.station_code'), nullable=False)
    journey_date = db.Column(db.Date, nullable=False)
    original_platform_id = db.Column(db.Integer, db.ForeignKey('platforms.platform_id'), nullable=False)
    new_platform_id = db.Column(db.Integer, db.ForeignKey('platforms.platform_id'), nullable=False)
    change_time = db.Column(db.DateTime, default=datetime.utcnow)
    reason = db.Column(db.String(255))

class IssueTicket(db.Model):
    __tablename__ = 'issue_tickets'
    
    issue_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pnr = db.Column(db.String(20), db.ForeignKey('reservations.pnr', ondelete='SET NULL'))
    passenger_id = db.Column(db.Integer, db.ForeignKey('passengers.passenger_id'), nullable=False)
    issue_type = db.Column(db.Enum(IssueType), nullable=False)
    description = db.Column(db.Text, nullable=False)
    creation_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum(IssueStatus), default=IssueStatus.PENDING)
    priority = db.Column(db.Enum(IssuePriority), default=IssuePriority.MEDIUM)
    resolution_type = db.Column(db.Enum(ResolutionType))
    resolution_time = db.Column(db.DateTime)

class RescheduleOption(db.Model):
    __tablename__ = 'reschedule_options'
    
    reschedule_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue_tickets.issue_id', ondelete='CASCADE'), nullable=False)
    original_pnr = db.Column(db.String(20), db.ForeignKey('reservations.pnr'), nullable=False)
    new_train_id = db.Column(db.String(20), db.ForeignKey('trains.train_id'), nullable=False)
    new_journey_date = db.Column(db.Date, nullable=False)
    new_source_station = db.Column(db.String(10), db.ForeignKey('stations.station_code'), nullable=False)
    new_destination_station = db.Column(db.String(10), db.ForeignKey('stations.station_code'), nullable=False)
    booking_preference = db.Column(db.String(50), default='next_available')
    reason_for_change = db.Column(db.String(255))
    additional_cost = db.Column(db.Numeric(10, 2), default=0)
    is_selected = db.Column(db.Boolean, default=False)

class TicketCollector(db.Model):
    __tablename__ = 'ticket_collectors'
    
    tc_id = db.Column(db.String(20), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20), nullable=False)
    station_code = db.Column(db.String(10), db.ForeignKey('stations.station_code'))

class TCSchedule(db.Model):
    __tablename__ = 'tc_schedules'
    
    schedule_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tc_id = db.Column(db.String(20), db.ForeignKey('ticket_collectors.tc_id', ondelete='CASCADE'), nullable=False)
    train_id = db.Column(db.String(20), db.ForeignKey('trains.train_id'))
    station_code = db.Column(db.String(10), db.ForeignKey('stations.station_code'))
    duty_date = db.Column(db.Date, nullable=False)
    shift_start = db.Column(db.Time, nullable=False)
    shift_end = db.Column(db.Time, nullable=False)

class TCPerformance(db.Model):
    __tablename__ = 'tc_performance'
    
    performance_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tc_id = db.Column(db.String(20), db.ForeignKey('ticket_collectors.tc_id', ondelete='CASCADE'), nullable=False)
    month = db.Column(db.SmallInteger, nullable=False)
    year = db.Column(db.SmallInteger, nullable=False)
    tickets_checked = db.Column(db.Integer, default=0)
    violations_detected = db.Column(db.Integer, default=0)
    passenger_complaints = db.Column(db.Integer, default=0)
    rating = db.Column(db.Numeric(3, 2))
    
    __table_args__ = (
        db.UniqueConstraint('tc_id', 'month', 'year', name='unique_tc_performance'),
    )

class CrewAssignment(db.Model):
    __tablename__ = 'crew_assignments'
    
    assignment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_id = db.Column(db.String(20), db.ForeignKey('trains.train_id'), nullable=False)
    journey_date = db.Column(db.Date, nullable=False)
    crew_type = db.Column(db.Enum(CrewType), nullable=False)
    employee_id = db.Column(db.String(20), nullable=False) 
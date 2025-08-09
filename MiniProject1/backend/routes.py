from flask import Blueprint, request, jsonify
from app import db
from models import *
from datetime import datetime
import uuid

api = Blueprint('api', __name__)

# Train Management Routes
@api.route('/trains', methods=['GET'])
def get_trains():
    trains = Train.query.all()
    return jsonify([{
        'train_id': train.train_id,
        'train_name': train.train_name,
        'train_type': train.train_type.value,
        'total_capacity': train.total_capacity,
        'frequency': train.frequency.value,
        'special_attributes': train.special_attributes
    } for train in trains])

@api.route('/trains', methods=['POST'])
def create_train():
    data = request.get_json()
    train = Train(
        train_id=data['train_id'],
        train_name=data['train_name'],
        train_type=TrainType[data['train_type'].upper()],
        total_capacity=data['total_capacity'],
        frequency=Frequency[data['frequency'].upper()],
        special_attributes=data.get('special_attributes')
    )
    db.session.add(train)
    db.session.commit()
    return jsonify({'message': 'Train created successfully'}), 201

# Station Management Routes
@api.route('/stations', methods=['GET'])
def get_stations():
    stations = Station.query.all()
    return jsonify([{
        'station_code': station.station_code,
        'station_name': station.station_name,
        'latitude': float(station.latitude) if station.latitude else None,
        'longitude': float(station.longitude) if station.longitude else None,
        'total_platforms': station.total_platforms,
        'facilities': station.facilities
    } for station in stations])

@api.route('/stations', methods=['POST'])
def create_station():
    data = request.get_json()
    station = Station(
        station_code=data['station_code'],
        station_name=data['station_name'],
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        total_platforms=data['total_platforms'],
        facilities=data.get('facilities')
    )
    db.session.add(station)
    db.session.commit()
    return jsonify({'message': 'Station created successfully'}), 201

# Route Management Routes
@api.route('/routes', methods=['GET'])
def get_routes():
    routes = Route.query.all()
    return jsonify([{
        'route_id': route.route_id,
        'source_station': route.source_station,
        'destination_station': route.destination_station,
        'total_distance': float(route.total_distance)
    } for route in routes])

@api.route('/routes', methods=['POST'])
def create_route():
    data = request.get_json()
    route = Route(
        source_station=data['source_station'],
        destination_station=data['destination_station'],
        total_distance=data['total_distance']
    )
    db.session.add(route)
    db.session.commit()
    return jsonify({'message': 'Route created successfully'}), 201

# Reservation Management Routes
@api.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.get_json()
    
    # Generate PNR
    pnr = str(uuid.uuid4())[:8].upper()
    
    # Create reservation
    reservation = Reservation(
        pnr=pnr,
        train_id=data['train_id'],
        journey_date=datetime.strptime(data['journey_date'], '%Y-%m-%d').date(),
        source_station=data['source_station'],
        destination_station=data['destination_station'],
        booking_status=BookingStatus.CONFIRMED,
        total_fare=data['total_fare'],
        quota_id=data.get('quota_id'),
        booking_flexibility=FlexibilityPreference[data.get('booking_flexibility', 'RIGID').upper()],
        alternative_contact=data.get('alternative_contact'),
        special_instructions=data.get('special_instructions')
    )
    
    db.session.add(reservation)
    
    # Create passenger records
    for passenger_data in data['passengers']:
        passenger = Passenger(
            first_name=passenger_data['first_name'],
            last_name=passenger_data['last_name'],
            email=passenger_data.get('email'),
            phone=passenger_data['phone'],
            date_of_birth=datetime.strptime(passenger_data['date_of_birth'], '%Y-%m-%d').date() if passenger_data.get('date_of_birth') else None,
            gender=Gender[passenger_data.get('gender', 'OTHER').upper()],
            address=passenger_data.get('address'),
            special_requirements=passenger_data.get('special_requirements')
        )
        db.session.add(passenger)
        db.session.flush()  # Get the passenger_id
        
        # Create reservation passenger record
        reservation_passenger = ReservationPassenger(
            pnr=pnr,
            passenger_id=passenger.passenger_id,
            seat_number=passenger_data.get('seat_number'),
            coach_id=passenger_data.get('coach_id'),
            ticket_status=BookingStatus.CONFIRMED,
            fare=passenger_data['fare']
        )
        db.session.add(reservation_passenger)
    
    db.session.commit()
    return jsonify({'pnr': pnr, 'message': 'Reservation created successfully'}), 201

@api.route('/reservations/<pnr>', methods=['GET'])
def get_reservation(pnr):
    reservation = Reservation.query.get_or_404(pnr)
    passengers = ReservationPassenger.query.filter_by(pnr=pnr).all()
    
    return jsonify({
        'pnr': reservation.pnr,
        'train_id': reservation.train_id,
        'journey_date': reservation.journey_date.strftime('%Y-%m-%d'),
        'source_station': reservation.source_station,
        'destination_station': reservation.destination_station,
        'booking_status': reservation.booking_status.value,
        'total_fare': float(reservation.total_fare),
        'passengers': [{
            'passenger_id': p.passenger_id,
            'seat_number': p.seat_number,
            'coach_id': p.coach_id,
            'ticket_status': p.ticket_status.value,
            'fare': float(p.fare)
        } for p in passengers]
    })

@api.route('/reservations', methods=['GET'])
def get_reservations():
    reservations = Reservation.query.all()
    return jsonify([{
        'pnr': reservation.pnr,
        'train_id': reservation.train_id,
        'journey_date': reservation.journey_date.strftime('%Y-%m-%d'),
        'source_station': reservation.source_station,
        'destination_station': reservation.destination_station,
        'booking_status': reservation.booking_status.value,
        'total_fare': float(reservation.total_fare),
        'passengers': [{
            'first_name': p.first_name,
            'last_name': p.last_name,
            'email': p.email,
            'phone': p.phone,
            'date_of_birth': p.date_of_birth.strftime('%Y-%m-%d') if p.date_of_birth else None,
            'gender': p.gender.value if p.gender else None,
            'address': p.address,
            'special_requirements': p.special_requirements,
            'fare': float(p.fare)
        } for p in reservation.passengers]
    } for reservation in reservations])

@api.route('/reservations/<pnr>', methods=['DELETE'])
def delete_reservation(pnr):
    reservation = Reservation.query.get_or_404(pnr)
    
    # Delete associated passengers
    for passenger in reservation.passengers:
        db.session.delete(passenger)
    
    # Delete the reservation
    db.session.delete(reservation)
    db.session.commit()
    
    return jsonify({'message': 'Reservation deleted successfully'})

# Issue Management Routes
@api.route('/issues', methods=['POST'])
def create_issue():
    data = request.get_json()
    
    issue = IssueTicket(
        pnr=data.get('pnr'),
        passenger_id=data['passenger_id'],
        issue_type=IssueType[data['issue_type'].upper()],
        description=data['description'],
        priority=IssuePriority[data.get('priority', 'MEDIUM').upper()]
    )
    
    db.session.add(issue)
    db.session.commit()
    
    return jsonify({
        'issue_id': issue.issue_id,
        'message': 'Issue ticket created successfully'
    }), 201

@api.route('/issues/<int:issue_id>', methods=['GET'])
def get_issue(issue_id):
    issue = IssueTicket.query.get_or_404(issue_id)
    
    return jsonify({
        'issue_id': issue.issue_id,
        'pnr': issue.pnr,
        'passenger_id': issue.passenger_id,
        'issue_type': issue.issue_type.value,
        'description': issue.description,
        'status': issue.status.value,
        'priority': issue.priority.value,
        'resolution_type': issue.resolution_type.value if issue.resolution_type else None,
        'creation_time': issue.creation_time.isoformat(),
        'resolution_time': issue.resolution_time.isoformat() if issue.resolution_time else None
    })

# Train Schedule Routes
@api.route('/train-schedules', methods=['GET'])
def get_train_schedules():
    schedules = TrainSchedule.query.all()
    return jsonify([{
        'schedule_id': schedule.schedule_id,
        'train_id': schedule.train_id,
        'route_id': schedule.route_id,
        'day_of_operation': schedule.day_of_operation.value
    } for schedule in schedules])

@api.route('/train-schedules', methods=['POST'])
def create_train_schedule():
    data = request.get_json()
    
    schedule = TrainSchedule(
        train_id=data['train_id'],
        route_id=data['route_id'],
        day_of_operation=DayOfWeek[data['day_of_operation'].upper()]
    )
    
    db.session.add(schedule)
    db.session.commit()
    
    return jsonify({'message': 'Train schedule created successfully'}), 201

# Station Schedule Routes
@api.route('/station-schedules', methods=['POST'])
def create_station_schedule():
    data = request.get_json()
    
    schedule = StationSchedule(
        schedule_id=data['schedule_id'],
        station_code=data['station_code'],
        arrival_time=datetime.strptime(data['arrival_time'], '%H:%M').time() if data.get('arrival_time') else None,
        departure_time=datetime.strptime(data['departure_time'], '%H:%M').time() if data.get('departure_time') else None,
        platform_id=data.get('platform_id'),
        halt_duration=data.get('halt_duration', 5)
    )
    
    db.session.add(schedule)
    db.session.commit()
    
    return jsonify({'message': 'Station schedule created successfully'}), 201

# Dynamic Pricing Routes
@api.route('/dynamic-pricing', methods=['POST'])
def create_dynamic_pricing():
    data = request.get_json()
    
    pricing = DynamicPricing(
        train_id=data['train_id'],
        journey_date=datetime.strptime(data['journey_date'], '%Y-%m-%d').date(),
        coach_type=CoachType[data['coach_type'].upper()],
        base_fare=data['base_fare'],
        dynamic_fare=data['dynamic_fare'],
        reason=data.get('reason')
    )
    
    db.session.add(pricing)
    db.session.commit()
    
    return jsonify({'message': 'Dynamic pricing created successfully'}), 201

# Operational Status Routes
@api.route('/operational-status', methods=['POST'])
def update_operational_status():
    data = request.get_json()
    
    status = OperationalStatus(
        train_id=data['train_id'],
        journey_date=datetime.strptime(data['journey_date'], '%Y-%m-%d').date(),
        current_station=data.get('current_station'),
        next_station=data.get('next_station'),
        current_status=data['current_status'],
        delay_minutes=data.get('delay_minutes', 0),
        expected_arrival=datetime.strptime(data['expected_arrival'], '%Y-%m-%d %H:%M') if data.get('expected_arrival') else None
    )
    
    db.session.add(status)
    db.session.commit()
    
    return jsonify({'message': 'Operational status updated successfully'}), 201

# Ticket Collector Routes
@api.route('/ticket-collectors', methods=['POST'])
def create_ticket_collector():
    data = request.get_json()
    
    collector = TicketCollector(
        tc_id=data['tc_id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data.get('email'),
        phone=data['phone'],
        station_code=data.get('station_code')
    )
    
    db.session.add(collector)
    db.session.commit()
    
    return jsonify({'message': 'Ticket collector created successfully'}), 201

@api.route('/ticket-collectors/<tc_id>/schedule', methods=['POST'])
def create_tc_schedule(tc_id):
    data = request.get_json()
    
    schedule = TCSchedule(
        tc_id=tc_id,
        train_id=data.get('train_id'),
        station_code=data.get('station_code'),
        duty_date=datetime.strptime(data['duty_date'], '%Y-%m-%d').date(),
        shift_start=datetime.strptime(data['shift_start'], '%H:%M').time(),
        shift_end=datetime.strptime(data['shift_end'], '%H:%M').time()
    )
    
    db.session.add(schedule)
    db.session.commit()
    
    return jsonify({'message': 'Ticket collector schedule created successfully'}), 201 
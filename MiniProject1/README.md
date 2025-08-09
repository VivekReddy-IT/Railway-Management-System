# Railway Reservation System

A comprehensive railway reservation system built with Flask and React.

## Features

- Train and station management
- Route management
- Reservation system with PNR generation
- Dynamic pricing
- Operational status tracking
- Issue management
- Ticket collector management
- Real-time updates

## Prerequisites

- Python 3.8+
- PostgreSQL
- Node.js 14+
- npm or yarn

## Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Run the backend server:
```bash
flask run
```

## Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## API Documentation

### Train Management

- `GET /api/trains` - Get all trains
- `POST /api/trains` - Create a new train

### Station Management

- `GET /api/stations` - Get all stations
- `POST /api/stations` - Create a new station

### Route Management

- `GET /api/routes` - Get all routes
- `POST /api/routes` - Create a new route

### Reservation Management

- `POST /api/reservations` - Create a new reservation
- `GET /api/reservations/<pnr>` - Get reservation details

### Issue Management

- `POST /api/issues` - Create a new issue
- `GET /api/issues/<issue_id>` - Get issue details

### Train Schedule Management

- `GET /api/train-schedules` - Get all train schedules
- `POST /api/train-schedules` - Create a new train schedule

### Station Schedule Management

- `POST /api/station-schedules` - Create a new station schedule

### Dynamic Pricing

- `POST /api/dynamic-pricing` - Create dynamic pricing

### Operational Status

- `POST /api/operational-status` - Update operational status

### Ticket Collector Management

- `POST /api/ticket-collectors` - Create a new ticket collector
- `POST /api/ticket-collectors/<tc_id>/schedule` - Create ticket collector schedule

## Database Schema

The database schema includes tables for:
- Trains
- Stations
- Routes
- Reservations
- Passengers
- Schedules
- Issues
- Ticket Collectors
- And more...

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License. 
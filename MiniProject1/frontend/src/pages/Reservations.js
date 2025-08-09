import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Grid,
  IconButton,
  Stepper,
  Step,
  StepLabel,
  FormControl,
  InputLabel,
  Select,
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import axios from 'axios';

const steps = ['Select Journey', 'Passenger Details', 'Review & Confirm'];

function Reservations() {
  const [activeStep, setActiveStep] = useState(0);
  const [reservations, setReservations] = useState([]);
  const [trains, setTrains] = useState([]);
  const [stations, setStations] = useState([]);
  const [open, setOpen] = useState(false);
  const [formData, setFormData] = useState({
    train_id: '',
    journey_date: null,
    source_station: '',
    destination_station: '',
    passengers: [
      {
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        date_of_birth: null,
        gender: '',
        address: '',
        special_requirements: '',
        fare: '',
      },
    ],
  });

  useEffect(() => {
    fetchReservations();
    fetchTrains();
    fetchStations();
  }, []);

  const fetchReservations = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/reservations');
      setReservations(response.data);
    } catch (error) {
      console.error('Error fetching reservations:', error);
    }
  };

  const fetchTrains = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/trains');
      setTrains(response.data);
    } catch (error) {
      console.error('Error fetching trains:', error);
    }
  };

  const fetchStations = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/stations');
      setStations(response.data);
    } catch (error) {
      console.error('Error fetching stations:', error);
    }
  };

  const handleNext = () => {
    setActiveStep((prevStep) => prevStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handlePassengerChange = (index, field, value) => {
    const updatedPassengers = [...formData.passengers];
    updatedPassengers[index] = {
      ...updatedPassengers[index],
      [field]: value,
    };
    setFormData({
      ...formData,
      passengers: updatedPassengers,
    });
  };

  const addPassenger = () => {
    setFormData({
      ...formData,
      passengers: [
        ...formData.passengers,
        {
          first_name: '',
          last_name: '',
          email: '',
          phone: '',
          date_of_birth: null,
          gender: '',
          address: '',
          special_requirements: '',
          fare: '',
        },
      ],
    });
  };

  const removePassenger = (index) => {
    const updatedPassengers = formData.passengers.filter((_, i) => i !== index);
    setFormData({
      ...formData,
      passengers: updatedPassengers,
    });
  };

  const handleSubmit = async () => {
    try {
      await axios.post('http://localhost:5000/api/reservations', formData);
      fetchReservations();
      setOpen(false);
      setActiveStep(0);
    } catch (error) {
      console.error('Error creating reservation:', error);
    }
  };

  const handleDelete = async (pnr) => {
    if (window.confirm('Are you sure you want to delete this reservation?')) {
      try {
        await axios.delete(`http://localhost:5000/api/reservations/${pnr}`);
        fetchReservations();
      } catch (error) {
        console.error('Error deleting reservation:', error);
      }
    }
  };

  const getStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Train</InputLabel>
                <Select
                  name="train_id"
                  value={formData.train_id}
                  onChange={handleChange}
                  required
                >
                  {trains.map((train) => (
                    <MenuItem key={train.train_id} value={train.train_id}>
                      {train.train_name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <DatePicker
                  label="Journey Date"
                  value={formData.journey_date}
                  onChange={(date) =>
                    setFormData({ ...formData, journey_date: date })
                  }
                  renderInput={(params) => <TextField {...params} fullWidth />}
                />
              </LocalizationProvider>
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Source Station</InputLabel>
                <Select
                  name="source_station"
                  value={formData.source_station}
                  onChange={handleChange}
                  required
                >
                  {stations.map((station) => (
                    <MenuItem key={station.station_code} value={station.station_code}>
                      {station.station_name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Destination Station</InputLabel>
                <Select
                  name="destination_station"
                  value={formData.destination_station}
                  onChange={handleChange}
                  required
                >
                  {stations.map((station) => (
                    <MenuItem key={station.station_code} value={station.station_code}>
                      {station.station_name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        );
      case 1:
        return (
          <Box>
            {formData.passengers.map((passenger, index) => (
              <Box key={index} sx={{ mb: 3, p: 2, border: '1px solid #ccc', borderRadius: 1 }}>
                <Typography variant="h6" gutterBottom>
                  Passenger {index + 1}
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="First Name"
                      value={passenger.first_name}
                      onChange={(e) =>
                        handlePassengerChange(index, 'first_name', e.target.value)
                      }
                      required
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Last Name"
                      value={passenger.last_name}
                      onChange={(e) =>
                        handlePassengerChange(index, 'last_name', e.target.value)
                      }
                      required
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Email"
                      type="email"
                      value={passenger.email}
                      onChange={(e) =>
                        handlePassengerChange(index, 'email', e.target.value)
                      }
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Phone"
                      value={passenger.phone}
                      onChange={(e) =>
                        handlePassengerChange(index, 'phone', e.target.value)
                      }
                      required
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <LocalizationProvider dateAdapter={AdapterDateFns}>
                      <DatePicker
                        label="Date of Birth"
                        value={passenger.date_of_birth}
                        onChange={(date) =>
                          handlePassengerChange(index, 'date_of_birth', date)
                        }
                        renderInput={(params) => <TextField {...params} fullWidth />}
                      />
                    </LocalizationProvider>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <FormControl fullWidth>
                      <InputLabel>Gender</InputLabel>
                      <Select
                        value={passenger.gender}
                        onChange={(e) =>
                          handlePassengerChange(index, 'gender', e.target.value)
                        }
                      >
                        <MenuItem value="Male">Male</MenuItem>
                        <MenuItem value="Female">Female</MenuItem>
                        <MenuItem value="Other">Other</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Address"
                      multiline
                      rows={2}
                      value={passenger.address}
                      onChange={(e) =>
                        handlePassengerChange(index, 'address', e.target.value)
                      }
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Special Requirements"
                      multiline
                      rows={2}
                      value={passenger.special_requirements}
                      onChange={(e) =>
                        handlePassengerChange(index, 'special_requirements', e.target.value)
                      }
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Fare"
                      type="number"
                      value={passenger.fare}
                      onChange={(e) =>
                        handlePassengerChange(index, 'fare', e.target.value)
                      }
                      required
                    />
                  </Grid>
                  {index > 0 && (
                    <Grid item xs={12}>
                      <Button
                        variant="outlined"
                        color="error"
                        onClick={() => removePassenger(index)}
                      >
                        Remove Passenger
                      </Button>
                    </Grid>
                  )}
                </Grid>
              </Box>
            ))}
            <Button variant="outlined" onClick={addPassenger} sx={{ mt: 2 }}>
              Add Another Passenger
            </Button>
          </Box>
        );
      case 2:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Journey Details
            </Typography>
            <Typography>
              Train: {trains.find((t) => t.train_id === formData.train_id)?.train_name}
            </Typography>
            <Typography>
              Date: {formData.journey_date?.toLocaleDateString()}
            </Typography>
            <Typography>
              From: {stations.find((s) => s.station_code === formData.source_station)?.station_name}
            </Typography>
            <Typography>
              To: {stations.find((s) => s.station_code === formData.destination_station)?.station_name}
            </Typography>

            <Typography variant="h6" sx={{ mt: 3 }} gutterBottom>
              Passenger Details
            </Typography>
            {formData.passengers.map((passenger, index) => (
              <Box key={index} sx={{ mb: 2, p: 2, border: '1px solid #ccc', borderRadius: 1 }}>
                <Typography variant="subtitle1">
                  Passenger {index + 1}: {passenger.first_name} {passenger.last_name}
                </Typography>
                <Typography>Email: {passenger.email}</Typography>
                <Typography>Phone: {passenger.phone}</Typography>
                <Typography>Fare: ₹{passenger.fare}</Typography>
              </Box>
            ))}
          </Box>
        );
      default:
        return 'Unknown step';
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Reservations
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpen(true)}
        >
          New Reservation
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>PNR</TableCell>
              <TableCell>Train</TableCell>
              <TableCell>Date</TableCell>
              <TableCell>From</TableCell>
              <TableCell>To</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Total Fare</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {reservations.map((reservation) => (
              <TableRow key={reservation.pnr}>
                <TableCell>{reservation.pnr}</TableCell>
                <TableCell>
                  {trains.find((t) => t.train_id === reservation.train_id)?.train_name}
                </TableCell>
                <TableCell>{reservation.journey_date}</TableCell>
                <TableCell>
                  {stations.find((s) => s.station_code === reservation.source_station)?.station_name}
                </TableCell>
                <TableCell>
                  {stations.find((s) => s.station_code === reservation.destination_station)?.station_name}
                </TableCell>
                <TableCell>{reservation.booking_status}</TableCell>
                <TableCell>₹{reservation.total_fare}</TableCell>
                <TableCell>
                  <IconButton>
                    <EditIcon />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(reservation.pnr)}>
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>New Reservation</DialogTitle>
        <DialogContent>
          <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>
          {getStepContent(activeStep)}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button onClick={handleBack} disabled={activeStep === 0}>
            Back
          </Button>
          <Button
            variant="contained"
            onClick={activeStep === steps.length - 1 ? handleSubmit : handleNext}
          >
            {activeStep === steps.length - 1 ? 'Confirm' : 'Next'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default Reservations; 
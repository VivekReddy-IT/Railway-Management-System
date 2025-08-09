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
  IconButton,
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import axios from 'axios';

function Stations() {
  const [stations, setStations] = useState([]);
  const [open, setOpen] = useState(false);
  const [editingStation, setEditingStation] = useState(null);
  const [formData, setFormData] = useState({
    station_code: '',
    station_name: '',
    latitude: '',
    longitude: '',
    total_platforms: '',
    facilities: '',
  });

  useEffect(() => {
    fetchStations();
  }, []);

  const fetchStations = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/stations');
      setStations(response.data);
    } catch (error) {
      console.error('Error fetching stations:', error);
    }
  };

  const handleClickOpen = (station = null) => {
    if (station) {
      setEditingStation(station);
      setFormData({
        station_code: station.station_code,
        station_name: station.station_name,
        latitude: station.latitude || '',
        longitude: station.longitude || '',
        total_platforms: station.total_platforms,
        facilities: station.facilities || '',
      });
    } else {
      setEditingStation(null);
      setFormData({
        station_code: '',
        station_name: '',
        latitude: '',
        longitude: '',
        total_platforms: '',
        facilities: '',
      });
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingStation(null);
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingStation) {
        await axios.put(`http://localhost:5000/api/stations/${editingStation.station_code}`, formData);
      } else {
        await axios.post('http://localhost:5000/api/stations', formData);
      }
      fetchStations();
      handleClose();
    } catch (error) {
      console.error('Error saving station:', error);
    }
  };

  const handleDelete = async (stationCode) => {
    if (window.confirm('Are you sure you want to delete this station?')) {
      try {
        await axios.delete(`http://localhost:5000/api/stations/${stationCode}`);
        fetchStations();
      } catch (error) {
        console.error('Error deleting station:', error);
      }
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Station Management
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleClickOpen()}
        >
          Add Station
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Station Code</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>Latitude</TableCell>
              <TableCell>Longitude</TableCell>
              <TableCell>Platforms</TableCell>
              <TableCell>Facilities</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {stations.map((station) => (
              <TableRow key={station.station_code}>
                <TableCell>{station.station_code}</TableCell>
                <TableCell>{station.station_name}</TableCell>
                <TableCell>{station.latitude}</TableCell>
                <TableCell>{station.longitude}</TableCell>
                <TableCell>{station.total_platforms}</TableCell>
                <TableCell>{station.facilities}</TableCell>
                <TableCell>
                  <IconButton onClick={() => handleClickOpen(station)}>
                    <EditIcon />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(station.station_code)}>
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>
          {editingStation ? 'Edit Station' : 'Add New Station'}
        </DialogTitle>
        <DialogContent>
          <Box component="form" sx={{ mt: 2 }}>
            <TextField
              fullWidth
              label="Station Code"
              name="station_code"
              value={formData.station_code}
              onChange={handleChange}
              margin="normal"
              required
              disabled={!!editingStation}
            />
            <TextField
              fullWidth
              label="Station Name"
              name="station_name"
              value={formData.station_name}
              onChange={handleChange}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Latitude"
              name="latitude"
              type="number"
              value={formData.latitude}
              onChange={handleChange}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Longitude"
              name="longitude"
              type="number"
              value={formData.longitude}
              onChange={handleChange}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Total Platforms"
              name="total_platforms"
              type="number"
              value={formData.total_platforms}
              onChange={handleChange}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Facilities"
              name="facilities"
              value={formData.facilities}
              onChange={handleChange}
              margin="normal"
              multiline
              rows={2}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editingStation ? 'Update' : 'Add'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default Stations; 
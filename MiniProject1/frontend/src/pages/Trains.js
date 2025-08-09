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
  IconButton,
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import axios from 'axios';

const trainTypes = ['express', 'passenger', 'special', 'devotional'];
const frequencies = ['daily', 'weekly', 'bi-weekly', 'special'];

function Trains() {
  const [trains, setTrains] = useState([]);
  const [open, setOpen] = useState(false);
  const [editingTrain, setEditingTrain] = useState(null);
  const [formData, setFormData] = useState({
    train_id: '',
    train_name: '',
    train_type: '',
    total_capacity: '',
    frequency: '',
    special_attributes: '',
  });

  useEffect(() => {
    fetchTrains();
  }, []);

  const fetchTrains = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/trains');
      setTrains(response.data);
    } catch (error) {
      console.error('Error fetching trains:', error);
    }
  };

  const handleClickOpen = (train = null) => {
    if (train) {
      setEditingTrain(train);
      setFormData({
        train_id: train.train_id,
        train_name: train.train_name,
        train_type: train.train_type,
        total_capacity: train.total_capacity,
        frequency: train.frequency,
        special_attributes: train.special_attributes || '',
      });
    } else {
      setEditingTrain(null);
      setFormData({
        train_id: '',
        train_name: '',
        train_type: '',
        total_capacity: '',
        frequency: '',
        special_attributes: '',
      });
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingTrain(null);
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
      if (editingTrain) {
        await axios.put(`http://localhost:5000/api/trains/${editingTrain.train_id}`, formData);
      } else {
        await axios.post('http://localhost:5000/api/trains', formData);
      }
      fetchTrains();
      handleClose();
    } catch (error) {
      console.error('Error saving train:', error);
    }
  };

  const handleDelete = async (trainId) => {
    if (window.confirm('Are you sure you want to delete this train?')) {
      try {
        await axios.delete(`http://localhost:5000/api/trains/${trainId}`);
        fetchTrains();
      } catch (error) {
        console.error('Error deleting train:', error);
      }
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Train Management
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleClickOpen()}
        >
          Add Train
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Train ID</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Capacity</TableCell>
              <TableCell>Frequency</TableCell>
              <TableCell>Special Attributes</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {trains.map((train) => (
              <TableRow key={train.train_id}>
                <TableCell>{train.train_id}</TableCell>
                <TableCell>{train.train_name}</TableCell>
                <TableCell>{train.train_type}</TableCell>
                <TableCell>{train.total_capacity}</TableCell>
                <TableCell>{train.frequency}</TableCell>
                <TableCell>{train.special_attributes}</TableCell>
                <TableCell>
                  <IconButton onClick={() => handleClickOpen(train)}>
                    <EditIcon />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(train.train_id)}>
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
          {editingTrain ? 'Edit Train' : 'Add New Train'}
        </DialogTitle>
        <DialogContent>
          <Box component="form" sx={{ mt: 2 }}>
            <TextField
              fullWidth
              label="Train ID"
              name="train_id"
              value={formData.train_id}
              onChange={handleChange}
              margin="normal"
              required
              disabled={!!editingTrain}
            />
            <TextField
              fullWidth
              label="Train Name"
              name="train_name"
              value={formData.train_name}
              onChange={handleChange}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              select
              label="Train Type"
              name="train_type"
              value={formData.train_type}
              onChange={handleChange}
              margin="normal"
              required
            >
              {trainTypes.map((type) => (
                <MenuItem key={type} value={type}>
                  {type.charAt(0).toUpperCase() + type.slice(1)}
                </MenuItem>
              ))}
            </TextField>
            <TextField
              fullWidth
              label="Total Capacity"
              name="total_capacity"
              type="number"
              value={formData.total_capacity}
              onChange={handleChange}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              select
              label="Frequency"
              name="frequency"
              value={formData.frequency}
              onChange={handleChange}
              margin="normal"
              required
            >
              {frequencies.map((freq) => (
                <MenuItem key={freq} value={freq}>
                  {freq.charAt(0).toUpperCase() + freq.slice(1)}
                </MenuItem>
              ))}
            </TextField>
            <TextField
              fullWidth
              label="Special Attributes"
              name="special_attributes"
              value={formData.special_attributes}
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
            {editingTrain ? 'Update' : 'Add'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default Trains;
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  Autocomplete,
  CircularProgress,
  Card,
  CardContent,
  Divider,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import {
  DirectionsRailway as TrainIcon,
  AccessTime as TimeIcon,
  ConfirmationNumber as TicketIcon,
} from '@mui/icons-material';
import axios from 'axios';

const TrainSearch = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [searchResults, setSearchResults] = useState([]);
  const [formData, setFormData] = useState({
    from: '',
    to: '',
    date: new Date(),
  });

  // Mock stations data - replace with API call
  const stations = [
    { code: 'MUM', name: 'Mumbai Central' },
    { code: 'DEL', name: 'New Delhi' },
    { code: 'BLR', name: 'Bangalore City' },
    { code: 'CHN', name: 'Chennai Central' },
    { code: 'KOL', name: 'Kolkata' },
  ];

  const handleSearch = async () => {
    setLoading(true);
    try {
      // Replace with actual API call
      const response = await axios.get('/api/trains/search', {
        params: {
          from: formData.from.code,
          to: formData.to.code,
          date: formData.date.toISOString().split('T')[0],
        },
      });
      setSearchResults(response.data);
    } catch (error) {
      console.error('Error searching trains:', error);
      // Mock data for demonstration
      setSearchResults([
        {
          id: 1,
          name: 'Rajdhani Express',
          number: '12301',
          from: 'MUM',
          to: 'DEL',
          departure: '16:55',
          arrival: '08:35',
          duration: '15h 40m',
          fare: {
            ac: 2500,
            nonac: 1200,
          },
        },
        {
          id: 2,
          name: 'Duronto Express',
          number: '12213',
          from: 'MUM',
          to: 'DEL',
          departure: '23:00',
          arrival: '15:30',
          duration: '16h 30m',
          fare: {
            ac: 2200,
            nonac: 1000,
          },
        },
      ]);
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Paper
        elevation={3}
        sx={{
          p: 4,
          mb: 4,
          background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)',
          color: 'white',
        }}
      >
        <Typography variant="h4" component="h1" gutterBottom>
          Search Trains
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Autocomplete
              options={stations}
              getOptionLabel={(option) => `${option.name} (${option.code})`}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="From Station"
                  variant="outlined"
                  fullWidth
                  sx={{ backgroundColor: 'white', borderRadius: 1 }}
                />
              )}
              value={formData.from}
              onChange={(event, newValue) => {
                setFormData({ ...formData, from: newValue });
              }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <Autocomplete
              options={stations}
              getOptionLabel={(option) => `${option.name} (${option.code})`}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="To Station"
                  variant="outlined"
                  fullWidth
                  sx={{ backgroundColor: 'white', borderRadius: 1 }}
                />
              )}
              value={formData.to}
              onChange={(event, newValue) => {
                setFormData({ ...formData, to: newValue });
              }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <LocalizationProvider dateAdapter={AdapterDateFns}>
              <DatePicker
                label="Journey Date"
                value={formData.date}
                onChange={(newValue) => {
                  setFormData({ ...formData, date: newValue });
                }}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    fullWidth
                    sx={{ backgroundColor: 'white', borderRadius: 1 }}
                  />
                )}
              />
            </LocalizationProvider>
          </Grid>
        </Grid>
        <Box sx={{ mt: 3, textAlign: 'center' }}>
          <Button
            variant="contained"
            size="large"
            onClick={handleSearch}
            disabled={loading || !formData.from || !formData.to}
            sx={{
              backgroundColor: 'white',
              color: 'primary.main',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.9)',
              },
            }}
          >
            {loading ? <CircularProgress size={24} /> : 'Search Trains'}
          </Button>
        </Box>
      </Paper>

      {/* Search Results */}
      {searchResults.length > 0 && (
        <Box>
          <Typography variant="h5" gutterBottom>
            Available Trains
          </Typography>
          <Grid container spacing={3}>
            {searchResults.map((train) => (
              <Grid item xs={12} key={train.id}>
                <Card>
                  <CardContent>
                    <Grid container spacing={2} alignItems="center">
                      <Grid item xs={12} md={3}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <TrainIcon color="primary" />
                          <Box>
                            <Typography variant="h6">{train.name}</Typography>
                            <Typography variant="body2" color="text.secondary">
                              Train #{train.number}
                            </Typography>
                          </Box>
                        </Box>
                      </Grid>
                      <Grid item xs={12} md={3}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <TimeIcon color="primary" />
                          <Box>
                            <Typography variant="body1">
                              {train.departure} - {train.arrival}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              Duration: {train.duration}
                            </Typography>
                          </Box>
                        </Box>
                      </Grid>
                      <Grid item xs={12} md={3}>
                        <Box>
                          <Typography variant="body1">
                            AC: ₹{train.fare.ac}
                          </Typography>
                          <Typography variant="body1">
                            Non-AC: ₹{train.fare.nonac}
                          </Typography>
                        </Box>
                      </Grid>
                      <Grid item xs={12} md={3}>
                        <Button
                          variant="contained"
                          fullWidth
                          onClick={() => navigate(`/booking/${train.id}`)}
                        >
                          Book Now
                        </Button>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}
    </Container>
  );
};

export default TrainSearch; 
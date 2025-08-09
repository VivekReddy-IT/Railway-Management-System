import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Container,
  Grid,
  Typography,
  Card,
  CardContent,
  CardMedia,
} from '@mui/material';
import {
  DirectionsRailway as TrainIcon,
  AccessTime as TimeIcon,
  ConfirmationNumber as TicketIcon,
  Security as SecurityIcon,
} from '@mui/icons-material';

const features = [
  {
    icon: <TrainIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: 'Extensive Network',
    description: 'Connect to major cities and destinations across the country with our comprehensive rail network.',
  },
  {
    icon: <TimeIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: 'Real-time Updates',
    description: 'Get live train status, platform information, and delay updates in real-time.',
  },
  {
    icon: <TicketIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: 'Easy Booking',
    description: 'Book your tickets in seconds with our user-friendly booking system.',
  },
  {
    icon: <SecurityIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: 'Secure Payments',
    description: 'Your transactions are protected with state-of-the-art security measures.',
  },
];

const Home = () => {
  const navigate = useNavigate();

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)',
          color: 'white',
          py: 8,
          mb: 6,
        }}
      >
        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={6}>
              <Typography variant="h2" component="h1" gutterBottom>
                Welcome to Rail Transit
              </Typography>
              <Typography variant="h5" paragraph>
                Your journey begins here. Book train tickets, check schedules, and travel with comfort.
              </Typography>
              <Button
                variant="contained"
                size="large"
                onClick={() => navigate('/search')}
                sx={{
                  backgroundColor: 'white',
                  color: 'primary.main',
                  '&:hover': {
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                  },
                }}
              >
                Search Trains
              </Button>
            </Grid>
            <Grid item xs={12} md={6}>
              <Box
                component="img"
                src="/train-hero.jpg"
                alt="Modern train"
                sx={{
                  width: '100%',
                  height: 'auto',
                  borderRadius: 2,
                  boxShadow: 3,
                }}
              />
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ mb: 8 }}>
        <Typography variant="h3" component="h2" align="center" gutterBottom>
          Why Choose Rail Transit?
        </Typography>
        <Grid container spacing={4} sx={{ mt: 2 }}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  textAlign: 'center',
                  p: 2,
                }}
              >
                <Box sx={{ mb: 2 }}>{feature.icon}</Box>
                <Typography variant="h6" component="h3" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {feature.description}
                </Typography>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Call to Action */}
      <Box sx={{ bgcolor: 'grey.100', py: 8 }}>
        <Container maxWidth="md">
          <Card sx={{ p: 4, textAlign: 'center' }}>
            <Typography variant="h4" component="h2" gutterBottom>
              Ready to Start Your Journey?
            </Typography>
            <Typography variant="body1" paragraph>
              Join thousands of satisfied travelers who choose Rail Transit for their journey.
            </Typography>
            <Button
              variant="contained"
              size="large"
              onClick={() => navigate('/register')}
              sx={{ mt: 2 }}
            >
              Create Account
            </Button>
          </Card>
        </Container>
      </Box>
    </Box>
  );
};

export default Home; 
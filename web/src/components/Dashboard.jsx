import React from 'react'
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Paper
} from '@mui/material'
import { useNavigate } from 'react-router-dom'

const Dashboard = () => {
  const navigate = useNavigate()

  const features = [
    {
      title: 'Problem Analysis',
      description: 'Analyze business problems and identify root causes',
      action: 'Analyze Problem',
      path: '/analyze'
    },
    {
      title: 'Strategy Generation',
      description: 'Generate multi-option strategic recommendations',
      action: 'Generate Strategy',
      path: '/strategies'
    },
    {
      title: 'Transformation Planning',
      description: 'Plan cloud migrations and digital transformations',
      action: 'Plan Transformation',
      path: '/analyze'
    },
    {
      title: 'Operations Optimization',
      description: 'Optimize business processes and resource allocation',
      action: 'Optimize Operations',
      path: '/analyze'
    },
    {
      title: 'AI Strategy Advisor',
      description: 'Get AI adoption roadmaps and use case identification',
      action: 'Get AI Strategy',
      path: '/strategies'
    },
    {
      title: 'Report Generation',
      description: 'Export professional reports and presentations',
      action: 'Generate Report',
      path: '/reports'
    }
  ]

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Welcome to StrategyForge AI
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        AI-powered business consulting at a fraction of traditional costs
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        {features.map((feature, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {feature.description}
                </Typography>
                <Button
                  variant="contained"
                  onClick={() => navigate(feature.path)}
                >
                  {feature.action}
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Paper sx={{ p: 3, mt: 4 }}>
        <Typography variant="h6" gutterBottom>
          Competitive Advantage
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <Typography variant="subtitle2">Cost</Typography>
            <Typography variant="body2" color="text.secondary">
              $99/month vs $200-500/hour consultants
            </Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="subtitle2">Speed</Typography>
            <Typography variant="body2" color="text.secondary">
              Minutes vs weeks for strategy development
            </Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="subtitle2">Scalability</Typography>
            <Typography variant="body2" color="text.secondary">
              Handle unlimited projects simultaneously
            </Typography>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  )
}

export default Dashboard


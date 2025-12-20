import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Tabs,
  Tab,
  CssBaseline
} from '@mui/material'
import ProblemInput from './components/ProblemInput'
import StrategyViewer from './components/StrategyViewer'
import RoadmapTimeline from './components/RoadmapTimeline'
import ReportExporter from './components/ReportExporter'
import Dashboard from './components/Dashboard'

function App() {
  const [currentTab, setCurrentTab] = useState(0)

  const handleTabChange = (event, newValue) => {
    setCurrentTab(newValue)
  }

  return (
    <Router>
      <CssBaseline />
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              StrategyForge AI
            </Typography>
            <Tabs value={currentTab} onChange={handleTabChange} textColor="inherit">
              <Tab label="Dashboard" component={Link} to="/" />
              <Tab label="Problem Analysis" component={Link} to="/analyze" />
              <Tab label="Strategies" component={Link} to="/strategies" />
              <Tab label="Reports" component={Link} to="/reports" />
            </Tabs>
          </Toolbar>
        </AppBar>

        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/analyze" element={<ProblemInput />} />
            <Route path="/strategies" element={<StrategyViewer />} />
            <Route path="/reports" element={<ReportExporter />} />
          </Routes>
        </Container>
      </Box>
    </Router>
  )
}

export default App


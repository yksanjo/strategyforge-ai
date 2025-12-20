import React, { useState } from 'react'
import {
  Box,
  TextField,
  Button,
  Paper,
  Typography,
  CircularProgress,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material'
import { analyzeProblem } from '../services/api'

const ProblemInput = () => {
  const [problemDescription, setProblemDescription] = useState('')
  const [industry, setIndustry] = useState('')
  const [companySize, setCompanySize] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleAnalyze = async () => {
    if (!problemDescription.trim()) {
      setError('Please enter a problem description')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await analyzeProblem({
        problem_description: problemDescription,
        industry: industry || undefined,
        company_size: companySize || undefined
      })
      setResult(data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Problem Analysis
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Describe your business problem and get AI-powered analysis
      </Typography>

      <Paper sx={{ p: 3, mt: 2 }}>
        <TextField
          fullWidth
          multiline
          rows={6}
          label="Problem Description"
          value={problemDescription}
          onChange={(e) => setProblemDescription(e.target.value)}
          placeholder="Describe your business problem, challenges, or situation..."
          sx={{ mb: 2 }}
        />

        <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>Industry</InputLabel>
            <Select
              value={industry}
              label="Industry"
              onChange={(e) => setIndustry(e.target.value)}
            >
              <MenuItem value="">Not specified</MenuItem>
              <MenuItem value="financial-services">Financial Services</MenuItem>
              <MenuItem value="healthcare">Healthcare</MenuItem>
              <MenuItem value="technology">Technology</MenuItem>
              <MenuItem value="retail">Retail</MenuItem>
              <MenuItem value="manufacturing">Manufacturing</MenuItem>
              <MenuItem value="other">Other</MenuItem>
            </Select>
          </FormControl>

          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>Company Size</InputLabel>
            <Select
              value={companySize}
              label="Company Size"
              onChange={(e) => setCompanySize(e.target.value)}
            >
              <MenuItem value="">Not specified</MenuItem>
              <MenuItem value="startup">Startup</MenuItem>
              <MenuItem value="small">Small</MenuItem>
              <MenuItem value="medium">Medium</MenuItem>
              <MenuItem value="large">Large</MenuItem>
              <MenuItem value="enterprise">Enterprise</MenuItem>
            </Select>
          </FormControl>
        </Box>

        <Button
          variant="contained"
          onClick={handleAnalyze}
          disabled={loading}
          fullWidth
        >
          {loading ? <CircularProgress size={24} /> : 'Analyze Problem'}
        </Button>
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}

      {result && (
        <Paper sx={{ p: 3, mt: 2 }}>
          <Typography variant="h6" gutterBottom>
            Analysis Results
          </Typography>
          <Box
            component="pre"
            sx={{
              backgroundColor: '#f5f5f5',
              p: 2,
              borderRadius: 1,
              overflow: 'auto',
              maxHeight: 500
            }}
          >
            {JSON.stringify(result, null, 2)}
          </Box>
        </Paper>
      )}
    </Box>
  )
}

export default ProblemInput


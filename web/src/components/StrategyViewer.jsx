import React, { useState } from 'react'
import {
  Box,
  TextField,
  Button,
  Paper,
  Typography,
  CircularProgress,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material'
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'
import { generateStrategy } from '../services/api'

const StrategyViewer = () => {
  const [problemAnalysis, setProblemAnalysis] = useState('')
  const [numOptions, setNumOptions] = useState(3)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleGenerate = async () => {
    if (!problemAnalysis.trim()) {
      setError('Please enter or paste problem analysis JSON')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      let analysisData
      try {
        analysisData = JSON.parse(problemAnalysis)
      } catch (e) {
        // If not JSON, create a simple analysis object
        analysisData = {
          problem_statement: problemAnalysis,
          raw_analysis: problemAnalysis
        }
      }

      const data = await generateStrategy({
        problem_analysis: analysisData,
        num_options: numOptions
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
        Strategy Generation
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Generate strategic recommendations from problem analysis
      </Typography>

      <Paper sx={{ p: 3, mt: 2 }}>
        <TextField
          fullWidth
          multiline
          rows={8}
          label="Problem Analysis (JSON or text)"
          value={problemAnalysis}
          onChange={(e) => setProblemAnalysis(e.target.value)}
          placeholder="Paste problem analysis JSON or describe the problem..."
          sx={{ mb: 2 }}
        />

        <TextField
          type="number"
          label="Number of Strategy Options"
          value={numOptions}
          onChange={(e) => setNumOptions(parseInt(e.target.value) || 3)}
          inputProps={{ min: 1, max: 5 }}
          sx={{ mb: 2, width: 200 }}
        />

        <Button
          variant="contained"
          onClick={handleGenerate}
          disabled={loading}
          fullWidth
        >
          {loading ? <CircularProgress size={24} /> : 'Generate Strategies'}
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
            Generated Strategies
          </Typography>
          {result.strategies && Array.isArray(result.strategies) ? (
            result.strategies.map((strategy, index) => (
              <Accordion key={index} sx={{ mt: 2 }}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography variant="subtitle1">
                    {strategy.name || `Strategy Option ${index + 1}`}
                  </Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Box component="pre" sx={{ whiteSpace: 'pre-wrap' }}>
                    {JSON.stringify(strategy, null, 2)}
                  </Box>
                </AccordionDetails>
              </Accordion>
            ))
          ) : (
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
          )}
        </Paper>
      )}
    </Box>
  )
}

export default StrategyViewer


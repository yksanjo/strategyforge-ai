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
import { generateReport, exportReport } from '../services/api'

const ReportExporter = () => {
  const [analysisResults, setAnalysisResults] = useState('')
  const [reportType, setReportType] = useState('executive')
  const [format, setFormat] = useState('pdf')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleGenerate = async () => {
    if (!analysisResults.trim()) {
      setError('Please enter analysis results JSON')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      let resultsData
      try {
        resultsData = JSON.parse(analysisResults)
      } catch (e) {
        setError('Invalid JSON format')
        setLoading(false)
        return
      }

      const data = await generateReport({
        analysis_results: resultsData,
        report_type: reportType
      })
      setResult(data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async () => {
    if (!result) {
      setError('Please generate a report first')
      return
    }

    setLoading(true)
    setError(null)

    try {
      let resultsData
      try {
        resultsData = JSON.parse(analysisResults)
      } catch (e) {
        resultsData = { raw: analysisResults }
      }

      const blob = await exportReport(resultsData, format)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `report.${format}`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Report Generation
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Generate and export professional reports from analysis results
      </Typography>

      <Paper sx={{ p: 3, mt: 2 }}>
        <TextField
          fullWidth
          multiline
          rows={10}
          label="Analysis Results (JSON)"
          value={analysisResults}
          onChange={(e) => setAnalysisResults(e.target.value)}
          placeholder="Paste analysis results JSON here..."
          sx={{ mb: 2 }}
        />

        <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>Report Type</InputLabel>
            <Select
              value={reportType}
              label="Report Type"
              onChange={(e) => setReportType(e.target.value)}
            >
              <MenuItem value="executive">Executive</MenuItem>
              <MenuItem value="detailed">Detailed</MenuItem>
              <MenuItem value="presentation">Presentation</MenuItem>
            </Select>
          </FormControl>

          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>Export Format</InputLabel>
            <Select
              value={format}
              label="Export Format"
              onChange={(e) => setFormat(e.target.value)}
            >
              <MenuItem value="pdf">PDF</MenuItem>
              <MenuItem value="pptx">PowerPoint</MenuItem>
              <MenuItem value="docx">Word</MenuItem>
              <MenuItem value="json">JSON</MenuItem>
            </Select>
          </FormControl>
        </Box>

        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            onClick={handleGenerate}
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Generate Report'}
          </Button>
          {result && (
            <Button
              variant="outlined"
              onClick={handleExport}
              disabled={loading}
            >
              Export {format.toUpperCase()}
            </Button>
          )}
        </Box>
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}

      {result && (
        <Paper sx={{ p: 3, mt: 2 }}>
          <Typography variant="h6" gutterBottom>
            Generated Report
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

export default ReportExporter


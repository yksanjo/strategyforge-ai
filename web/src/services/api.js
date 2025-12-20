import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const analyzeProblem = async (data) => {
  const response = await api.post('/api/analyze-problem', data)
  return response.data
}

export const generateStrategy = async (data) => {
  const response = await api.post('/api/generate-strategy', data)
  return response.data
}

export const planTransformation = async (data) => {
  const response = await api.post('/api/plan-transformation', data)
  return response.data
}

export const optimizeOperations = async (data) => {
  const response = await api.post('/api/optimize-operations', data)
  return response.data
}

export const getAIStrategy = async (data) => {
  const response = await api.post('/api/ai-strategy', data)
  return response.data
}

export const generateReport = async (data) => {
  const response = await api.post('/api/generate-report', data)
  return response.data
}

export const exportReport = async (analysisResults, format = 'pdf') => {
  const response = await api.post(
    `/api/export-report?format=${format}`,
    analysisResults,
    { responseType: 'blob' }
  )
  return response.data
}

export default api


import React from 'react'
import {
  Box,
  Typography,
  Timeline,
  TimelineItem,
  TimelineSeparator,
  TimelineConnector,
  TimelineContent,
  TimelineDot,
  Paper
} from '@mui/material'

const RoadmapTimeline = ({ roadmap }) => {
  if (!roadmap || !Array.isArray(roadmap)) {
    return (
      <Paper sx={{ p: 2 }}>
        <Typography variant="body2" color="text.secondary">
          No roadmap data available
        </Typography>
      </Paper>
    )
  }

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Implementation Roadmap
      </Typography>
      <Timeline>
        {roadmap.map((phase, index) => (
          <TimelineItem key={index}>
            <TimelineSeparator>
              <TimelineDot color="primary" />
              {index < roadmap.length - 1 && <TimelineConnector />}
            </TimelineSeparator>
            <TimelineContent>
              <Paper sx={{ p: 2 }}>
                <Typography variant="subtitle1">
                  {phase.name || `Phase ${index + 1}`}
                </Typography>
                {phase.timeline && (
                  <Typography variant="body2" color="text.secondary">
                    Timeline: {phase.timeline}
                  </Typography>
                )}
                {phase.description && (
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    {phase.description}
                  </Typography>
                )}
              </Paper>
            </TimelineContent>
          </TimelineItem>
        ))}
      </Timeline>
    </Box>
  )
}

export default RoadmapTimeline


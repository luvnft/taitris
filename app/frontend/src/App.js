import React, { useState } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import { Container, Grid, TextField, Typography, InputAdornment, IconButton, Card } from '@mui/material';

import Layout from './components/Layout';
import { theme } from './components/theme';

import SendIcon from '@mui/icons-material/Send';
import axios from 'axios';
import './App.css';

function App() {
  const [objective, setObjective] = useState('');
  const [result, setResult] = useState('');
  const [showResults, setShowResults] = useState(false);

  const handleRunScript = async () => {
    try {
      setShowResults(true); // This will trigger the UI to display the result next to the text box
      const response = await axios.post('http://localhost:5001/runscript', { objective });
      setResult(response.data);
    } catch (error) {
      console.error('Error running script:', error);
      setResult('Error running script');
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      handleRunScript();
    }
  };

  return (
    <Layout>
      <ThemeProvider theme={theme}>
        <Container maxWidth="lg" sx={{ padding: '4% 0', textAlign: 'center' }}>
        <Typography variant="h4" gutterBottom sx={{ mb: 6, color: theme.palette.text.secondary }}>
      <span style={{ fontFamily: 'Pacifico, cursive' }}>InfluAI</span> - Influencer Marketing Automation
    </Typography>
    </Container>
    <Container maxWidth="lg" sx={{ padding: '0% 0', textAlign: 'left' }}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={showResults ? 4 : 12}>
              <Card variant="outlined" sx={{ p: 2, mx: 'auto', mb: 3, backgroundColor: theme.palette.background.paper, color: theme.palette.text.primary }}>
                <TextField
                  multiline
                  rows={4}
                  fullWidth
                  label="Describe your campaign"
                  variant="outlined"
                  value={objective}
                  onChange={(e) => setObjective(e.target.value)}
                  onKeyPress={handleKeyPress}
                  autoComplete="off"
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton onClick={handleRunScript} edge="end">
                          <SendIcon />
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                  sx={{ input: { color: theme.palette.text.primary } }}
                />
              </Card>
            </Grid>
            {showResults && (
              <Grid item xs={12} md={8}>
                <Card sx={{ p: 2, backgroundColor: theme.palette.background.paper, color: theme.palette.text.primary }}>
                  <Typography variant="subtitle1" gutterBottom>
                    Results:
                  </Typography>
                  <pre>{result}</pre>
                </Card>
              </Grid>
            )}
          </Grid>
        </Container>
      </ThemeProvider>
    </Layout>
  );
}

export default App;

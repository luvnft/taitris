// src/theme.js
import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    type: 'dark',
    primary: {
      main: '#0dafff',
    },
    background: {
      default: '#121212',
      paper: '#323232',
    },
    text: {
      primary: '#ccc',
      secondary: '#0dafff',
    },
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
    h4: {
      fontSize: '2.5rem',
      fontWeight: 400,
    },
  },
  components: {
    MuiTextField: {
      styleOverrides: {
        root: {
          borderRadius: '30px',
          backgroundColor: '#222',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          minWidth: '40px',
        },
      },
    },
  },
});

export default theme;

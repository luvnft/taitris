import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
    navbar: {
      mode: 'dark', // Switches the palette to dark mode.
      primary: {
        main: '#00acc1', // Cyan for a vibrant, noticeable primary action color
      },
      background: {
        default: '#0a192f', // Deep navy as the main background, adds depth
        paper: '#112240', // Slightly lighter navy for elements like cards and paper
      },
      text: {
        primary: '#e0e0e0', // Off-white for primary text, ensuring good contrast
        secondary: '#8892b0', // Softer blue-grey for less emphasized text
      },
    },
    palette: {
      mode: 'dark', // Keeps dark mode.
      primary: {
        main: '#00acc1', // Same vibrant cyan as in the navbar
      },
      background: {
        default: '#0a192f', // Matching deep navy for consistency
        paper: '#112240', // Consistent with navbar paper color
      },
      text: {
        primary: '#e0e0e0', // Consistent off-white for readability
        secondary: '#8892b0', // Consistent blue-grey for uniformity
      },
    },
    typography: {
      fontFamily: 'Roboto, Arial, sans-serif', // Slightly more modern font choice
      h4: {
        fontWeight: 600,
        color: '#ccd6f6', // Soft light blue for headings to enhance visibility
      },
      subtitle1: {
        fontSize: '1rem',
        color: '#8892b0', // Matches secondary text color for style cohesion
      },
    },
  });

import * as React from 'react';
import { theme } from './theme';
import { AppBar, Box, Toolbar, Button, IconButton, Typography, Drawer, List, ListItem, ListItemText, useMediaQuery, useTheme } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import CloseIcon from '@mui/icons-material/Close';
import Brightness4Icon from '@mui/icons-material/Brightness4'; // Icon for dark mode
import Brightness7Icon from '@mui/icons-material/Brightness7'; // Icon for light mode

const Layout = ({ children }) => {
  const [drawerOpen, setDrawerOpen] = React.useState(false);
  const [isDarkMode, setDarkMode] = React.useState(true); // State to track theme mode
  const muiTheme = useTheme();
  const isLargeScreen = useMediaQuery(muiTheme.breakpoints.up('md'));

  const toggleDrawer = (open) => (event) => {
    if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
      return;
    }
    setDrawerOpen(open);
  };

  const toggleTheme = () => {
    setDarkMode(!isDarkMode); // Toggle between dark and light mode
  };

  const handleMainAreaClick = () => {
    if (drawerOpen) {
      setDrawerOpen(false);
    }
  };

  const drawerContent = (
    <Box
      sx={{
        width: 250,
        bgcolor: theme.navbar.background.default,
        paddingTop: 5
      }}
      role="presentation"
      onClick={toggleDrawer(false)}
      onKeyDown={toggleDrawer(false)}
    >
      <IconButton
        onClick={toggleDrawer(false)}
        sx={{ marginLeft: 'auto' }}
      >
        <CloseIcon sx={{ color: theme.navbar.text.primary }}/> 
      </IconButton>
      <List>
        {['Home', 'Campaign', 'Admin'].map((text) => (
          <ListItem button key={text}>
            <ListItemText primary={text} sx={{ color: theme.navbar.text.primary }} />
          </ListItem>
        ))}
      </List>
    </Box>
  );

  const mainContentStyle = {
    flexGrow: 1,
    bgcolor: isDarkMode ? theme.palette.background.default : '#fff', // dark or light background
    color: isDarkMode ? theme.palette.text.primary : '#000', // dark or light text
    minHeight: '100vh',
    transition: 'all 0.3s' // smooth transition for theme change
  };

  return (
    // <Box sx={{ flexGrow: 1 }} onClick={handleMainAreaClick}>
    <Box sx={mainContentStyle} onClick={handleMainAreaClick}>
      <AppBar position="static" sx={{ color: theme.navbar.text.primary, backgroundColor: theme.navbar.background.default }}>
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
            onClick={() => setDrawerOpen(!drawerOpen)}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontFamily: 'Roboto, Pacifico, cursive' }}>
           InfluAI
          </Typography>
          <IconButton
            color="inherit"
            onClick={toggleTheme}
            sx={{ ml: 'auto' }}
          >
            {isDarkMode ? <Brightness7Icon /> : <Brightness4Icon />}
          </IconButton>
          {/* <Button color="inherit">Login</Button> */}
        </Toolbar>
      </AppBar>
      <Drawer
        variant={isLargeScreen ? 'persistent' : 'temporary'}
        anchor="left"
        open={drawerOpen}
        onClose={toggleDrawer(false)}
        ModalProps={{
          keepMounted: true, // Better open performance on mobile.
        }}
        sx={{
          width: 250,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: 250,
            boxSizing: 'border-box',
            bgcolor: theme.navbar.background.default,
          },
        }}
      >
        {drawerContent}
      </Drawer>
      <Box sx={{ p: 3 }}>
        {React.Children.map(children, child => {
          // Clone each child and pass the `themeMode` prop
          return React.cloneElement(child, { themeMode: isDarkMode ? 'dark' : 'bright' });
        })}
      </Box>
    </Box>
  );
}

export default Layout;

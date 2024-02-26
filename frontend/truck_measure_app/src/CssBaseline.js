import React from 'react';
import { CssBaseline, GlobalStyles } from '@mui/material';

const GlobalCss = () => (
  <>
    <CssBaseline />
    <GlobalStyles
      styles={(theme) => ({
        body: {
          backgroundColor: theme.palette.background.default, // Use the theme's default background color
          color: theme.palette.text.primary,
        },
      })}
    />
  </>
);

export default GlobalCss;

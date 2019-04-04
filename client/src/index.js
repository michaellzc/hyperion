import React from 'react';
import ReactDOM from 'react-dom';
import App from './app';

import { progressBarFetch, setOriginalFetch } from 'react-fetch-progressbar';

// Let react-fetch-progressbar know what the original fetch is.
setOriginalFetch(window.fetch);

/*
  Now override the fetch with progressBarFetch, so the ProgressBar
  knows how many requests are currently active.
*/
window.fetch = progressBarFetch;

ReactDOM.render(<App />, document.getElementById('root'));

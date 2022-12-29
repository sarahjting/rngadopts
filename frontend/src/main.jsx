import axios from "axios";
import React from "react";
import ReactDOM from "react-dom/client";
import App from "App";
import {BrowserRouter} from 'react-router-dom';

import "index.css";

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);

axios.defaults.baseURL= window.APP_URL + "/api";
axios.defaults.withCredentials = true;
axios.defaults.xsrfHeaderName = 'x-csrftoken'
axios.defaults.xsrfCookieName = 'csrftoken'

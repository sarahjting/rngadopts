/**
=========================================================
* Soft UI Dashboard React - v4.0.0
=========================================================
* Product Page: https://www.creative-tim.com/product/soft-ui-dashboard-react
* Copyright 2022 Creative Tim (https://www.creative-tim.com)
Coded by www.creative-tim.com
 =========================================================
* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/

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

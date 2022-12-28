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
import { BrowserRouter } from "react-router-dom";
import App from "./App"; 
import { SoftUIControllerProvider } from "./context";

ReactDOM.createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <SoftUIControllerProvider>
      <App />
    </SoftUIControllerProvider>
  </BrowserRouter>,
  document.getElement
)

axios.defaults.baseURL = window.APP_URL

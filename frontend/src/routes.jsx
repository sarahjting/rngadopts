import LoginPage from "pages/auth/login";
import DashboardPage from "pages/dashboard";
import { Navigate } from "react-router-dom";

const routes = [
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/adopts/create",
    element: <DashboardPage />,
  },
  {
    path: "/dashboard",
    element: <DashboardPage />,
  },
  {
    path: "*",
    element: <Navigate to="/dashboard" />
  },
];

export default routes;

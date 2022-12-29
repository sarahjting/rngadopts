import LoginPage from "pages/auth/login";
import DashboardPage from "pages/dashboard";
import { Navigate } from "react-router-dom";
import AdoptCreatePage from "pages/adopts/create";
import AdoptDetailPage from "pages/adopts/detail";

const routes = [
  {
    name: "login",
    path: "/login",
    element: <LoginPage />,
  },
  {
    name: "adopts_create",
    path: "/adopts/create",
    element: <AdoptCreatePage />,
  },
  {
    name: "adopts_detail",
    path: "/adopts/:id",
    element: <AdoptDetailPage />,
  },
  {
    name: "dashboard",
    path: "/dashboard",
    element: <DashboardPage />,
  },
  {
    path: "*",
    element: <Navigate to="/dashboard" />
  },
];

export default routes;

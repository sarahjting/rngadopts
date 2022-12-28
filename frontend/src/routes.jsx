import DashboardPage from "pages/dashboard";
import SpaceShip from "components/Icons/SpaceShip";

const routes = [
  {
    type: "collapse",
    name: "Dashboard",
    key: "dashboard",
    route: "/dashboard",
    icon: <SpaceShip size="12px" />,
    component: <DashboardPage />,
    noCollapse: true,
  },
];

export default routes;

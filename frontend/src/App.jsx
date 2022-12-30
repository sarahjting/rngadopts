import { useEffect, useState } from "react";
import { Routes, Route, useNavigate, useLocation } from "react-router-dom";
import routes from "routes";
import axios from "axios";
import DefaultLayout from "./layouts/DefaultLayout";
import AppContext from "./context";

export default function App() {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [toast, setToast] = useState(null);
  const [breadcrumbs, setBreadcrumbs] = useState([]);

  useEffect(() => {
    document.documentElement.scrollTop = 0;
    document.scrollingElement.scrollTop = 0;
  }, [pathname]);

  useEffect(() => {
    axios.get('me')
      .then((data) => data.data)
      .then((user) => {
        setUser(user || {id: null})
      });
  }, [])

  useEffect(() => {
    if (user && !user.id) {
      navigate('login')
    }
  }, [user, pathname])

  const getRoutes = (routes) =>
    routes.map(({name, path, element}, i) => <Route exact name={name} path={path} element={element} key={i} />);

  return (
    <AppContext.Provider value={{ 
        user, 
        setUser, 
        breadcrumbs,
        setBreadcrumbs,
        toast, 
        popToast: () => {
          if (toast) {
            clearTimeout(toast.timeoutHandle);
          }
          setToast(null);
        },
        pushToast: (message, type = 'info') => {
          if (toast) {
            clearTimeout(toast.timeoutHandle);
          }
          setToast({
            message,
            type,
            timeoutHandle: setTimeout(() => {
              setToast(null);
            }, 10000),
          })
        },
      }}>
      <DefaultLayout>
        <Routes>
          {getRoutes(routes)}
        </Routes>
      </DefaultLayout>
    </AppContext.Provider>
  );
}
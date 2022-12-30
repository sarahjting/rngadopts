import { createContext } from "react";

const AppContext = createContext({
    auth: null,
    setAuth: () => {},
    toast: null,
    breadcrumbs: [],
    setBreadcrumbs: () => {},
});

export default AppContext;

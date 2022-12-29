import { createContext } from "react";

const AppContext = createContext({
    auth: null,
    setAuth: () => {},
    toast: null,
});

export default AppContext;

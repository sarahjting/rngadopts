import { createContext } from "react";

const AppContext = createContext({
    user: null,
    setUser: () => {},
});

export default AppContext;

import { useContext } from "react";
import AppContext from "../context";
import { Link } from "react-router-dom";

export default function DefaultLayout({children}) {
    const {user} = useContext(AppContext);

    const userWidget = user && user.id && (
        <div className="flex-none">
            <div className="dropdown dropdown-end">
                <label tabIndex={0} className="btn btn-ghost btn-circle avatar">
                    <div className="w-10 rounded-full">
                        <img src="https://placeimg.com/80/80/people" />
                    </div>
                </label>
                <ul tabIndex={0} className="menu menu-compact dropdown-content mt-3 p-2 shadow bg-base-100 rounded-box w-52 bg-base-300">
                    <li><a href={APP_URL + "/auth/logout/"}>Logout</a></li>
                </ul>
            </div>
        </div>
    )

    return user ? (
        <div>
            <div className="navbar bg-base-100">
                <div className="flex-1">
                    <Link to="dashboard" className="btn btn-ghost normal-case text-xl">rngadopts</Link>
                </div>
                {userWidget}
            </div>
            <div className="m-auto py-2 px-4 lg:w-1/2">
                {children}
            </div>
        </div>
    ) : (
        <>Loading...</>
    );
  }
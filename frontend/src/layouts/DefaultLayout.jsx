import { useContext, useState } from "react";
import AppContext from "../context";
import { Link } from "react-router-dom";

export default function DefaultLayout({children}) {
  const {user} = useContext(AppContext);
  const [isUserCollapsed, setIsUserCollapsed] = useState(true);

  const userWidget = user && user.id && (
    <>
      <button type="button" className="flex mr-3 text-sm bg-gray-800 rounded-full md:mr-0 focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-600" id="user-menu-button" aria-expanded="false" data-dropdown-toggle="user-dropdown" data-dropdown-placement="bottom">
        <span className="sr-only">Open user menu</span>
        <img className="w-8 h-8 rounded-full" src={user.avatar_url} alt="user photo" onClick={() => setIsUserCollapsed(!isUserCollapsed)} />
      </button>
      <a href={APP_URL + "/auth/logout/"} className="block px-4 py-2 text-sm text-gray-700">Logout</a>
    </>
  );

  return user ? (
    <>
      <nav className="bg-white border-gray-200 px-2 sm:px-4 py-2.5 rounded dark:bg-gray-900">
        <div className="container flex flex-wrap items-center justify-between mx-auto">
          <Link to="dashboard" className="flex items-center">
              <span className="self-center text-xl font-semibold whitespace-nowrap dark:text-white">rngadopts</span>
          </Link>
          <div className="flex items-center md:order-2">
            {userWidget}
            <button data-collapse-toggle="mobile-menu-2" type="button" className="inline-flex items-center p-2 ml-1 text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600" aria-controls="mobile-menu-2" aria-expanded="false">
              <span className="sr-only">Open main menu</span>
              <svg className="w-6 h-6" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"></path></svg>
            </button>
          </div>
        </div>
      </nav>

      <div className="m-auto py-2 px-4 lg:w-1/2">
          {children}
      </div>
    </>
  ) : (<>Loading...</>);
}

import { useContext, useState } from "react";
import AppContext from "../context";
import { Link } from "react-router-dom";

export default function DefaultLayout({children}) {
  const {user, toast, popToast} = useContext(AppContext);
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

  const toastBgColor = {info: 'bg-white', success: 'bg-green-500', danger: 'bg-red-500'}[toast?.type];
  const toastTextColor = {info: 'text-gray-500', success: 'text-green-200', danger: 'text-red-200'}[toast?.type];
  const toastIconBgColor = {info: 'bg-blue-100', success: 'bg-green-400', danger: 'bg-red-600'}[toast?.type];
  const toastIconTextColor = {info: 'text-blue-500', success: 'text-green-500', danger: 'text-red-500'}[toast?.type];
  const toastWidget = toast && (
    <div onClick={() => popToast()} className={`absolute bottom-5 right-5 flex items-center p-4 w-full max-w-xs ${toastBgColor} ${toastTextColor} rounded-lg shadow hover:cursor-pointer`} role="alert">
      <div className={`inline-flex flex-shrink-0 justify-center items-center w-8 h-8 ${toastIconBgColor} ${toastIconTextColor} rounded-lg`}>
        <svg aria-hidden="true" className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fillRule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z" clipRule="evenodd"></path></svg>
        <span className="sr-only">Fire icon</span>
      </div>
      <div className="ml-3 text-sm font-normal">{toast.message}</div>
    </div>
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
              <svg className="w-6 h-6" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fillRule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd"></path></svg>
            </button>
          </div>
        </div>
      </nav>

      <div className="m-auto py-2 px-4 lg:w-1/2">
          {children}
      </div>

      {toastWidget}
    </>
  ) : (<>Loading...</>);
}

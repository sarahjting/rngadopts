import { Link } from "react-router-dom";
import { useContext } from "react";
import CaretRightIcon from "components/icons/CaretRightIcon";
import HomeIcon from "components/icons/HomeIcon";
import AppContext from "context";

export default function GeneralBreadcrumbs() {
    const {breadcrumbs} = useContext(AppContext);
    return (
        <nav  className="flex mb-4" aria-label="Breadcrumb">
            <ol  className="inline-flex items-center space-x-1 md:space-x-3">
                <li  className="inline-flex items-center">
                    <Link to="dashboard"  className="inline-flex items-center text-sm font-medium text-gray-700 hover:text-gray-900">
                        <HomeIcon className="text-gray-400 mr-2" />
                        Dashboard
                    </Link>
                </li>
                {breadcrumbs.map(({to, title, onClick=(() => {})}, i) => (
                    <li key={i} onClick={onClick}>
                        <div className="flex items-center">
                            <CaretRightIcon className="text-gray-400" />
                            <Link to={to}  className={`ml-1 text-sm font-medium ${i == breadcrumbs.length - 1 ? "text-gray-500" : "text-gray-700"} hover:text-gray-900 md:ml-2`}>
                                {title}
                            </Link>
                        </div>
                    </li>
                ))}
            </ol>
        </nav>
    );
}
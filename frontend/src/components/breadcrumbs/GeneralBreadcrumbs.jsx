import { Link } from "react-router-dom";
import CaretRightIcon from "../icons/CaretRightIcon";
import HomeIcon from "../icons/HomeIcon";

export default function GeneralBreadcrumbs({breadcrumbs = []}) {
    return (
        <nav  className="flex mb-4" aria-label="Breadcrumb">
            <ol  className="inline-flex items-center space-x-1 md:space-x-3">
                <li  className="inline-flex items-center">
                    <Link to="dashboard"  className="inline-flex items-center text-sm font-medium text-gray-700 hover:text-gray-900">
                        <HomeIcon className="text-gray-400 mr-2" />
                        Dashboard
                    </Link>
                </li>
                {breadcrumbs.map((breadcrumb, i) => (
                    <li key={i}>
                        <div className="flex items-center">
                            <CaretRightIcon className="text-gray-400" />
                            <Link to={breadcrumb.to}  className={`ml-1 text-sm font-medium ${i == breadcrumbs.length - 1 ? "text-gray-500" : "text-gray-700"} hover:text-gray-900 md:ml-2`}>
                                {breadcrumb.title}
                            </Link>
                        </div>
                    </li>
                ))}
            </ol>
        </nav>
    );
}
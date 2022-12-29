import { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

export default function DashboardPage() {
    const [adopts, setAdopts] = useState(null);

    useEffect(() => {
        axios.get('adopts/')
            .then(data => data.data)
            .then(adopts => {
                setAdopts(adopts);
            });
    }, [])
    
    const createButton = window.APP_FLAGS.adopts_creation && (
        <div className="text-right mb-3">
            <Link to="/adopts/create" className="text-white bg-blue-500 hover:bg-blue-600 font-medium rounded-lg text-sm px-5 py-2.5 text-center">
                Create adopt
            </Link>
        </div>
    );

    if (adopts === null) {
        return (<>Loading...</>);
    }

    if (adopts.length === 0) {
        return (
            <>
                {createButton}
                <p>You do not have any adopts registered.</p>
            </>
        )
    }

    return (
        <>
            {createButton}
            <div className="overflow-x-auto relative">
                <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                        <tr>
                            <th className="py-3 px-6">Adopt name</th>
                            <th className="py-3 px-6">Adopt alias (used for Discord commands)</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                    {adopts.map((adopt, key) => (
                        <tr key={key}>
                            <td className="py-4 px-6">
                                {adopt.name}
                            </td>
                            <td className="py-4 px-6">
                                {adopt.short_name}
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </>
    );
}
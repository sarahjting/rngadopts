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
        <div className="text-right mb-2">
            <Link to="/adopts/create" className="btn btn-primary btn-sm">Create adopt</Link>
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
            <table className="table w-full">
                <thead>
                    <tr>
                        <th>Adopt name</th>
                        <th>Adopt alias (used for Discord commands)</th>
                    </tr>
                </thead>
                {adopts.map((adopt, key) => (
                    <tr key={key}>
                        <td>
                            {adopt.name}
                        </td>
                        <td>
                            {adopt.short_name}
                        </td>
                    </tr>
                ))}
            </table>
        </>
    );
}
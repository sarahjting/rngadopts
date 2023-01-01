import { useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import AppContext from "context";
import AdoptForm from "./components/forms/AdoptForm";

export default function AdoptCreatePage() {
    const {setBreadcrumbs} = useContext(AppContext);
    const navigate = useNavigate();
    
    useEffect(() => {
        if (!window.APP_FLAGS.adopts_creation) {
            navigate('dashboard')
        }
        setBreadcrumbs([{to: `/adopts/create`, title: "Create adopt"}]);
    }, [])

    return (
        <div className="max-w-md w-96 m-auto">
            <AdoptForm onSubmitted={(adopt) => navigate(`adopts/${adopt.id}`)} />
        </div>
    );
}
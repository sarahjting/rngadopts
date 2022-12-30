import { useState, useEffect, useContext } from "react";
import AppContext from "context";
import AdoptForm from "./forms/AdoptForm";

export default function AdoptBasicsPanel({adopt, onSubmitted = (() => {})}) {
    const {setBreadcrumbs} = useContext(AppContext);

    useEffect(() => {
        setBreadcrumbs([
            {to: `/adopts/${adopt.id}`, title: adopt.name},
            {to: `/adopts/${adopt.id}`, title: "Basics"},
        ]);
    }, [adopt]);

    return (
        <>
            <AdoptForm adopt={adopt} onSubmitted={onSubmitted} />
        </>
    );
}

import { useState, useEffect } from "react";
import axios from "axios";
import GenePoolsPanelForm from "./GenePoolsPanelForm";

export default function GenePoolsPanel({adopt, colorPools, onSubmitted = (() => {})}) {
    const [currentGenePool, setCurrentGenePool] = useState(null);
    const [genePools, setGenePools] = useState(null);
    const [showModal, setShowModal] = useState(false);

    useEffect(() => {
        reloadGenePools();
    }, [])
    
    function reloadGenePools() {
        axios.get(`adopts/${adopt.id}/gene-pools`)
            .then(data => setGenePools(data.data));
    }

    function submitted() {
        setShowModal(false);
        reloadGenePools();
        onSubmitted();
    }

    function pushCreateModal() {
        setCurrentGenePool(null);
        setShowModal(true);
    }

    function pushUpdateModal(genePool) {
        setCurrentGenePool(genePool);
        setShowModal(true);
    }

    if (colorPools && colorPools.length === 0) {
        return (<div>Add color pools in the "Color pools" tab first.</div>)
    }

    return genePools ? (
        <div>
            {genePools.length ? (
            <div className="overflow-x-auto relative rounded-lg mb-3">
                <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-100 border-b border-gray-50">
                        <tr>
                            <th className="py-3 px-6">Gene pool</th>
                            <th className="py-3 px-6">Type</th>
                            <th className="py-3 px-6">Color pool</th>
                            <th className="py-3 px-6">Sort</th>
                        </tr>
                    </thead>
                    <tbody className="bg-gray-50 border-b">
                    {genePools.map((genePool, key) => (
                        <tr key={key} className="border-b border-gray-100">
                            <td className="py-4 px-6">
                                <button className="text-blue-500" onClick={() => pushUpdateModal(genePool)}>
                                    {genePool.name}
                                    <span className={`inline-flex justify-center items-center ml-2 w-4 p-3 h-4 text-xs font-semibold ${genePool.genes_count ? "text-blue-800 bg-blue-200" : "text-red-800 bg-red-200"} rounded-full`}>
                                        {genePool.genes_count}
                                    </span>
                                </button>
                            </td>
                            <td className="py-4 px-6">
                                {genePool.type}
                            </td>
                            <td className="py-4 px-6">
                                {genePool.color_pool ? genePool.color_pool.name : 'None'}
                            </td>
                            <td className="py-4 px-6">
                                {genePool.sort}
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
            ) : (<div className="mb-3">No gene pools have been added to this adopt yet.</div>)}
            <button className="text-white bg-blue-500 hover:bg-blue-600 font-medium rounded-lg text-sm px-5 py-2.5 text-center w-full" onClick={pushCreateModal}>
                Add new gene pool
            </button>
            <GenePoolsPanelForm
                adopt={adopt} 
                colorPools={colorPools} 
                genePool={currentGenePool}
                show={showModal} 
                onSubmitted={submitted} 
                onClose={() => 
                setShowModal(false)}
            ></GenePoolsPanelForm>
        </div>
    ) : (<>Loading...</>);
}
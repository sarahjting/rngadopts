import { useState } from "react";
import GenePoolFormModal from "pages/adopts/components/modals/GenePoolFormModal";
import { SCREENS } from "./GenePoolsPanel";

export default function GenePoolsPanelIndex({adopt, colorPools, genePools, onSwitchScreen, onSubmitted = (() => {})}) {
    const [showModal, setShowModal] = useState(false);

    function submitted() {
        setShowModal(false);
        onSubmitted();
    }

    return (
        <div>
            {genePools.length ? (
            <div className="overflow-x-auto relative">
                <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-100 border-b border-gray-50">
                        <tr>
                            <th className="py-3 px-6">Gene pool</th>
                            <th className="py-3 px-6">Slug</th>
                            <th className="py-3 px-6">Type</th>
                            <th className="py-3 px-6">Color pool</th>
                        </tr>
                    </thead>
                    <tbody className="bg-gray-50 border-b">
                    {genePools.map((genePool, key) => (
                        <tr key={key} className="border-b border-gray-100">
                            <td className="py-4 px-6">
                                <button className="text-blue-500" onClick={() => onSwitchScreen(SCREENS.GENE_POOLS_DETAIL, genePool)}>
                                    {genePool.name}
                                    <span className={`inline-flex justify-center items-center ml-2 w-4 p-3 h-4 text-xs font-semibold ${genePool.genes_count ? "text-blue-800 bg-blue-200" : "text-red-800 bg-red-200"} rounded-full`}>
                                        {genePool.genes_count}
                                    </span>
                                </button>
                            </td>
                            <td className="py-4 px-6">
                                {genePool.slug}
                            </td>
                            <td className="py-4 px-6">
                                {genePool.type}
                            </td>
                            <td className="py-4 px-6">
                                {genePool.color_pool ? genePool.color_pool.name : 'None'}
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
            ) : (<div className="p-8">No gene pools have been added to this adopt yet.</div>)}
            <button className="text-white bg-blue-500 hover:bg-blue-600 font-medium rounded-b-lg text-sm px-5 py-2.5 text-center w-full" onClick={() => setShowModal(true)}>
                Add new gene pool
            </button>
            <GenePoolFormModal
                adopt={adopt} 
                colorPools={colorPools} 
                show={showModal} 
                onSubmitted={submitted} 
                onClose={() => 
                setShowModal(false)}
            ></GenePoolFormModal>
        </div>
    );
}
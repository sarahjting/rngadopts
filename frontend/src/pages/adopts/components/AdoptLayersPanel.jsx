import { useState } from "react";
import AdoptLayerFormModal from "pages/adopts/components/modals/AdoptLayerFormModal";

export default function AdoptLayersPanel({adopt, genePools, onSubmitted = (() => {})}) {
    const [showModal, setShowModal] = useState(false);
    const [currentAdoptLayer, setCurrentAdoptLayer] = useState(null);

    function submitted() {
        setShowModal(false);
        onSubmitted();
    }

    function pushCreateModal() {
        setCurrentAdoptLayer(null);
        setShowModal(true);
    }

    function pushUpdateModal(adoptLayer) {
        setCurrentAdoptLayer(adoptLayer);
        setShowModal(true);
    }

    return adopt?.adopt_layers ? (
        <div>
            {adopt.adopt_layers.length ? (
            <div className="overflow-x-auto relative rounded-lg mb-3">
                <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-100 border-b border-gray-50">
                        <tr>
                            <th className="py-3 px-6">Layer</th>
                            <th className="py-3 px-6">Type</th>
                            <th className="py-3 px-6">Sort</th>
                            <th className="py-3 px-6"></th>
                        </tr>
                    </thead>
                    <tbody className="bg-gray-50 border-b">
                    {adopt.adopt_layers.map((adoptLayer, key) => (
                        <tr key={key} className="border-b border-gray-100">
                            <td className="py-4 px-6">
                                <img src={adoptLayer.image} />
                            </td>
                            <td className="py-4 px-6">
                                {adoptLayer.type}
                                {adoptLayer.type === "gene" && (<> ({adoptLayer.gene_pool.name})</>)}
                            </td>
                            <td className="py-4 px-6">
                                {adoptLayer.sort}
                            </td>
                            <td className="py-4 px-6 text-right">
                                <button className="btn bg-blue-500 text-white py-1 px-3 rounded-md" onClick={() => pushUpdateModal(adoptLayer)}>
                                    Edit
                                </button>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
            ) : (<div className="mb-3">No layers have been added to this adopt yet.</div>)}
            <button className="text-white bg-blue-500 hover:bg-blue-600 font-medium rounded-lg text-sm px-5 py-2.5 text-center w-full" onClick={pushCreateModal}>
                Add new layer
            </button>
            <AdoptLayerFormModal 
                adopt={adopt} 
                genePools={genePools} 
                adoptLayer={currentAdoptLayer}
                show={showModal} 
                onSubmitted={submitted} 
                onClose={() => 
                setShowModal(false)}
            ></AdoptLayerFormModal>
        </div>
    ) : (<>Loading...</>);
}
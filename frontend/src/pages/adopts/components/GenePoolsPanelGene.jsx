import { useState } from "react";
import GeneLayerFormModal from "pages/adopts/components/modals/GeneLayerFormModal";
import { SCREENS } from "pages/adopts/components/GenePoolsPanel";
import GeneFormModal from "pages/adopts/components/modals/GeneFormModal";
import CaretLeftIcon from "components/icons/CaretLeftIcon";
import PencilIcon from "components/icons/PencilIcon";

const MODALS = {
    UPDATE_GENE: 'UPDATE_GENE',
    CREATE_GENE_LAYER: 'CREATE_GENE_LAYER',
    UPDATE_GENE_LAYER: 'UPDATE_GENE_LAYER',
};

export default function GenePoolsPanelGene({adopt, colorPools, genePool, gene, onSwitchScreen, onSubmitted = (() => {})}) {
    const [modal, setModal] = useState(null);
    const [currentGeneLayer, setCurrentGeneLayer] = useState(null);

    function submitted() {
        setModal(null);
        setCurrentGeneLayer(null);
        onSubmitted();
    }

    function pushUpdateGeneModal() {
        setModal(MODALS.UPDATE_GENE);
    }

    function pushCreateGeneLayerModal() {
        setModal(MODALS.CREATE_GENE_LAYER);
        setCurrentGeneLayer(null);
    }

    function pushUpdateGeneLayerModal(geneLayer) {
        setModal(MODALS.UPDATE_GENE_LAYER);
        setCurrentGeneLayer(geneLayer);
    }

    if (!adopt || !colorPools || !genePool || !gene) {
        return (<>Loading...</>);
    }

    return (
        <div>
            <div className="flex justify-between">
                <h1 className="flex items-center">
                    Gene: {gene.name}
                    <button className="ml-2 p-1 text-xs text-blue-500" onClick={pushUpdateGeneModal}>
                        <PencilIcon />
                    </button>
                </h1>
                <button className="flex items-center text-sm mb-2" onClick={() => onSwitchScreen(SCREENS.GENE_POOLS_DETAIL, genePool)}>
                    <CaretLeftIcon className="text-gray-400 mr-2" /> 
                    Back to {genePool.name}
                </button>
            </div>
            <hr className="mb-3" />
            {gene.gene_layers.length ? (
            <div className="overflow-x-auto relative rounded-lg mb-3">
                <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-100 border-b border-gray-50">
                        <tr>
                            <th className="py-3 px-6">Layer</th>
                            <th className="py-3 px-6">Type</th>
                            <th className="py-3 px-6">Sort</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody className="bg-gray-50 border-b">
                    {gene.gene_layers.map((geneLayer, key) => (
                        <tr key={key} className="border-b border-gray-100">
                            <td>
                                <img src={geneLayer.image} />
                            </td>
                            <td className="py-4 px-6">
                                {geneLayer.type}
                            </td>
                            <td className="py-4 px-6">
                                {geneLayer.sort}
                            </td>
                            <td>
                                <button className="btn bg-blue-500 text-white py-1 px-3 rounded-md" onClick={() => pushUpdateGeneLayerModal(geneLayer)}>
                                    Edit
                                </button>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
            ) : (<div className="mb-3">No layers have been added to this gene yet.</div>)}
            <button className="text-white bg-blue-500 hover:bg-blue-600 font-medium rounded-lg text-sm px-5 py-2.5 text-center w-full" onClick={pushCreateGeneLayerModal}>
                Add new layer
            </button>
            <GeneFormModal
                adopt={adopt} 
                colorPools={colorPools} 
                genePool={genePool}
                gene={gene}
                show={modal === MODALS.UPDATE_GENE} 
                onSubmitted={submitted} 
                onClose={() => setModal(null)}
            ></GeneFormModal>
            <GeneLayerFormModal
                adopt={adopt} 
                colorPools={colorPools} 
                genePool={genePool}
                gene={gene}
                geneLayer={currentGeneLayer}
                show={modal === MODALS.UPDATE_GENE_LAYER || modal === MODALS.CREATE_GENE_LAYER} 
                onSubmitted={submitted} 
                onClose={() => setModal(null)}
            ></GeneLayerFormModal>
        </div>
    );
}
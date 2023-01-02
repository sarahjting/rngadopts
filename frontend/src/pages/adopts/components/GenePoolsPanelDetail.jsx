import { useState } from "react";
import GenePoolFormModal from "pages/adopts/components/modals/GenePoolFormModal";
import { SCREENS } from "pages/adopts/components/GenePoolsPanel";
import GeneFormModal from "pages/adopts/components/modals/GeneFormModal";
import CaretLeftIcon from "components/icons/CaretLeftIcon";
import PencilIcon from "components/icons/PencilIcon";
import { useEffect } from "react";

const MODALS = {
    UPDATE_GENE_POOL: 'UPDATE_GENE_POOL',
    CREATE_GENE: 'CREATE_GENE',
    UPDATE_GENE: 'UPDATE_GENE',
};

export default function GenePoolsPanelDetail({adopt, colorPools, genePool, onSwitchScreen, onSubmitted = (() => {})}) {
    const [modal, setModal] = useState(null);
    const [currentGene, setCurrentGene] = useState(null);
    const [isInvalidated, setIsInvalidated] = useState(false);

    function submitted() {
        setModal(null);
        onSubmitted();
        setIsInvalidated(true);
    }

    useEffect(() => {
        setIsInvalidated(false); 
    }, [adopt]);

    function pushModal(modalType, gene = null) {
        setModal(modalType);
        setCurrentGene(gene);
    }

    if (isInvalidated) {
        return <div className="p-8">Loading...</div>;
    }

    return (
        <div>
            <div className="bg-gray-100 border-b border-gray-200">
                <button className="flex w-full items-center text-sm p-4" onClick={() => onSwitchScreen(SCREENS.GENE_POOLS_INDEX)}>
                    <CaretLeftIcon className="text-gray-400 mr-2" />  Back
                </button>
            </div>
            <div className="flex justify-between py-4 px-4 border-b border-gray-200">
                Gene pool: {genePool.name}
                <button className="flex p-1 text-xs text-blue-500" onClick={() => pushModal(MODALS.UPDATE_GENE_POOL)}>
                <PencilIcon className="mr-2" /> Edit 
                </button>
            </div>
            {genePool.genes.length ? (
            <div className="overflow-x-auto relative">
                <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-100 border-b border-gray-50">
                        <tr>
                            <th className="py-2 px-2">Name</th>
                            <th className="py-2 px-2">Weight</th>
                            <th className="py-2 px-2">Color pool override</th>
                            <th className="py-2 px-2">Layers</th>
                            <th className="py-2 px-2"></th>
                            <th className="py-2 px-2"></th>
                        </tr>
                    </thead>
                    <tbody className="bg-gray-50 border-b">
                    {genePool.genes.map((gene, key) => (
                        <tr key={key} className="border-b border-gray-100">
                            <td className="py-2 px-2">
                                <button className="ml-2 text-blue-500" onClick={() => onSwitchScreen(SCREENS.GENES_DETAIL, genePool, gene)}>
                                    {gene.name}
                                </button>
                            </td>
                            <td className="py-2 px-2">
                                {gene.weight}
                            </td>
                            <td className="py-2 px-2">
                                {gene.color_pool ? gene.color_pool.name : '--'}
                            </td>
                            <td className="py-2 px-2">
                                <button className="text-blue-500" onClick={() => onSwitchScreen(SCREENS.GENES_DETAIL, genePool, gene)}>
                                    <span className={`inline-flex justify-center items-center mr-2 w-4 p-3 h-4 text-xs font-semibold ${gene.gene_layers.length ? "text-blue-800 bg-blue-200" : "text-red-800 bg-red-200"} rounded-full`}>
                                        {gene.gene_layers.length}
                                    </span>
                                </button>
                            </td>
                            <td className="py-2 px-2">
                                <button className="flex text-blue-500" onClick={() => pushModal(MODALS.UPDATE_GENE, gene)}>
                                    <PencilIcon className="mr-2" /> Edit 
                                </button>
                            </td>
                            <td className="py-2 px-2">
                                <button className="flex text-blue-500" onClick={() => onSwitchScreen(SCREENS.GENES_DETAIL, genePool, gene)}>
                                    <PencilIcon className="mr-2" /> Layers 
                                </button>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
            ) : (<div className="p-8">No genes have been added to this gene pool yet.</div>)}
            <button className="text-white bg-blue-500 hover:bg-blue-600 font-medium rounded-b-lg text-sm px-5 py-2.5 text-center w-full" onClick={() => pushModal(MODALS.CREATE_GENE)}>
                Add new gene
            </button>
            <GenePoolFormModal
                adopt={adopt} 
                colorPools={colorPools} 
                genePool={genePool}
                show={modal === MODALS.UPDATE_GENE_POOL} 
                onSubmitted={submitted} 
                onClose={() => setModal(null)}
            ></GenePoolFormModal>
            <GeneFormModal
                adopt={adopt} 
                colorPools={colorPools} 
                genePool={genePool}
                gene={currentGene}
                show={modal === MODALS.CREATE_GENE || modal === MODALS.UPDATE_GENE} 
                onSubmitted={submitted} 
                onClose={() => setModal(null)}
            ></GeneFormModal>
        </div>
    );
}
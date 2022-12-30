import { useState, useEffect } from "react";
import axios from "axios";
import GenePoolFormModal from "pages/adopts/components/modals/GenePoolFormModal";
import { SCREENS } from "pages/adopts/components/GenePoolsPanel";
import GeneFormModal from "pages/adopts/components/modals/GeneFormModal";
import CaretLeftIcon from "components/icons/CaretLeftIcon";

const MODALS = {
    UPDATE_GENE_POOL: 'UPDATE_GENE_POOL',
    CREATE_GENE: 'CREATE_GENE',
};

export default function GenePoolsPanelIndex({adopt, colorPools, genePool, onSwitchScreen, onSubmitted = (() => {})}) {
    const [modal, setModal] = useState(null);
    const [genes, setGenes] = useState(null);

    function reloadGenes() {
        axios.get(`adopts/${adopt.id}/gene-pools/${genePool.id}/genes`).then(data => setGenes(data.data));
    }

    useEffect(() => {
        reloadGenes();
    }, []);

    function submitted() {
        setModal(null);
        reloadGenes();
        onSubmitted();
    }

    if (!genes) {
        return (<>Loading...</>);
    }

    return (
        <div>
            <div className="flex justify-between">
                <h1>Gene pool: {genePool.name}</h1>
                <button className="flex items-center text-sm mb-2" onClick={() => onSwitchScreen(SCREENS.GENE_POOLS_INDEX)}>
                <CaretLeftIcon className="text-gray-400 mr-2" /> 
                Back to all gene pools
                </button>
            </div>
            <hr className="mb-3" />
            {genes.length ? (
            <div className="overflow-x-auto relative rounded-lg mb-3">
                <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-100 border-b border-gray-50">
                        <tr>
                            <th className="py-3 px-6">Name</th>
                            <th className="py-3 px-6">Weight</th>
                            <th className="py-3 px-6">Color pool override</th>
                        </tr>
                    </thead>
                    <tbody className="bg-gray-50 border-b">
                    {genes.map((gene, key) => (
                        <tr key={key} className="border-b border-gray-100">
                            <td className="py-4 px-6">
                                <button className="text-blue-500" onClick={() => onSwitchScreen(SCREENS.GENES_DETAIL, genePool, gene)}>
                                    {gene.name}
                                </button>
                            </td>
                            <td className="py-4 px-6">
                                {gene.weight}
                            </td>
                            <td className="py-4 px-6">
                                {gene.color_pool ? gene.color_pool.name : '--'}
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
            ) : (<div className="mb-3">No genes have been added to this gene pool yet.</div>)}
            <button className="text-white bg-blue-500 hover:bg-blue-600 font-medium rounded-lg text-sm px-5 py-2.5 text-center w-full" onClick={() => setModal(MODALS.CREATE_GENE)}>
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
                show={modal === MODALS.CREATE_GENE} 
                onSubmitted={submitted} 
                onClose={() => setModal(null)}
            ></GeneFormModal>
        </div>
    );
}
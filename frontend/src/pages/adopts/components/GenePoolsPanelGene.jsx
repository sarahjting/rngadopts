import { useState, useEffect } from "react";
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

export default function GenePoolsPanelGene({adopt, colorPools, genePools, genePool, gene, onSwitchScreen, onSubmitted = (() => {})}) {
    const [modal, setModal] = useState(null);
    const [currentGeneLayer, setCurrentGeneLayer] = useState(null);
    const [isInvalidated, setIsInvalidated] = useState(false);

    function submitted() {
        setModal(null);
        setCurrentGeneLayer(null);
        onSubmitted();
        setIsInvalidated(true);
    }

    useEffect(() => {
        setIsInvalidated(false);
    }, [adopt]);

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
        return ((<div className="p-8">Loading...</div>));
    }

    const genes = genePools.map((pool) => pool.genes).flat(1);

    function geneLayerRow(geneLayer, key) {
        const requiredGene = genes.find(x => x.id === geneLayer.required_gene_id);
        const requiredGenePool = genePools.find(x => x.id === geneLayer.required_gene_pool_id);
        return (
            <tr key={key} className="border-b border-gray-100">
                <td className="py-4 px-6">
                    <img src={geneLayer.image} />
                </td>
                <td className="py-4 px-6">
                    {geneLayer.type}
                </td>
                <td className="py-4 px-6">
                    {requiredGene && (<>
                        <span className="bg-orange-300 text-white py-2 px-2 mb-2 rounded-md text-center mr-2">Requires {requiredGene.name}</span>
                    </>)}
                    {requiredGenePool && (<>
                        <span className="bg-orange-300 text-white py-2 px-2 mb-2 rounded-md text-center mr-2">Requires {requiredGenePool.name}</span>
                    </>)}
                    {geneLayer.type.substring(0, 5) === "color" ? `Palette ${geneLayer.color_key}` : "--"}
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
        );
    }

    if (isInvalidated) {
        return <div className="p-8">Loading...</div>;
    }

    return (
        <div>
            <div className="bg-gray-100 border-b border-gray-200">
                <button className="flex w-full items-center text-sm p-4" onClick={() => onSwitchScreen(SCREENS.GENE_POOLS_DETAIL, genePool)}>
                    <CaretLeftIcon className="text-gray-400 mr-2" />  Back
                </button>
            </div>
            <div className="flex justify-between py-4 px-4 border-b border-gray-200">
                Gene: {gene.name}
                <button className="flex p-1 text-xs text-blue-500" onClick={() => pushUpdateGeneModal()}>
                <PencilIcon className="mr-2" /> Edit 
                </button>
            </div>
            {gene.gene_layers.length ? (
            <div className="overflow-x-auto relative">
                <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-100 border-b border-gray-50">
                        <tr>
                            <th className="py-3 px-6">Layer</th>
                            <th className="py-3 px-6">Type</th>
                            <th className="py-3 px-6">Palette</th>
                            <th className="py-3 px-6">Sort</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody className="bg-gray-50 border-b">
                    {gene.gene_layers.map((geneLayer, key) => geneLayerRow(geneLayer, key))}
                    </tbody>
                </table>
            </div>
            ) : (<div className="p-8">No layers have been added to this gene yet.</div>)}
            <button className="text-white bg-blue-500 hover:bg-blue-600 font-medium rounded-b-lg text-sm px-5 py-2.5 text-center w-full" onClick={pushCreateGeneLayerModal}>
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
                genePools={genePools}
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
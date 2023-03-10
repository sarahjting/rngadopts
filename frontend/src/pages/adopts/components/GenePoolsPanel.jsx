import { useState, useContext, useEffect } from "react";
import AppContext from "context";
import GenePoolsPanelDetail from "./GenePoolsPanelDetail";
import GenePoolsPanelIndex from "./GenePoolsPanelIndex";
import GenePoolsPanelGene from "./GenePoolsPanelGene";
import axios from "axios";

export const SCREENS = {
    GENE_POOLS_INDEX: "GENE_POOLS_INDEX",
    GENE_POOLS_DETAIL: "GENE_POOLS_DETAIL",
    GENES_DETAIL: "GENE_DETAIL",
};

export default function GenePoolsPanel({adopt, colorPools, genePools, onSubmitted = (() => {})}) {
    const {setBreadcrumbs} = useContext(AppContext);
    const [currentScreen, setCurrentScreen] = useState(SCREENS.GENE_POOLS_INDEX);
    const [currentGenePool, setCurrentGenePool] = useState(null);
    const [currentGene, setCurrentGene] = useState(null);

    useEffect(() => {
        if (currentGenePool) {
            const updatedGenePool = genePools.find(x => x.id === currentGenePool.id);
            setCurrentGenePool(updatedGenePool);
            if (!updatedGenePool) {
                setCurrentScreen(SCREENS.GENE_POOLS_INDEX);
            }
        }
    }, [genePools]);

    useEffect(() => {
        if (currentGene) {
            const updatedGene = currentGenePool.genes.find(x => x.id === currentGene.id);
            setCurrentGene(updatedGene);
            if (!updatedGene) {
                setCurrentScreen(SCREENS.GENE_POOLS_DETAIL);
            }
        }
    }, [currentGenePool]);

    function switchScreen(screen, genePool = null, gene = null) {
        setCurrentGenePool(genePool);
        setCurrentGene(gene);
        setCurrentScreen(screen);
        const breadcrumbs = [
            {to: `/adopts/${adopt.id}`, title: adopt.name},
            {to: `/adopts/${adopt.id}`, title: "Gene pools", onClick: () => switchScreen(SCREENS.GENE_POOLS_INDEX)},
        ];
        if (genePool) {
            breadcrumbs.push({to: `/adopts/${adopt.id}`, title: genePool.name, onClick: () => switchScreen(SCREENS.GENE_POOLS_DETAIL, genePool)});
        }
        if (gene) {
            breadcrumbs.push({to: `/adopts/${adopt.id}`, title: 'Genes', onClick: () => switchScreen(SCREENS.GENE_POOLS_DETAIL, genePool)});
            breadcrumbs.push({to: `/adopts/${adopt.id}`, title: gene.name, onClick: () => switchScreen(SCREENS.GENES_DETAIL, genePool, gene)});
        }
        setBreadcrumbs(breadcrumbs);
    }

    if (colorPools && colorPools.length === 0) {
        return (<div className="p-8">Add color pools in the "Color pools" tab first.</div>)
    }

    // we use a hidden toggle here is because we want the component to be hidden but retain state
    // this is so the user gets taken back to the screen that they were just on with their existing settings after they submit a form
    return (<>
        <div>
            {currentScreen === SCREENS.GENE_POOLS_DETAIL && currentGenePool && (<GenePoolsPanelDetail
                adopt={adopt}
                colorPools={colorPools}
                genePool={currentGenePool}
                onSubmitted={onSubmitted}
                onSwitchScreen={switchScreen}
            ></GenePoolsPanelDetail>)}
            {currentScreen === SCREENS.GENES_DETAIL && currentGenePool && (<GenePoolsPanelGene
                adopt={adopt}
                colorPools={colorPools}
                genePools={genePools}
                genePool={currentGenePool}
                gene={currentGene}
                onSubmitted={onSubmitted}
                onSwitchScreen={switchScreen}
            ></GenePoolsPanelGene>)}
            {currentScreen === SCREENS.GENE_POOLS_INDEX && (<GenePoolsPanelIndex
                adopt={adopt}
                colorPools={colorPools}
                genePools={genePools}
                onSubmitted={onSubmitted}
                onSwitchScreen={switchScreen}
            ></GenePoolsPanelIndex>)}
        </div>
    </>)
}
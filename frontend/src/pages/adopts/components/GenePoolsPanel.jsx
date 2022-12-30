import { useState } from "react";
import GenePoolsPanelDetail from "./GenePoolsPanelDetail";
import GenePoolsPanelIndex from "./GenePoolsPanelIndex";

export const SCREENS = {
    GENE_POOLS_INDEX: "GENE_POOLS_INDEX",
    GENE_POOLS_DETAIL: "GENE_POOLS_DETAIL",
    GENES_DETAIL: "GENE_DETAIL",
};

export default function GenePoolsPanel({adopt, colorPools, genePools, onSubmitted = (() => {})}) {
    const [currentScreen, setCurrentScreen] = useState(SCREENS.GENE_POOLS_INDEX);
    const [currentGenePool, setCurrentGenePool] = useState(null);
    const [currentGene, setCurrentGene] = useState(null);
    
    function switchScreen(screen, genePool = null, gene = null) {
        setCurrentGenePool(genePool);
        setCurrentGene(gene);
        setCurrentScreen(screen);
    }

    if (!genePools || !colorPools || !adopt) {
        return (<>Loading...</>);
    }

    if (colorPools && colorPools.length === 0) {
        return (<div>Add color pools in the "Color pools" tab first.</div>)
    }

    if (currentScreen === SCREENS.GENE_POOLS_DETAIL) {
        return (<GenePoolsPanelDetail
            adopt={adopt}
            colorPools={colorPools}
            genePool={currentGenePool}
            onSubmitted={onSubmitted}
            onSwitchScreen={switchScreen}
        ></GenePoolsPanelDetail>)
    } else if (currentScreen === SCREENS.GENES_DETAIL) {

    } else {
        return (<GenePoolsPanelIndex
            adopt={adopt}
            colorPools={colorPools}
            genePools={genePools}
            onSubmitted={onSubmitted}
            onSwitchScreen={switchScreen}
        ></GenePoolsPanelIndex>)
    }
}
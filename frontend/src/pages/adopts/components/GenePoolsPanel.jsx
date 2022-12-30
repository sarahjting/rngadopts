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
    const [genes, setGenes] = useState(null);
    const [currentScreen, setCurrentScreen] = useState(SCREENS.GENE_POOLS_INDEX);
    const [currentGenePool, setCurrentGenePool] = useState(null);
    const [currentGene, setCurrentGene] = useState(null);

    function reloadGenes() {
        if (currentGenePool) {
            axios.get(`adopts/${adopt.id}/gene-pools/${currentGenePool.id}/genes`).then(data => setGenes(data.data));
        } else {
            setGenes(null);
        }
    }

    useEffect(() => {
        reloadGenes();
    }, []);

    useEffect(() => {
        if (currentGenePool) {
            setCurrentGenePool(genePools.find(x => x.id === currentGenePool.id));
        }
    }, [genePools]);

    useEffect(() => {
        reloadGenes();
    }, [currentGenePool]);

    useEffect(() => {
        if (currentGene) {
            setCurrentGene(genes.find(x => x.id === currentGene.id));
        }
    }, [genes]);
    
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

    if (!genePools || !colorPools || !adopt || (currentGenePool && !genes)) {
        return (<div class="p-8">Loading...</div>);
    }

    if (colorPools && colorPools.length === 0) {
        return (<div class="p-8">Add color pools in the "Color pools" tab first.</div>)
    }

    if (currentScreen === SCREENS.GENE_POOLS_DETAIL) {
        return (<GenePoolsPanelDetail
            adopt={adopt}
            colorPools={colorPools}
            genePool={currentGenePool}
            genes={genes}
            onSubmitted={onSubmitted}
            onSwitchScreen={switchScreen}
        ></GenePoolsPanelDetail>)
    } else if (currentScreen === SCREENS.GENES_DETAIL) {
        return (<GenePoolsPanelGene
            adopt={adopt}
            colorPools={colorPools}
            genePool={currentGenePool}
            gene={currentGene}
            onSubmitted={onSubmitted}
            onSwitchScreen={switchScreen}
        ></GenePoolsPanelGene>)
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
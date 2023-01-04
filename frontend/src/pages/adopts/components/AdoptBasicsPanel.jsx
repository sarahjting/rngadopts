import { useState, useEffect, useContext } from "react";
import AppContext from "context";
import AdoptForm from "./forms/AdoptForm";
import axios from "axios";
import FormSelect from "components/form/FormSelect";

export default function AdoptBasicsPanel({adopt, genePools, colorPools, onSubmitted = (() => {})}) {
    const {setBreadcrumbs} = useContext(AppContext);
    const [currentGen, setCurrentGen] = useState(null);
    const [formGenes, setFormGenes] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        setBreadcrumbs([
            {to: `/adopts/${adopt.id}`, title: adopt.name},
            {to: `/adopts/${adopt.id}`, title: "Basics"},
        ]);
    }, [adopt]);

    useEffect(() => {
        randomize();
    }, [])

    function loaded() {
        setIsLoading(false);
    }

    function slugify(str) {
        return str.toLowerCase().replace(/[^0-9a-z]/gi, '');
    }

    function preview() {
        const url = window.APP_URL 
            + "/gen/" 
            + slugify(adopt.short_name) 
            + "-" 
            + formGenes.filter(gc => gc.enabled).map(gc => `${gc.gene_pool.slug}_${gc.gene.slug}_${gc.color}`).sort().join("-") 
            + ".png";
        if (url !== currentGen.url) {
            setIsLoading(true);
            setCurrentGen({"url": url});
        }
    }

    function randomize() {
        setIsLoading(true);
        axios.post(`adopt-gen/${adopt.id}`).then(data => {
            if (data.data.url === currentGen?.url) {
                setIsLoading(false);
            }
            setCurrentGen(data.data);
            setFormGenes(data.data.dict.gene_colors.map(gc => {
                const gene_pool = genePools.find(x => x.id === gc.gene.gene_pool_id);
                if (!gene_pool) {
                    return null;
                }
                return {
                    gene_pool,
                    gene: gene_pool.genes.find(x => x.id === gc.gene.id),
                    color: gc.color.slug,
                    enabled: true,
                };
            }).filter((x) => x));
        })
    }

    function setFormGene(genePool, gene, color=null, setEnabled=null) {
        const filter = genePool.type === "basic" ? (x => x.gene_pool.id === genePool.id) : (x => x.gene_pool.id === genePool.id && x.gene.id === gene.id);
        const existingGc = formGenes.find(filter);

        const isEnabled = setEnabled ?? existingGc?.enabled;
        setFormGenes([
            ...formGenes.filter((x) => !filter(x)), 
            {
                gene_pool: genePool,
                gene: gene ?? existingGc?.gene,
                color: color ?? existingGc?.color ?? colorPools.find(x => x.id === (formGenes.find(x => x.gene_pool.id === genePool.id)?.gene.color_pool?.id ?? genePool.color_pool.id)).colors_dict[0].slug,
                enabled: isEnabled,
            },
        ]);
    }

    function renderGenePoolRow(key, genePool, gene = null) {
        const selectedGene = gene ?? formGenes.find(x => x.gene_pool.id === genePool.id).gene
        return (
        <tr key={key}>
            <td className="text-sm text-right pr-3">
                {genePool.name}
            </td>
            {gene && (
                <td className="text-sm text-right pr-3" colspan={selectedGene.has_color ? 1 : 2}>
                    <label htmlFor={`gene-${gene.id}`} className="mr-2 text-sm font-medium text-gray-900 dark:text-gray-300">{gene.name}</label>
                    <input 
                        id={`gene-${gene.id}`} 
                        type="checkbox" 
                        checked={formGenes.find(x => x.gene_pool.id === genePool.id && x.gene.id === gene.id)?.enabled} 
                        className="w-4 h-4 text-blue-600 bg-gray-100 rounded border-gray-300 focus:ring-blue-500 focus:ring-2" 
                        onChange={(e) => setFormGene(genePool, gene, null, e.target.checked)}
                    />
                </td>
            )}
            {!gene && (
                <td colspan={selectedGene.has_color ? 1 : 2}>
                    <FormSelect 
                        value={formGenes.find(x => x.gene_pool.id === genePool.id)?.gene.id}
                        options={genePool?.genes.reduce((a, b) => ({
                            ...a,
                            [b.id]: b.name,
                        }), {}) ?? {}}
                        onChange={(e) => setFormGene(genePool, genePool.genes.find(x => `${x.id}` === `${e.target.value}`))}
                    ></FormSelect>
                </td>
            )}
            {selectedGene.has_color && (
            <td>
                <FormSelect 
                    value={formGenes.find(x => x.gene_pool.id === genePool.id && (gene === null || x.gene.id === gene.id))?.color}
                    options={colorPools.find(x => x.id === (formGenes.find(x => x.gene_pool.id === genePool.id)?.gene.color_pool?.id ?? genePool.color_pool.id))
                        ?.colors_dict
                        ?.reduce((a, b) => ({
                            ...a,
                            [b.slug]: b.name,
                        }), {}) ?? {}}
                    onChange={(e) => setFormGene(genePool, gene, e.target.value)}
                ></FormSelect>
            </td>
            )}
        </tr>
        );
    }

    const genePoolTable = genePools.map(
            (genePool, k) => genePool.type === "basic" ? [renderGenePoolRow(k, genePool)] 
                : genePool.genes.map((gene, kk) => renderGenePoolRow(`${k}-${kk}`, genePool, gene))
        ).flat();
        
    return (
        <div className="flex">
            <div className="border-r p-8">
                <h5>Basic info</h5>
                <hr className="mb-4" />
                <AdoptForm adopt={adopt} onSubmitted={onSubmitted} />
            </div>
            <div className="grow p-8">
                <h5>Sandbox</h5>
                <hr className="mb-4"/>
                {!currentGen && (<>Loading...</>)}
                {currentGen && (<>
                    <div className="flex justify-center mb-4">
                        <img height={adopt.height} width={adopt.width} key={currentGen.url} src={currentGen.url} onLoad={loaded} />
                    </div>
                    <div className="flex gap-2 mb-4">
                        <button 
                            className={`grow bg-orange-400 text-white rounded-md text-sm py-2 ${isLoading && "opacity-50"}`}
                            onClick={randomize} 
                            disabled={isLoading}
                        >Randomize</button>
                        <button 
                            className={`grow bg-blue-500 text-white rounded-md text-sm py-2 ${isLoading && "opacity-50"}`}
                            onClick={preview}
                            disabled={isLoading}
                        >Preview</button>
                    </div>
                    <table className="w-full">
                        <tbody>
                        {genePoolTable}
                        </tbody>
                    </table>
                </>)}
            </div>
        </div>
    );
}

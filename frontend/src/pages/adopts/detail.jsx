import { useState, useEffect, useContext } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import AppContext from "context";
import AdoptBasicsPanel from "./components/AdoptBasicsPanel";
import AdoptLayersPanel from "./components/AdoptLayersPanel";
import ColorPoolsPanel from "./components/ColorPoolsPanel";
import GenePoolsPanel from "./components/GenePoolsPanel";

export default function AdoptDetailPage() {
    const {setBreadcrumbs} = useContext(AppContext);
    const [loaders, setLoaders] = useState({});
    const [adopt, setAdopt] = useState(null);
    const [colorPools, setColorPools] = useState(null);
    const [genePools, setGenePools] = useState(null);
    const [currentTab, setCurrentTab] = useState('adopt-basic-tab');
    let { id } = useParams();

    useEffect(() => {
        reloadAdopt();
        reloadColorPools(false);
        reloadGenePools(false);
    }, []);

    useEffect(() => {
        const breadcrumbs = [];
        if (adopt) {
            breadcrumbs.push({to: `/adopts/${adopt.id}`, title: adopt.name});
            breadcrumbs.push({to: `/adopts/${adopt.id}`, title: tabs.find((x) => x.id === currentTab)?.tabTitle})
        }
        setBreadcrumbs(breadcrumbs);
    }, [adopt, currentTab])

    function pushLoader(key) {
        setLoaders({...loaders, [key]: true});
    }

    function popLoader(key) {
        const {[key]: _, ...poppedLoaders} = loaders;
        setLoaders(poppedLoaders);
    }

    function reloadAdopt(adopt=null) {
        if (adopt) {
            setAdopt(adopt);
        } else {
            pushLoader('adopt');
            axios.get(`adopts/${id}`).then(data => {
                setAdopt(data.data);
                popLoader('adopt');
            });
        }
    }

    function reloadColorPools(doReload=true) {
        pushLoader('color_pools');
        axios.get(`adopts/${id}/color-pools`).then(data => {
            setColorPools(data.data)
            popLoader('color_pools');
        });
        if (doReload) {
            reloadAdopt();
        }
    }

    function reloadGenePools(doReload=true) {
        pushLoader('gene_pools');
        axios.get(`adopts/${id}/gene-pools`).then(data => {
            setGenePools(data.data)
            popLoader('gene_pools');
        });
        if (doReload) {
            reloadAdopt();
        }
    }

    const tabs = [
        {
            id: "adopt-basic-tab",
            target: "adopt-basic-content",
            tabTitle: "Basic",
            tabPill: null,
            component: (<AdoptBasicsPanel adopt={adopt} onSubmitted={reloadAdopt} />)
        },
        {
            id: "adopt-layers-tab",
            target: "adopt-layers-content",
            tabTitle: "Base layers",
            tabPill: adopt?.layers_count,
            component: (<AdoptLayersPanel adopt={adopt} genePools={genePools} onSubmitted={reloadAdopt} />)
        },
        {
            id: "color-pools-tab",
            target: "color-pools-content",
            tabTitle: "Color pools",
            tabPill: adopt?.colors_count,
            component: (<ColorPoolsPanel adopt={adopt} colorPools={colorPools} onSubmitted={reloadColorPools} />)
        },
        {
            id: "gene-pools-tab",
            target: "gene-pools-content",
            tabTitle: "Gene pools",
            tabPill: adopt?.genes_count,
            component: (<GenePoolsPanel adopt={adopt} genePools={genePools} colorPools={colorPools} onSubmitted={reloadGenePools} />)
        },
    ]

    return !adopt ? (<>Loading...</>) : (
        <div className="w-full bg-white border rounded-lg shadow-md dark:bg-gray-800 dark:border-gray-700">
            <ul className="flex flex-wrap items-stretch text-sm font-medium text-center text-gray-500 border-b border-gray-200 rounded-t-lg bg-gray-50 dark:border-gray-700 dark:text-gray-400 dark:bg-gray-800" id="defaultTab" data-tabs-toggle="#defaultTabContent" role="tablist">
                {tabs.map((tab, key) => (
                <li key={key} className="mr-2 flex items-stretch">
                    <button 
                        id={tab.id} 
                        data-tabs-target={`#${tab.target}`} 
                        type="button" 
                        role="tab" 
                        aria-controls="about" 
                        aria-selected={currentTab === tab.id} 
                        className={`inline-block p-4 ${currentTab === tab.id ? "text-blue-600" : ""} rounded-tl-lg hover:bg-gray-100`}
                        onClick={() => setCurrentTab(tab.id)}
                    >
                        {tab.tabTitle} 
                        {tab.tabPill !== null && (
                            <span className={`inline-flex justify-center items-center ml-2 w-4 p-3 h-4 text-xs font-semibold ${tab.tabPill ? "text-blue-800 bg-blue-200" : "text-red-800 bg-red-200"} rounded-full`}>
                                {tab.tabPill}
                            </span>
                        )}
                    </button>
                </li>))}
            </ul>
            <div id="defaultTabContent" className={Object.keys(loaders).length > 0 ? "hidden" : "block"}>
                {tabs.map((tab, key) => (
                <div 
                    key={key}
                    className={`${currentTab === tab.id ? "" : "hidden"} p-4 bg-white rounded-lg md:p-8`} 
                    id={tab.target} 
                    role="tabpanel" 
                    aria-labelledby={tab.id}
                >
                    {tab.component}
                </div>
                ))}
            </div>
        </div>
    );
}
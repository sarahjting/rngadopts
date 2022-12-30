import { useState, useEffect, useContext } from "react";
import AdoptLayersPanel from "pages/adopts/components/AdoptLayersPanel";
import ColorPoolsPanel from "pages/adopts/components/ColorPoolsPanel";
import GenePoolsPanel from "pages/adopts/components/GenePoolsPanel";
import AppContext from "context";

export default function AdoptDetailTabs({adopt, colorPools, genePools, onAdoptUpdated, onColorPoolsUpdated, onGenePoolsUpdated}) {
    const {setBreadcrumbs} = useContext(AppContext);
    const [currentTab, setCurrentTab] = useState('adopt-layers-tab');

    useEffect(() => {
        const breadcrumbs = [{to: `/adopts/${adopt.id}`, title: adopt.name}];
        breadcrumbs.push({to: `/adopts/${adopt.id}`, title: tabs.find((x) => x.id === currentTab)?.tabTitle})
        setBreadcrumbs(breadcrumbs);
    }, [currentTab])

    const tabs = [
        {
            id: "adopt-layers-tab",
            target: "adopt-layers-content",
            tabTitle: "Base layers",
            tabPill: adopt.layers_count,
            component: (<AdoptLayersPanel adopt={adopt} genePools={genePools} onSubmitted={onAdoptUpdated} />)
        },
        {
            id: "color-pools-tab",
            target: "color-pools-content",
            tabTitle: "Color pools",
            tabPill: adopt.colors_count,
            component: (<ColorPoolsPanel adopt={adopt} colorPools={colorPools} onSubmitted={onColorPoolsUpdated} />)
        },
        {
            id: "gene-pools-tab",
            target: "gene-pools-content",
            tabTitle: "Gene pools",
            tabPill: adopt.genes_count,
            component: (<GenePoolsPanel adopt={adopt} genePools={genePools} colorPools={colorPools} onSubmitted={onGenePoolsUpdated} />)
        },
    ]

    return (
        <div className="w-full bg-white border rounded-lg shadow-md dark:bg-gray-800 dark:border-gray-700">
            <ul className="flex flex-wrap text-sm font-medium text-center text-gray-500 border-b border-gray-200 rounded-t-lg bg-gray-50 dark:border-gray-700 dark:text-gray-400 dark:bg-gray-800" id="defaultTab" data-tabs-toggle="#defaultTabContent" role="tablist">
                {tabs.map((tab, key) => (
                <li key={key} className="mr-2">
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
                        <span className={`inline-flex justify-center items-center ml-2 w-4 p-3 h-4 text-xs font-semibold ${tab.tabPill ? "text-blue-800 bg-blue-200" : "text-red-800 bg-red-200"} rounded-full`}>
                            {tab.tabPill}
                        </span>
                    </button>
                </li>))}
            </ul>
            <div id="defaultTabContent">
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
import { useState, useEffect, useContext } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import AppContext from "context";
import AdoptDetailTabs from "pages/adopts/components/AdoptDetailTabs";
import FormTextInput from "components/form/FormTextInput";

export default function AdoptDetailPage() {
    const {pushToast, setBreadcrumbs} = useContext(AppContext);
    const [loaders, setLoaders] = useState({});
    const [adopt, setAdopt] = useState(null);
    const [colorPools, setColorPools] = useState(null);
    const [genePools, setGenePools] = useState(null);
    const [name, setName] = useState('');
    const [shortName, setShortName] = useState('');
    const [errors, setErrors] = useState({});
    let { id } = useParams();

    function loadAdopt(adopt) {
        setAdopt(adopt);
        setName(adopt.name);
        setShortName(adopt.short_name);
        setBreadcrumbs([{to: `/adopts/${adopt.id}`, title: adopt.name}]);
    }

    function pushLoader(key) {
        setLoaders({...loaders, [key]: true});
    }

    function popLoader(key) {
        const {[key]: _, ...poppedLoaders} = loaders;
        setLoaders(poppedLoaders);
    }

    function reloadAdopt() {
        pushLoader('adopt');
        axios.get(`adopts/${id}`).then(data => {
            loadAdopt(data.data);
            popLoader('adopt');
        });
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

    useEffect(() => {
        reloadAdopt();
        reloadColorPools(false);
        reloadGenePools(false);
    }, []);

    function submit() {
        axios.put(`adopts/${adopt.id}`, {name, short_name: shortName})
            .then(data => data.data)
            .then(adopt => {
                loadAdopt(adopt);
                pushToast('Adopt updated.', 'success');
            })
            .catch(err => {
                if (err.response.status === 400) {
                    setErrors(err.response.data);
                }
            });
    }

    return !adopt ? (<>Loading...</>) : (
        <>
            <div className={`block md:flex gap-4`}>
                <div className="max-w-md w-96">
                    <div className="w-full p-4 bg-white border border-gray-200 rounded-lg shadow-md sm:p-6 md:p-8 mb-4">
                        <h5 className="text-xl font-medium text-gray-900 dark:text-white mb-3">Basic details</h5>
                        <FormTextInput 
                            label="Adopt name" 
                            name="name" 
                            errors={errors}
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                        ></FormTextInput>
                        <FormTextInput 
                            label="Short name"
                            helperText="for Discord commands" 
                            name="short_name" 
                            errors={errors}
                            value={shortName}
                            onChange={(e) => setShortName(e.target.value)}
                        ></FormTextInput>
                        <button className="w-full text-white bg-blue-500 hover:bg-blue-600 font-medium rounded-lg text-sm px-5 py-2.5 text-center" onClick={submit}>
                            Update
                        </button>
                    </div>
                </div>
                <div className="grow">
                    <AdoptDetailTabs 
                        adopt={adopt} 
                        colorPools={colorPools}
                        genePools={genePools}
                        onAdoptUpdated={reloadAdopt}
                        onColorPoolsUpdated={reloadColorPools}
                        onGenePoolsUpdated={reloadGenePools}
                        loaders={loaders}
                    ></AdoptDetailTabs>
                </div>
            </div>
        </>
    );
}
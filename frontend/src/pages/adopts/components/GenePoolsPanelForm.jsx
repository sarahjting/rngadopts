import { useState, useContext, useEffect } from "react";
import axios from "axios";
import AppContext from "context";
import GeneralModal from "components/modals/GeneralModal";
import FormSelect from "components/form/FormSelect";
import FormTextInput from "components/form/FormTextInput";

export default function GenePoolsPanelForm({adopt, colorPools, show, onSubmitted, onClose, genePool = null}) {
    const {pushToast} = useContext(AppContext);
    const [errors, setErrors] = useState({});
    const [form, setForm] = useState({});

    function submitted() {
        setForm({
            name: "",
            type: "basic",
            color_pool_id: "",
        });
        onSubmitted();
    };

    useEffect(() => {
        setErrors({});
        setForm({
            name: genePool?.name ?? "",
            type: genePool?.type ?? "basic",
            color_pool_id: genePool?.color_pool?.id ?? "",
        });
    }, [genePool])
    
    function submit() {
        const fn = genePool?.id ? axios.put : axios.post;
        fn(`adopts/${adopt.id}/gene-pools${genePool ? "/" + genePool.id : ""}`, form)
            .then(() => {
                pushToast('Gene pools updated.', 'success');
                submitted();
            })
            .catch((err) => {
                if (err.response?.status === 400) {
                    setErrors(err.response.data);
                } else {
                    throw err;
                }
            });
    }

    function deleteGenePool()
    {
        axios.delete(`adopts/${adopt.id}/gene-pools/${genePool.id}`)
            .then(() => {
                pushToast('Gene pool deleted.', 'success');
                submitted();
            })
            .catch((err) => {
                if (err.response?.status === 400) {
                    setErrors(err.response.data);
                } else {
                    throw err;
                }
            });
    }


    return (
        <GeneralModal 
            show={show}
            title={genePool ? 'Update gene pool' : 'Create new gene pool'}
            onClose={onClose} 
            footer={(
                <div className="flex w-full gap-3">
                    {genePool && (<button className="text-white bg-red-500 hover:bg-red-600 font-medium rounded-lg text-sm px-5 py-2.5 text-center" onClick={deleteGenePool}>Delete</button>)}
                    <button className="grow text-white bg-blue-500 hover:bg-blue-600 font-medium rounded-lg text-sm px-5 py-2.5 text-center" onClick={submit}>{genePool ? 'Update' : 'Create'}</button>
                </div>
            )}
        >
            <div>
                <div>
                    {!genePool && (
                        <p className="mb-3">
                            A gene pool is a group of genes. FR's "Primary", "Secondary", "Tertiary" would be gene pools.
                            You'll fill this pool with genes in the next step.
                        </p>)}

                    <FormTextInput 
                        name="name"
                        errors={errors}
                        label="Name"
                        value={form.name}
                        onChange={(e) => setForm({...form, name: e.target.value})}
                    ></FormTextInput>

                    <FormSelect 
                        name="type"
                        errors={errors}
                        value={form.type}
                        label="Type"
                        options={{basic: "Basic", multi: "Multi"}}
                        onChange={(e) => setForm({...form, type: e.target.value})}
                    ></FormSelect>
                    <div className="text-xs text-gray-500 mb-3">
                        <p>Basic: One gene per pool is always selected.</p> 
                        <p>Multi: Every gene in the pool has an individual X/100 chance of being randomly added.</p>
                    </div>
                    
                    <FormSelect 
                        name="color_pool_id"
                        errors={errors}
                        label="Color pool"
                        value={form.color_pool_id}
                        options={colorPools.reduce((a, b) => ({
                            ...a,
                            [b.id]: b.name,
                        }), {})}
                        onChange={(e) => setForm({...form, color_pool_id: e.target.value})}
                    ></FormSelect>
                </div>
            </div>
        </GeneralModal>
    );
}
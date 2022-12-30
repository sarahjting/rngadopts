import { useState, useContext, useEffect } from "react";
import axios from "axios";
import AppContext from "context";
import GeneralModal from "components/modals/GeneralModal";
import FormSelect from "components/form/FormSelect";
import FormFile from "components/form/FormFile";
import FormTextInput from "components/form/FormTextInput";

export default function AdoptLayerFormModal({adopt, genePools, show, onSubmitted, onClose, adoptLayer = null}) {
    const {pushToast} = useContext(AppContext);
    const [errors, setErrors] = useState({});
    const [form, setForm] = useState({});

    function submitted() {
        setForm({
            image: null,
            type: "static",
            gene_pool_id: genePools.length ? genePools[0].id : "",
            sort: "0",
        });
        onSubmitted();
    };

    useEffect(() => {
        setErrors({});
        setForm({
            image: null,
            type: adoptLayer?.type ?? "static",
            gene_pool_id: adoptLayer?.gene_pool.id ?? (genePools && genePools.length ? genePools[0].id : ""),
            sort: adoptLayer?.sort ?? "0",
        });
    }, [adoptLayer])
    
    function create() {
        const formData = new FormData();
        formData.append('type', form.type)
        formData.append('sort', form.sort)

        if (form.type === "gene") {
            formData.append('gene_pool_id', form.gene_pool_id)
        } else {
            formData.append('image', form.image)
        }

        axios.post(`adopts/${adopt.id}/layers`, formData)
            .then(() => {
                pushToast('Adopt base layer created.', 'success');
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

    function update() {
        const data = {type: form.type, sort: form.sort};
        if (form.type === "gene") {
            data.gene_pool_id = form.gene_pool_id;
        }
        axios.put(`adopts/${adopt.id}/layers/${adoptLayer.id}`, data)
            .then(() => {
                pushToast('Adopt base layer updated.', 'success');
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

    function deleteLayer()
    {
        axios.delete(`adopts/${adopt.id}/layers/${adoptLayer.id}`)
            .then(() => {
                pushToast('Adopt base layer deleted.', 'success');
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
            title={adoptLayer ? 'Update adopt base layer' : 'Create new adopt base layer'}
            onClose={onClose} 
            footer={(
                <div className="flex w-full gap-3">
                    {adoptLayer && (<button className="text-white bg-red-500 hover:bg-red-600 font-medium rounded-lg text-sm px-5 py-2.5 text-center" onClick={deleteLayer}>Delete</button>)}
                    <button className="grow text-white bg-blue-500 hover:bg-blue-600 font-medium rounded-lg text-sm px-5 py-2.5 text-center" onClick={adoptLayer ? update : create}>{adoptLayer ? 'Update' : 'Create'}</button>
                </div>
            )}
        >
            <div>
                <div>
                    {adoptLayer && adoptLayer.image && (<div class="flex justify-center mb-2"><img src={adoptLayer.image}></img></div>)}
                    <FormSelect 
                        name="type"
                        errors={errors}
                        value={form.type}
                        label="Type"
                        options={{static: "Static image (eg. lines, eye whites)", shading: "Shading", highlights: "Highlights", gene: "Gene"}}
                        onChange={(e) => setForm({...form, type: e.target.value})}
                    ></FormSelect>
                    
                    {form.type === "gene" && genePools && <FormSelect 
                        name="gene_pool_id"
                        errors={errors}
                        label="Gene pool"
                        value={form.gene_pool_id}
                        options={genePools.reduce((a, b) => ({
                            ...a,
                            [b.id]: b.name,
                        }), {})}
                        onChange={(e) => setForm({...form, gene_pool_id: e.target.value})}
                    ></FormSelect>}
                    
                    {!adoptLayer && form.type !== "gene" && (<FormFile
                        name="image"
                        label="Layer image"
                        onChange={(e) => setForm({...form, image: e.target.files[0]})}
                        errors={errors}
                    />)}

                    <FormTextInput 
                        name="sort"
                        errors={errors}
                        label="Sort"
                        helperText="Higher numbers go on top"
                        value={form.sort}
                        onChange={(e) => setForm({...form, sort: e.target.value})}
                    ></FormTextInput>
                </div>
            </div>
        </GeneralModal>
    );
}
import { useState, useContext, useEffect } from "react";
import axios from "axios";
import AppContext from "context";
import GeneralModal from "components/modals/GeneralModal";
import FormSelect from "components/form/FormSelect";
import FormFile from "components/form/FormFile";

export default function AdoptLayersPanelForm({adopt, colorPools, show, onSubmitted, onClose, adoptLayer = null}) {
    const {pushToast} = useContext(AppContext);
    const [errors, setErrors] = useState({});
    const [form, setForm] = useState({});

    function submitted() {
        setForm({
            image: null,
            type: "static",
            color_pool_id: "",
        });
        onSubmitted();
    };

    useEffect(() => {
        setErrors({});
        setForm({
            image: null,
            type: adoptLayer?.type ?? "static",
            color_pool_id: adoptLayer?.color_pool_id ?? "",
        });
    }, [adoptLayer])
    
    function create() {
        const formData = new FormData();
        formData.append('image', form.image)
        formData.append('type', form.type)

        if (form.type === "color") {
            formData.append('color_pool_id', form.color_pool_id)
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
        const data = {type: form.type};
        if (form.type === "color") {
            data.color_pool_id = form.color_pool_id;
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
                    <FormSelect 
                        name="type"
                        errors={errors}
                        value={form.type}
                        label="Type"
                        options={{static: "Static image (eg. lines, eye whites)", shading: "Shading", highlights: "Highlights"}}
                        onChange={(e) => setForm({...form, type: e.target.value})}
                    ></FormSelect>
                    
                    {form.type === "color" && <FormSelect 
                        name="color_pool_id"
                        errors={errors}
                        label="Color pool"
                        value={form.color_pool_id}
                        options={colorPools.reduce((a, b) => ({
                            ...a,
                            [b.id]: b.name,
                        }), {})}
                        onChange={(e) => setForm({...form, color_pool_id: e.target.value})}
                    ></FormSelect>}
                    
                    {!adoptLayer && (<FormFile
                        name="image"
                        label="Layer image"
                        onChange={(e) => setForm({...form, image: e.target.files[0]})}
                        errors={errors}
                    />)}
                </div>
            </div>
        </GeneralModal>
    );
}
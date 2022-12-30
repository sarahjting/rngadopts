import { useState, useContext, useEffect } from "react";
import axios from "axios";
import AppContext from "context";
import GeneralModal from "components/modals/GeneralModal";
import FormSelect from "components/form/FormSelect";
import FormFile from "components/form/FormFile";
import FormTextInput from "components/form/FormTextInput";

export default function GeneLayerFormModal({adopt, genePool, gene, show, onSubmitted, onClose, geneLayer = null}) {
    const {pushToast} = useContext(AppContext);
    const [errors, setErrors] = useState({});
    const [form, setForm] = useState({});

    const colorPool = gene.color_pool ?? genePool.color_pool;

    useEffect(() => {
        setErrors({});
        setForm({
            image: null,
            type: geneLayer?.type ?? "color_on",
            color_key: geneLayer?.color_key ?? "1",
            sort: geneLayer?.sort ?? "0",
        });
    }, [geneLayer])

    function submitted() {
        setForm({
            image: null,
            type: "color_on",
            color_key: "1",
            sort: "0",
        });
        onSubmitted();
    };
    
    function create() {
        const formData = new FormData();
        formData.append('gene_id', gene.id)
        formData.append('image', form.image)
        formData.append('type', form.type)
        formData.append('color_key', form.color_key)
        formData.append('sort', form.sort)

        axios.post(`adopts/${adopt.id}/gene-layers`, formData)
            .then(() => {
                pushToast('Gene layer created.', 'success');
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
        axios.put(`adopts/${adopt.id}/gene-layers/${geneLayer.id}`, {
            type: form.type, 
            sort: form.sort,
            color_key: form.color_key,
        })
            .then(() => {
                pushToast('Gene layer updated.', 'success');
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
        axios.delete(`adopts/${adopt.id}/gene-layers/${geneLayer.id}`)
            .then(() => {
                pushToast('Gene layer deleted.', 'success');
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
            title={geneLayer ? 'Update gene layer' : 'Create new gene layer'}
            onClose={onClose} 
            footer={(
                <div className="flex w-full gap-3">
                    {geneLayer && (<button className="text-white bg-red-500 hover:bg-red-600 font-medium rounded-lg text-sm px-5 py-2.5 text-center" onClick={deleteLayer}>Delete</button>)}
                    <button className="grow text-white bg-blue-500 hover:bg-blue-600 font-medium rounded-lg text-sm px-5 py-2.5 text-center" onClick={geneLayer ? update : create}>{geneLayer ? 'Update' : 'Create'}</button>
                </div>
            )}
        >
            <div>
                <div>
                    {!geneLayer && (<FormFile
                        name="image"
                        label="Layer image"
                        onChange={(e) => setForm({...form, image: e.target.files[0]})}
                        errors={errors}
                    />)}

                    <FormSelect 
                        name="type"
                        errors={errors}
                        value={form.type}
                        label="Type"
                        options={{
                            static_over: "Static over",
                            shading_over: "Shading over",
                            highlights_over: "Highlights over",
                            color_over: "Color over",
                            static_on: "Static on",
                            color_on: "Color on",
                            static_under: "Static under",
                            shading_under: "Shading under",
                            highlights_under: "Highlights under",
                            color_under: "Color under",
                        }}
                        onChange={(e) => setForm({...form, type: e.target.value})}
                    ></FormSelect>
                    <div className="text-xs text-gray-600 mb-3">
                        <ul className="list-disc ml-4">
                            <li>
                                Single-color marking: 1 COLOR ON layer. 
                            </li>
                            <li>
                                Multi-color marking: 1 COLOR ON layer for each color. Select a different palette for each. 
                            </li>
                            <li>
                                Apparel: 1 STATIC OVER layer. If you want color pool colors, refer to Tert/eyes guide.
                            </li>
                            <li>
                                Backdrop: 1 STATIC UNDER layer. If you want color pool colors, refer to Tert/eyes guide.
                            </li>
                            <li>
                                Skins/tattoos (markings that do not get flood filled): 1 STATIC ON layer.
                            </li>
                            <li>
                                Tert/eyes: Lines as STATIC OVER, shading as SHADING OVER, highlights as HIGHLIGHTS OVER, all color layers as COLOR OVER, eye white layer as a STATIC OVER.
                                <ul className="list-disc ml-4">
                                    <li>If your tert goes behind the adopt, use STATIC UNDER, SHADING UNDER, HIGHLIGHTS UNDER, COLOR UNDER</li>
                                    <li>You can use over and under layers for double-sided terts (eg. front and back wings)</li>
                                    <li>You can use over, under, and COLOR ON for terts that come with markings</li>
                                </ul>
                            </li>
                        </ul>
                    </div>

                    {
                        (form.type === 'color_over' || form.type === 'color_on' || form.type === 'color_under') && (
                            <>
                                <FormTextInput 
                                    name="color_key"
                                    errors={errors}
                                    label="Palette number"
                                    value={form.color_key}
                                    onChange={(e) => setForm({...form, color_key: e.target.value})}
                                ></FormTextInput>
                                <div className="text-xs text-gray-600 mb-3">
                                    <p>The color pool for this gene is <strong>{colorPool.name}</strong>.</p>
                                    {
                                        colorPool.palettes_count === 1 
                                            ? (<p> This color pool only has 1 palette, so leave this as 1.</p>)
                                            : (<p> This color pool has {colorPool.palettes_count} palettes. Pick a number between 1-{colorPool.palettes_count}; this palette will be used to color this layer.</p>)
                                    }
                                </div>
                            </>
                        )
                    }

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
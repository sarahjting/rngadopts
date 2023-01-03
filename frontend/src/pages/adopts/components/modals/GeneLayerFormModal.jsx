import { useState, useContext, useEffect } from "react";
import axios from "axios";
import AppContext from "context";
import GeneralModal from "components/modals/GeneralModal";
import FormSelect from "components/form/FormSelect";
import FormFile from "components/form/FormFile";
import FormTextInput from "components/form/FormTextInput";
import DeleteButton from "components/button/DeleteButton";
import SubmitButton from "components/button/SubmitButton";

export default function GeneLayerFormModal({adopt, genePools, genePool, gene, show, onSubmitted, onClose, geneLayer = null}) {
    const {pushToast} = useContext(AppContext);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [errors, setErrors] = useState({});
    const [form, setForm] = useState({});

    const requiredGene = form?.required_gene_id ? genePools.map(x => x.genes).flat(1).find(x => `${x.id}` === `${form.required_gene_id}`) : null;
    const requiredGenePool = requiredGene ? 
        genePools.find(x => !!x.genes.find(x => `${x.id}` === `${requiredGene.id}`)) : 
        (form?.required_gene_pool_id ? genePools.find(x => `${x.id}` === `${form.required_gene_pool_id}`) : null);
    const colorPool = requiredGene?.color_pool ?? requiredGenePool?.color_pool ?? gene.color_pool ?? genePool.color_pool;

    useEffect(() => {
        setErrors({});
        setForm({
            image: null,
            type: geneLayer?.type ?? "color_on",
            color_key: geneLayer?.color_key ?? "1",
            sort: geneLayer?.sort ?? "0",
            required_gene_id: geneLayer?.required_gene_id ?? "",
            required_gene_pool_id: geneLayer?.required_gene_pool_id ?? "",
        });
    }, [geneLayer])

    function submitted() {
        setForm({
            image: null,
            type: "color_on",
            color_key: "1",
            sort: "0",
            required_gene_id: "",
            required_gene_pool_id: "",
        });
        onSubmitted();
    };
    
    function create() {
        if (isSubmitting) {
            return;
        }

        setIsSubmitting(true);

        const formData = new FormData();
        formData.append('gene_id', gene.id);
        formData.append('image', form.image);
        formData.append('type', form.type);
        formData.append('color_key', form.color_key);
        formData.append('sort', form.sort);
        formData.append('required_gene_id', form.required_gene_id);
        formData.append('required_gene_pool_id', form.required_gene_pool_id);

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
            }).finally(() => setIsSubmitting(false));
    }

    function update() {
        if (isSubmitting) {
            return;
        }
        setIsSubmitting(true);
        axios.put(`adopts/${adopt.id}/gene-layers/${geneLayer.id}`, {
            type: form.type, 
            sort: form.sort,
            color_key: form.color_key,
            required_gene_id: form.required_gene_id,
            required_gene_pool_id: form.required_gene_pool_id,
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
            }).finally(() => setIsSubmitting(false));
    }

    function deleteLayer()
    {
        if (isSubmitting) {
            return;
        }
        setIsSubmitting(true);
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
            }).finally(() => setIsSubmitting(false));
    }

    return (
        <GeneralModal 
            show={show}
            title={geneLayer ? 'Update gene layer' : 'Create new gene layer'}
            onClose={onClose} 
            footer={(
                <div className="flex w-full gap-3">
                    {geneLayer && (<DeleteButton disabled={isSubmitting} onClick={deleteLayer}>Delete</DeleteButton>)}
                    <SubmitButton disabled={isSubmitting} onClick={geneLayer ? update : create}>{geneLayer ? 'Update' : 'Create'}</SubmitButton>
                </div>
            )}
        >
            <div>
                <div>
                    {geneLayer && geneLayer.image && (<div className="flex justify-center mb-2"><img src={geneLayer.image}></img></div>)}

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
                                Tert/eyes: Lines as STATIC OVER, shading as SHADING OVER, highlights as HIGHLIGHTS OVER, all color layers as COLOR OVER, eye white layer as a STATIC OVER.
                            </li>
                        </ul>
                    </div>

                    <div class="flex gap-3">
                        <div class="grow">
                            <FormSelect 
                                name="required_gene_pool_id"
                                errors={errors}
                                label="Required gene pool"
                                value={form.required_gene_pool_id}
                                options={genePools.reduce((a, b) => (b.type === "basic" ? {
                                    ...a,
                                    [b.id]: b.name,
                                } : a), {"": ""})}
                                onChange={(e) => setForm({...form, required_gene_pool_id: e.target.value, required_gene_id: ""})}
                            ></FormSelect>
                            <div className="text-xs text-gray-600 mb-3">
                                <p>Advanced: Ignore if you don't know what this is.</p>
                            </div>
                        </div>
                        <div class="grow">
                            <FormSelect 
                                name="required_gene_id"
                                errors={errors}
                                label="Required gene"
                                value={form.required_gene_id}
                                options={genePools.reduce((a, b) => ({
                                    ...a,
                                    [b.name]: b.genes.reduce((aa, bb) => ({
                                        ...aa,
                                        [bb.id]: bb.name,
                                    }), {}),
                                }), {"": ""})}
                                onChange={(e) => setForm({...form, required_gene_id: e.target.value, required_gene_pool_id: ""})}
                            ></FormSelect>
                            <div className="text-xs text-gray-600 mb-3">
                                <p>Advanced: Ignore if you don't know what this is.</p>
                            </div>
                        </div>
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
                                    {requiredGenePool && (<p>
                                        <span class="text-orange-500">You have selected a required gene. The color of this layer will be taken from <strong>{requiredGene && requiredGene.name} ({requiredGenePool.name})</strong>.</span> 
                                    </p>)}
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
import { useState, useContext, useEffect } from "react";
import axios from "axios";
import AppContext from "context";
import GeneralModal from "components/modals/GeneralModal";
import FormSelect from "components/form/FormSelect";
import FormTextInput from "components/form/FormTextInput";
import DeleteButton from "components/button/DeleteButton";
import SubmitButton from "components/button/SubmitButton";
import slugify from "../../../../utils/slugify";

export default function GeneFormModal({adopt, colorPools, genePool, show, onSubmitted, onClose, gene = null}) {
    const {pushToast} = useContext(AppContext);
    const [errors, setErrors] = useState({});
    const [form, setForm] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);

    function submitted() {
        setForm({
            name: "",
            slug: "",
            weight: "1",
            color_pool_id: "",
        });
        onSubmitted();
    };

    useEffect(() => {
        setErrors({});
        setForm({
            name: gene?.name ?? "",
            slug: gene?.slug ?? "",
            weight: gene?.weight ?? "1",
            color_pool_id: gene?.color_pool?.id ?? "",
        });
    }, [gene])
    
    function submit() {
        if (isSubmitting) {
            return;
        }

        setIsSubmitting(true);

        const fn = gene ? axios.put : axios.post;
        fn(`adopts/${adopt.id}/gene-pools/${genePool.id}/genes${gene ? "/" + gene.id : ""}`, form)
            .then(() => {
                pushToast('Genes updated.', 'success');
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

    function deleteGene()
    {
        if (isSubmitting) {
            return;
        }

        setIsSubmitting(true);
        
        axios.delete(`adopts/${adopt.id}/gene-pools/${genePool.id}/genes/${gene.id}`)
            .then(() => {
                pushToast('Gene deleted.', 'success');
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
            title={gene ? `Update gene: ${gene.name}` : 'Create new gene'}
            onClose={onClose} 
            footer={(
                <div className="flex w-full gap-3">
                    {gene && (<DeleteButton disabled={isSubmitting} onClick={deleteGene}>Delete</DeleteButton>)}
                    <SubmitButton disabled={isSubmitting} onClick={submit}>{gene ? 'Update' : 'Create'}</SubmitButton>
                </div>
            )}
        >
            <div>
                <div>
                    <FormTextInput 
                        name="name"
                        errors={errors}
                        label="Name"
                        value={form.name}
                        onChange={(e) => setForm({
                            ...form, 
                            name: e.target.value, 
                            slug: form.slug === slugify(form.name) ? slugify(e.target.value) : form.slug,
                        })}
                    ></FormTextInput>

                    <FormTextInput 
                        name="slug"
                        errors={errors}
                        label="Slug"
                        helperText="how the gene shows in the image URL"
                        value={form.slug}
                        onChange={(e) => setForm({...form, slug: e.target.value})}
                    ></FormTextInput>

                    <FormTextInput 
                        name="weight"
                        errors={errors}
                        label="Weight"
                        value={form.weight}
                        onChange={(e) => setForm({...form, weight: e.target.value})}
                    ></FormTextInput>
                    <div className="text-xs text-gray-500 mb-3">
                        {
                            genePool.type === "multi" && (<p>
                                <strong>This gene pool is a MULTI type.</strong>
                                Every gene is randomised independently based on weight. 
                                Gene A with a weight of 100 has a 100/100 chance of being added. 
                                Gene B with a weight of 50 has a 50/100 chance of being added.
                            </p>)
                        }
                        {
                            genePool.type === "basic" && (<>
                                <p className="mb-1">
                                    If A has a weight of 1 and B has a weight of 1, A will be picked 50% of the time. <br/>
                                    If A has a weight of 3 and B has a weight of 1, A will be picked 75% of the time.<br/>
                                    If A has a weight of 1000 and B has a weight of 1, A will be picked 1000/1001 times. 
                                </p>
                                <p className="mb-1">
                                    If you want all genes to have the same rarity, set all of them to 1. 
                                </p>
                                <p className="mb-1">
                                    If you want a gene to be more common, raise its weight. 
                                </p>
                                <p className="mb-1">
                                    If you want a gene to be more rare, raise the weight of everything except for that gene.
                                </p>
                            </>)
                        }
                    </div>
                    
                    <FormSelect 
                        name="color_pool_id"
                        errors={errors}
                        label="Color pool override"
                        value={form.color_pool_id}
                        options={colorPools.reduce((a, b) => ({
                            ...a,
                            [b.id]: b.name,
                        }), {"": "Do not override"})}
                        onChange={(e) => setForm({...form, color_pool_id: e.target.value})}
                    ></FormSelect>
                    <div className="text-xs text-gray-500 mb-3">
                        <p className="mb-1">
                            This gene pool's color pool is currently set to <strong>{genePool.color_pool.name}</strong>.
                        </p>
                        <p className="mb-1">
                            Set this here if you want to override it for this one gene. Otherwise you can leave this empty.
                        </p>
                    </div>
                </div>
            </div>
        </GeneralModal>
    );
}
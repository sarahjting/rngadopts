import { useState, useContext, useEffect } from "react";
import axios from "axios";
import AppContext from "context";
import GeneralModal from "components/modals/GeneralModal";
import FormSelect from "components/form/FormSelect";
import FormTextInput from "components/form/FormTextInput";
import DeleteButton from "components/button/DeleteButton";
import SubmitButton from "components/button/SubmitButton";
import slugify from "../../../../utils/slugify";

export default function GenePoolFormModal({adopt, colorPools, show, onSubmitted, onClose, genePool = null}) {
    const {pushToast} = useContext(AppContext);
    const [errors, setErrors] = useState({});
    const [form, setForm] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);

    function submitted() {
        setForm({
            name: "",
            slug: "",
            type: "basic",
            color_pool_id: "",
        });
        onSubmitted();
    };

    useEffect(() => {
        setErrors({});
        setForm({
            name: genePool?.name ?? "",
            slug: genePool?.slug ?? "",
            type: genePool?.type ?? "basic",
            color_pool_id: genePool?.color_pool?.id ?? colorPools[0].id,
        });
    }, [genePool])
    
    function submit() {
        if (isSubmitting) {
            return;
        }

        setIsSubmitting(true);

        const fn = genePool?.id ? axios.put : axios.post;
        fn(`adopts/${adopt.id}/gene-pools${genePool ? `/${genePool.id}` : ""}`, form)
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
            }).finally(() => setIsSubmitting(false));
    }

    function deleteGenePool()
    {
        if (isSubmitting) {
            return;
        }

        setIsSubmitting(true);

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
            }).finally(() => setIsSubmitting(false));
    }


    return (
        <GeneralModal 
            show={show}
            title={genePool ? 'Update gene pool' : 'Create new gene pool'}
            onClose={onClose} 
            footer={(
                <div className="flex w-full gap-3">
                    {genePool && (<DeleteButton disabled={isSubmitting} onClick={deleteGenePool}>Delete</DeleteButton>)}
                    <SubmitButton disabled={isSubmitting} onClick={submit}>{genePool ? 'Update' : 'Create'}</SubmitButton>
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
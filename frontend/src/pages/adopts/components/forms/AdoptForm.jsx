import { useState, useEffect, useContext } from "react";
import axios from "axios";
import AppContext from "context";
import FormTextInput from "components/form/FormTextInput";
import FormTextarea from "components/form/FormTextarea";

export default function AdoptForm({adopt, onSubmitted = (() => {})}) {
    const {pushToast} = useContext(AppContext);
    const [form, setForm] = useState({});
    const [errors, setErrors] = useState({});

    useEffect(() => {
        setForm({
            "name": adopt?.name ?? "",
            "short_name": adopt?.short_name ?? "",
            "width": adopt?.width ?? "0",
            "height": adopt?.height ?? "0",
            "current_display_id": adopt?.current_display_id ?? "1",
            "gen_caption": adopt?.gen_caption ?? "Thank you for your purchase! Here is your drop off: \n\n[img]"
        });
    }, [adopt]);

    function submit() {
        const fn = adopt ? axios.put : axios.post;
        const endpoint = adopt ? `adopts/${adopt.id}` : "adopts/";
        fn(endpoint, form)
            .then(data => data.data)
            .then(adopt => {
                pushToast('Adopts updated.', 'success');
                onSubmitted(adopt);
            })
            .catch(err => {
                if (err.response.status === 400) {
                    setErrors(err.response.data);
                }
            });
    }

    return (
        <div className="w-full bg-white mb-4">
            <FormTextInput 
                label="Adopt name" 
                name="name" 
                errors={errors}
                value={form.name}
                onChange={(e) => setForm({...form, name: e.target.value})}
            ></FormTextInput>
            <FormTextInput 
                label="Short name"
                helperText="for Discord" 
                name="short_name" 
                errors={errors}
                value={form.short_name}
                onChange={(e) => setForm({...form, short_name: e.target.value})}
            ></FormTextInput>
            <FormTextInput 
                label="Width (px)"
                name="width" 
                errors={errors}
                value={form.width}
                onChange={(e) => setForm({...form, width: e.target.value})}
            ></FormTextInput>
            <FormTextInput 
                label="Height (px)"
                name="height" 
                errors={errors}
                value={form.height}
                onChange={(e) => setForm({...form, height: e.target.value})}
            ></FormTextInput>
            <FormTextarea 
                label="Caption on generate"
                name="gen_caption" 
                errors={errors}
                value={form.gen_caption}
                onChange={(e) => setForm({...form, gen_caption: e.target.value})}
            ></FormTextarea>
            {
                adopt && (<FormTextInput 
                    label="Current ID"
                    name="current_display_id" 
                    errors={errors}
                    value={form.current_display_id}
                    onChange={(e) => setForm({...form, current_display_id: e.target.value})}
                ></FormTextInput>)
            }
            <button className="w-full text-white bg-blue-500 hover:bg-blue-600 font-medium rounded-lg text-sm px-5 py-2.5 text-center" onClick={submit}>
                {adopt ? "Update" : "Create"}
            </button>
        </div>
    );
}
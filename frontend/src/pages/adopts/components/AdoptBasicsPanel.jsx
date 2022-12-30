import { useState, useEffect, useContext } from "react";
import axios from "axios";
import AppContext from "context";
import FormTextInput from "components/form/FormTextInput";

export default function AdoptBasicsPanel({adopt, onSubmitted = (() => {})}) {
    const {pushToast, setBreadcrumbs} = useContext(AppContext);
    const [form, setForm] = useState({});
    const [errors, setErrors] = useState({});

    useEffect(() => {
        setForm({
            "name": adopt.name,
            "short_name": adopt.short_name,
        })
        setBreadcrumbs([
            {to: `/adopts/${adopt.id}`, title: adopt.name},
            {to: `/adopts/${adopt.id}`, title: "Basics"},
        ]);
    }, [adopt]);

    function submit() {
        axios.put(`adopts/${adopt.id}`, form)
            .then(data => data.data)
            .then(adopt => {
                pushToast('Adopt updated.', 'success');
                onSubmitted(adopt);
            })
            .catch(err => {
                if (err.response.status === 400) {
                    setErrors(err.response.data);
                }
            });
    }

    return (
        <>
            <div className="max-w-md w-96 m-auto">
                <div className="w-full p-4 bg-white sm:p-6 md:p-8 mb-4">
                    <h5 className="text-xl font-medium text-gray-900 dark:text-white mb-3">Basic details</h5>
                    <FormTextInput 
                        label="Adopt name" 
                        name="name" 
                        errors={errors}
                        value={form.name}
                        onChange={(e) => setForm({...form, name: e.target.value})}
                    ></FormTextInput>
                    <FormTextInput 
                        label="Short name"
                        helperText="for Discord commands" 
                        name="short_name" 
                        errors={errors}
                        value={form.short_name}
                        onChange={(e) => setForm({...form, short_name: e.target.value})}
                    ></FormTextInput>
                    <button className="w-full text-white bg-blue-500 hover:bg-blue-600 font-medium rounded-lg text-sm px-5 py-2.5 text-center" onClick={submit}>
                        Update
                    </button>
                </div>
            </div>
        </>
    );
}
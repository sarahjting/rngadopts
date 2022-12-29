import { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import FormTextInput from "components/form/FormTextInput";
import AppContext from "context";

export default function AdoptCreatePage() {
    const {pushToast} = useContext(AppContext);
    const navigate = useNavigate();
    const [name, setName] = useState('');
    const [shortName, setShortName] = useState('');
    const [errors, setErrors] = useState({});
    
    useEffect(() => {
        if (!window.APP_FLAGS.adopts_creation) {
            navigate('dashboard')
        }
    }, [])

    function submit() {
        axios.post("adopts/", {name, short_name: shortName})
            .then(data => data.data)
            .then(adopt => {
                pushToast('Adopt created.', 'success');
                navigate(`/adopts/${adopt.id}`)
            })
            .catch(err => {
                if (err.response?.status === 400) {
                    setErrors(err.response.data);
                } else {
                    throw err;
                }
            });
    }

    return (
        <div className="max-w-md m-auto">
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
                Create
            </button>
        </div>
    );
}
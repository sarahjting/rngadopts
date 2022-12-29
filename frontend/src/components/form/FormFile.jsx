import FormInput from "components/form/FormInput";

export default function FormTextInput({label = null, helperText = null, errors = {}, ...props}) {
    return (<FormInput name={props.name} errors={errors} label={label} helperText={helperText}>
        <input 
            className={`block w-full text-sm text-gray-900 bg-gray-50 rounded-lg border cursor-pointer focus:outline-none mb-2 border-gray-300`} 
            type="file"
            {...props}
        />
    </FormInput>);
}
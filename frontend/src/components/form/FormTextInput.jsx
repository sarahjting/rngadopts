import FormInput from "components/form/FormInput";

export default function FormTextInput({label = null, helperText = null, errors = {}, value = "", ...props}) {
    const hasErrors = errors[props.name] && props.errors[props.name].length;

    return (<FormInput name={props.name} errors={errors} label={label} helperText={helperText}>
        <input 
            type="text" 
            value={value}
            className={`bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5 ${hasErrors ? "ring-3 ring-red-500 border-red-500" : "focus:ring-blue-500 focus:border-blue-500"}`} 
            {...props} 
        />
    </FormInput>);
}
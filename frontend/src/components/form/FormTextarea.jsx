import FormInput from "components/form/FormInput";

export default function FormTextarea({label = null, helperText = null, errors = {}, ...props}) {
    const hasErrors = props.errors && props.errors[props.name] && props.errors[props.name].length;

    return (<FormInput name={props.name} errors={errors} label={label} helperText={helperText}>
        <textarea className={`block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 ${hasErrors ? "ring-3 ring-red-500 border-red-500" : "focus:ring-blue-500 focus:border-blue-500"}`} {...props} />
    </FormInput>);
}
import FormInput from "components/form/FormInput";

export default function FormSelect({options, value = "", label = null, helperText = null, errors = {}, ...props}) {
    const hasErrors = props.errors && props.errors[props.name] && props.errors[props.name].length;
    
    return (<FormInput name={props.name} errors={errors} label={label} helperText={helperText}>
        <select 
            className={`bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 w-full pr-8 mb-2 ${hasErrors ? "border-red-500" : "border-gray-300"}`} 
            defaultValue={value}
            {...props}
        >
            {Object.keys(options).map((key) => (<option key={key} value={key}>{options[key]}</option>))}
        </select>
    </FormInput>);
}
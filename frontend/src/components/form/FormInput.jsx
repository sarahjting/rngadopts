export default function FormInput({children, name, errors = {}, label = null, helperText = null}) {
    const hasErrors = errors[name] && errors[name].length;

    return (<div className={`w-full mb-2 ${hasErrors ? "text-red-500" : "text-gray-900"}`}>
        {label && (<label className="label block mb-1 text-sm font-medium">{label} {helperText && (<span className="text-sm text-gray-400 font-light">{helperText}</span>)}</label>)}
        {children}
        {errors[name] && errors[name].map((err, key) => (<div key={key} className="text-sm">{err}</div>))}
    </div>);
}
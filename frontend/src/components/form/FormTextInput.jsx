export default function FormTextInput(props) {
    const hasErrors = props.errors && props.errors[props.name] && props.errors[props.name].length;

    return (<div className={`form-control w-full mb-5 ${hasErrors ? "text-red-500" : "text-gray-900"}`}>
        {props.label && (<label className="label">
            <label className="block mb-2 text-sm font-medium ">{props.label}</label>
            {props.labelHelper && (<span className="label-text-alt">{props.labelHelper}</span>)}
        </label>)}
        <input type="text" className={`bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5 ${hasErrors ? "ring-3 ring-red-500 border-red-500" : "focus:ring-blue-500 focus:border-blue-500"}`} {...props} />
        {props.errors && props.errors[props.name] && props.errors[props.name].map((err, key) => (<div key={key}>{err}</div>))}
    </div>);
}
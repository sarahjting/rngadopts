import { useEffect } from "react";

export default function FormTextInput(props) {
    const hasError = props.errors && props.errors[props.name] && props.errors[props.name].length > 0

    return (
        <div className="form-control w-full mb-2">
            {props.label && (<label className="label">
                <span className="label-text label-danger">{props.label}</span>
                {props.labelHelper && (<span className="label-text-alt">{props.labelHelper}</span>)}
            </label>)}
            <input type="text" className={`input input-bordered w-full ${hasError ? "input-error" : ""}`} {...props} />
            {props.errors && props.errors[props.name] && props.errors[props.name].map((err, key) => (<div className="text-error mt-1" key={key}>{err}</div>))}
        </div>
    );
}
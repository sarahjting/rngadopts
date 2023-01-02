export default function SubmitButton({disabled = false, children = "Submit", ...props}) {
    return (<button 
        disabled={disabled}
        className={`grow text-white bg-blue-500 hover:bg-blue-600 font-medium rounded-lg text-sm px-5 py-2.5 text-center ${disabled && "opacity-50"}`} 
        {...props}
    >{children}</button>);
}
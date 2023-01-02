export default function DeleteButton({disabled = false, ...props}) {
    return (<button 
        disabled={disabled}
        className={`text-white bg-red-500 hover:bg-red-600 font-medium rounded-lg text-sm px-5 py-2.5 text-center ${disabled && "opacity-50"}`} 
        {...props}
    >Delete</button>);
}
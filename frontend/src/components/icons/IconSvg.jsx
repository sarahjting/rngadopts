export default function IconSvg({className = "", size = "4", children, ...props}) {
    return (
        <svg className={`w-${size} h-${size} ${className}`} fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" {...props}>{children}</svg>
    );
}
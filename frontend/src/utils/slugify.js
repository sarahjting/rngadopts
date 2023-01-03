export default function slugify(str) {
    return str.toLowerCase().replace(/[^0-9a-z]/gi, "");
}
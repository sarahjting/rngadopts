/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "index.html",
    "templates/*.html",
    "./src/**/*.{html,js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require("daisyui"),
  ],
}

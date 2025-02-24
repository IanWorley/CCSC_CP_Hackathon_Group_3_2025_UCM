/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx,js,jsx}"],
  theme: {
    extend: {
      colors: {
        ucm: {
          red: "#d21e32",
        },
      },
    },
  },
  plugins: [],
};

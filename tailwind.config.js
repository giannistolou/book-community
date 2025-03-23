/** @type {import('tailwindcss').Config} */
import daisyui from "daisyui"
export default {
  content: ["./findBookCafe/**/*.{html,js}", "./landingPage/**/*.{html,js}"],
  daisyui: {
    themes: ["retro"],
  },
  plugins: [daisyui],
}
  
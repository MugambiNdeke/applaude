/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'luxury-black': '#0A0A0A', // Primary Background
        'electric-gold': '#FFD700', // Primary Action/Accent 
        'deep-gold': '#B8860B', // Subtle Hover/Shadow Tone
        'soft-white': '#E0E0E0', // Text/UI Elements
      },
      fontFamily: {
        poppins: ['Poppins', 'sans-serif'], // Exclusive Typography
      },
      boxShadow: {
        'gold-glow': '0 0 10px 1px rgba(255, 215, 0, 0.6)', // Subtle glow effect
      }
    },
  },
  plugins: [],
}

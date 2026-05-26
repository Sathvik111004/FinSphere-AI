/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        background: "#0B0F19",
        card: "rgba(17, 24, 39, 0.7)",
        primary: {
          DEFAULT: "#6366F1",
          hover: "#4F46E5"
        },
        accent: {
          emerald: "#10B981",
          crimson: "#EF4444",
          amber: "#F59E0B"
        }
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}

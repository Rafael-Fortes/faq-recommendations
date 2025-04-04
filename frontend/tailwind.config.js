/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#6400E4',
          dark: '#5000B4',
          light: '#8A3EF6',
        },
        accent: '#FFD300',
        background: '#FFF8F2',
        text: '#10162F',
        'light-gray': '#F6F6F6',
        green: {
          relevance: '#3CB371',
        },
        blue: {
          relevance: '#3B82F6',
        }
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', 'sans-serif'],
      },
    },
  },
  plugins: [],
}; 
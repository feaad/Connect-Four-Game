import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      // backgroundImage: {
      //   'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
      //   'gradient-conic':
      //     'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      // },
      fontFamily: {
        'sans': ['Helvetica Neue', 'Arial', 'sans', 'Helvetica'],
        'akshar': ['Akshar', 'sans-serif'],
      },
      colors: {
        bgc: "#E0F0F3",
        "btn-colour": "#224146",
        "btn-colour-hover": "#1E8190",
        "grid-colour": "#C2D2D4",
        "player1": "#B91372",
        "player2": "#FF7F11",
        "bg-1": "#0E3A49",
        "bg-2": "#228EAE",
        "bg-3": "#1FCFCF",
        "grid-bg": "#2D565B",
      }
    },
  },
  plugins: [require("tailwindcss-animate"), require("daisyui")],
  daisyui: {
    themes: ["light", "dark"],
  },
}

export default config;

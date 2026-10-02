import type { Config } from "tailwindcss";
const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        eco: {
          50: "#f0f9f2",
          100: "#dcf0e1",
          500: "#3fa66a",
          600: "#2f8654",
          900: "#173c26",
        },
        ink: "#1c1f1e",
      },
      borderRadius: { xl2: "20px" },
    },
  },
  plugins: [],
};
export default config;

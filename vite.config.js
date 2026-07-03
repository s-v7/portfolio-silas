/* eslint-env node */
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const isProduction = process.env.NODE_ENV?.includes("prod") ?? false;

export default defineConfig({
  plugins: [react()],
  base: isProduction ? "/portfolio-silas/" : "/",
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:3333",
        changeOrigin: true,
      },
    },
  },
});

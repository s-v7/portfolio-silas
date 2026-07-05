/* eslint-env node */
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";

const isProduction = process.env.NODE_ENV?.includes("prod") ?? false;

export default defineConfig({
  plugins: [react()],
  base: isProduction ? "/portfolio-silas/" : "/",
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:3333",
        changeOrigin: true,
      },
    },
  },
});

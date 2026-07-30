import React from "react";
import ReactDOM from "react-dom/client";
import App from "./app/App";

import "./styles/base/global.css";
import "./styles/base/design-system.css";
import "./styles/base/layout.css";
import "./index.css";

if ("scrollRestoration" in history) {
  globalThis.history.scrollRestoration = "manual";
}

globalThis.addEventListener("load", () => {
  globalThis.scrollTo(0, 0);
});

const rootElement = document.getElementById("root");

if (!rootElement) {
  throw new Error("Root element #root not found");
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

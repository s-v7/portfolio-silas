import React from "react";
import ReactDOM from "react-dom/client";
import App from "./app/App";

import "./styles/base/global.css";
import "./styles/base/design-system.css";
import "./styles/base/layout.css";
import "./index.css";

// Disable browser scroll restoration (SPA behav...)
if ("scrollRestoration" in history) {
  window.history.scrollRestoration = "manual";
}

window.addEventListener("load", () => {
  window.scrollTo(0, 0);
});

const rootElement = document.getElementById("root");

if (!rootElement) {
  throw new Error("Root element #root not found");
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);

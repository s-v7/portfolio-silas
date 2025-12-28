import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

// Disable browser scroll restoration (SPA behav...)
if ("scrollRestoration" in history) {
	// history.scrollRestoration = "manual";
	window.history.scrollRestoration = "manual";
}

window.addEventListener("load", () => {
	window.scrollTo(0,0);
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

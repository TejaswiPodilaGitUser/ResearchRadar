import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App";

import "./index.css";
import "./styles/layout.css";
import "./styles/navigation.css";
import "./styles/components.css";
import "./styles/pages.css";

import "./styles/home-page.css";
import "./styles/search-page.css";
import "./styles/paper-page.css";
import "./styles/paper-detail.css";
import "./styles/author-page.css";
import "./styles/topic-page.css";

import "./styles/metrics.css";
import "./styles/api-metrics.css";

import "./styles/error-state.css";
import "./styles/pagination.css";


const rootElement =
  document.getElementById("root");


if (!rootElement) {
  throw new Error(
    'Root element "#root" was not found.',
  );
}


ReactDOM.createRoot(
  rootElement,
).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
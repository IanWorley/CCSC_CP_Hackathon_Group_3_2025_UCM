import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import "./index.css";
import Index from "./routes/Index.tsx";
import Layout from "./routes/Layout.tsx";
import Login from "./routes/Login.tsx";
import MachinePage from "./routes/MachinePage.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Index />} />
          <Route path="/machine/:id" element={<MachinePage />} />
          <Route path="/login" element={<Login />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>
);

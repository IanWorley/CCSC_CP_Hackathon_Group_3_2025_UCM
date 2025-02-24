import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { BrowserRouter, Navigate, Route, Routes } from "react-router";
import Layout from './components/Layout.tsx';
import Login from './components/Login.tsx';
import Machines from './components/Machines.tsx';
import MachinePage from './components/MachinePage.tsx';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="/login" element={<Login />} />
          <Route path='/machines' element={<Machines />} />
          <Route path="/machine/:id" element={<MachinePage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)

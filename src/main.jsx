import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import RoleSelector from './RoleSelector';
import LoginForm from './LoginForm';
import SignupForm from './SignupForm';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<RoleSelector />} />
        <Route path="/user/login" element={<LoginForm role="user" />} />
        <Route path="/admin/login" element={<LoginForm role="admin" />} />
        <Route path="/user/signup" element={<SignupForm role="user" />} />
        <Route path="/admin/signup" element={<SignupForm role="admin" />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);

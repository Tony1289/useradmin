import React, { useState } from 'react';

function LoginForm({ role }) {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    securityCode: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // In a real app, you'd send this to a backend to verify
    console.log(`🔐 Attempting ${role} login`, formData);
    alert(`${role} login submitted (mock).`);
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '40px' }}>
      <h2>{role === 'admin' ? 'Admin' : 'User'} Login</h2>

      <form onSubmit={handleSubmit} style={{ maxWidth: '400px', margin: 'auto' }}>
        <input
          type="text"
          name="username"
          placeholder="Username or Email"
          value={formData.username}
          onChange={handleChange}
          required
          style={inputStyle}
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
          style={inputStyle}
        />

        {role === 'admin' && (
          <input
            type="text"
            name="securityCode"
            placeholder="Admin Security Code"
            value={formData.securityCode}
            onChange={handleChange}
            required
            style={inputStyle}
          />
        )}

        <button type="submit" style={buttonStyle}>
          Login
        </button>
      </form>
    </div>
  );
}

const inputStyle = {
  display: 'block',
  width: '100%',
  padding: '10px',
  margin: '10px 0',
  fontSize: '1rem',
};

const buttonStyle = {
  padding: '10px 20px',
  fontSize: '1rem',
  backgroundColor: '#28a745',
  color: 'white',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer',
};

export default LoginForm;

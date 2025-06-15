import React from 'react';
import { useNavigate } from 'react-router-dom';

function RoleSelector() {
  const navigate = useNavigate();

  const handleSelect = (role, action) => {
    navigate(`/${role}/${action}`);
  };

  return (
    <div style={containerStyle}>
      <h1>Select Your Role</h1>

      <div style={cardContainer}>
        <div style={cardStyle}>
          <h2>User</h2>
          <button style={buttonStyle} onClick={() => handleSelect('user', 'signup')}>
            Sign Up as User
          </button>
          <button style={buttonStyle} onClick={() => handleSelect('user', 'login')}>
            Login as User
          </button>
        </div>

        <div style={cardStyle}>
          <h2>Admin</h2>
          <button style={buttonStyle} onClick={() => handleSelect('admin', 'signup')}>
            Sign Up as Admin
          </button>
          <button style={buttonStyle} onClick={() => handleSelect('admin', 'login')}>
            Login as Admin
          </button>
        </div>
      </div>
    </div>
  );
}

const containerStyle = {
  textAlign: 'center',
  marginTop: '60px',
};

const cardContainer = {
  display: 'flex',
  justifyContent: 'center',
  gap: '30px',
  marginTop: '30px',
  flexWrap: 'wrap',
};

const cardStyle = {
  border: '1px solid #ccc',
  borderRadius: '8px',
  padding: '30px',
  width: '220px',
  boxShadow: '0 2px 6px rgba(0,0,0,0.1)',
};

const buttonStyle = {
  display: 'block',
  width: '100%',
  padding: '10px',
  margin: '10px 0',
  fontSize: '1rem',
  backgroundColor: '#007bff',
  color: 'white',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer',
};

export default RoleSelector;

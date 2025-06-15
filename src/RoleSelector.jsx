import React from 'react';
import { useNavigate } from 'react-router-dom';

function RoleSelector() {
  const navigate = useNavigate();

  const handleSelect = (role, action) => {
    navigate(`/${role}/${action}`);
  };

  return (
    <div style={styles.body}>
      <style>
        {`
          button:hover {
            opacity: 0.9;
          }
        `}
      </style>
      <h1 style={styles.heading}>Select Your Role</h1>
      <div style={styles.cardContainer}>
        <div style={styles.card}>
          <h2>User</h2>
          <button style={styles.button} onClick={() => handleSelect('user', 'signup')}>
            Sign Up as User
          </button>
          <button style={styles.button} onClick={() => handleSelect('user', 'login')}>
            Login as User
          </button>
        </div>

        <div style={styles.card}>
          <h2>Admin</h2>
          <button style={styles.button} onClick={() => handleSelect('admin', 'signup')}>
            Sign Up as Admin
          </button>
          <button style={styles.button} onClick={() => handleSelect('admin', 'login')}>
            Login as Admin
          </button>
        </div>
      </div>
    </div>
  );
}

const styles = {
  body: {
    minHeight: '100vh',
    backgroundImage:
      'url(https://img.playbook.com/IZSaaisbuPYRUSQYBZckzA61Px-1dJx2_5pGRp3N4dk/Z3M6Ly9wbGF5Ym9v/ay1hc3NldHMtcHVi/bGljLzRkZmUwYjQ2/LWRhNjAtNDQ2Yy1h/Y2UxLWM0ZTZkMGI3/NTdlMA)',
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    fontFamily: "'Poppins', sans-serif",
    padding: '60px 20px',
    textAlign: 'center',
    color: '#fff',
  },
  heading: {
    fontSize: '32px',
    marginBottom: '40px',
  },
  cardContainer: {
    display: 'flex',
    justifyContent: 'center',
    flexWrap: 'wrap',
    gap: '30px',
  },
  card: {
    background: 'rgba(255, 255, 255, 0.1)',
    backdropFilter: 'blur(15px)',
    border: '1px solid rgba(255, 255, 255, 0.2)',
    borderRadius: '12px',
    padding: '30px',
    width: '240px',
    boxShadow: '0 4px 10px rgba(0,0,0,0.2)',
  },
  button: {
    display: 'block',
    width: '100%',
    padding: '12px',
    margin: '10px 0',
    fontSize: '1rem',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '40px',
    cursor: 'pointer',
    fontWeight: 'bold',
  },
};

export default RoleSelector;

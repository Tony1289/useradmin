import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function AdminDashboard() {
  const [users, setUsers] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get('http://localhost:8000/admin/users')
      .then(response => {
        setUsers(response.data.users);
      })
      .catch(error => {
        console.error("Error fetching users:", error);
        alert("Session expired or unauthorized. Please login again.");
        navigate('/admin/login');
      });
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/admin/login');
  };

  const formatDateTime = (datetime) => {
    if (!datetime) return '—';
    const date = new Date(datetime);
    return (
      <>
        <div>{date.toLocaleDateString('en-GB')}</div>
        <div>{date.toLocaleTimeString('en-US')}</div>
      </>
    );
  };

  return (
    <>
      {/* Font Import */}
      <link
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap"
        rel="stylesheet"
      />

      <div style={styles.pageWrapper}>
        <div style={styles.container}>
          <h2 style={styles.title}>Admin Dashboard</h2>
          <div style={styles.tableWrapper}>
            <table style={styles.table}>
              <thead>
                <tr>
                  <th style={styles.th}>UserRole</th>
                  <th style={styles.th}>Email</th>
                  <th style={styles.th}>Password</th>
                  <th style={styles.th}>Login Time</th>
                  <th style={styles.th}>Logout Time</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user, index) => (
                  <tr key={index} style={index % 2 === 0 ? styles.rowEven : styles.rowOdd}>
                    <td style={styles.td}>{user.username}</td>
                    <td style={styles.td}>{user.hashed_email}</td>
                    <td style={styles.td}>{user.hashed_password}</td>
                    <td style={styles.td}>{formatDateTime(user.login_time)}</td>
                    <td style={styles.td}>{formatDateTime(user.logout_time)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div style={styles.logoutWrapper}>
            <button onClick={handleLogout} style={styles.logoutButton}>Logout</button>
          </div>
        </div>
      </div>
    </>
  );
}

const styles = {
  pageWrapper: {
    backgroundColor: '#1e1e2f',
    minHeight: '100vh',
    padding: '40px 20px',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'flex-start',
    fontFamily: "'Inter', sans-serif",
  },
  container: {
    width: '100%',
    maxWidth: '1100px',
    backgroundColor: '#ffffff',
    borderRadius: '12px',
    boxShadow: '0 8px 24px rgba(0, 0, 0, 0.2)',
    padding: '30px',
  },
  title: {
    fontSize: '28px',
    fontWeight: '700',
    marginBottom: '24px',
    color: '#1a1a1a',
    textAlign: 'center',
  },
  tableWrapper: {
    overflowX: 'auto',
    borderRadius: '8px',
    overflow: 'hidden',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    fontSize: '15px',
    textAlign: 'center',
  },
  th: {
    padding: '14px',
    backgroundColor: '#2d3748',
    color: '#ffffff',
    fontWeight: '600',
    borderBottom: '2px solid #4a5568',
  },
  td: {
    padding: '12px',
    borderBottom: '1px solid #e2e8f0',
    color: '#2d2d2d',
    wordBreak: 'break-word',
    textAlign: 'center',
  },
  rowEven: {
    backgroundColor: '#f7fafc',
    transition: 'background 0.3s',
  },
  rowOdd: {
    backgroundColor: '#ffffff',
    transition: 'background 0.3s',
  },
  logoutWrapper: {
    marginTop: '30px',
    textAlign: 'center',
  },
  logoutButton: {
    backgroundColor: '#e53e3e',
    color: 'white',
    padding: '10px 24px',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontWeight: '600',
    fontSize: '15px',
    transition: 'background 0.3s',
  },
};

export default AdminDashboard;

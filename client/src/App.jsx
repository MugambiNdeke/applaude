import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import LandingPage from './pages/landingPage';
import Dashboard from './pages/dashboard';

// Simple Authentication Mock (Replace with actual JWT/Context logic)
const isAuthenticated = () => {
    // In production, check for a valid JWT in localStorage
    return localStorage.getItem('access_token') === 'MOCK_TOKEN'; 
};

// Route Guard Component
const ProtectedRoute = ({ children }) => {
    if (!isAuthenticated()) {
        // Redirect non-authenticated users to the landing page
        return <Navigate to="/" replace />;
    }
    return children;
};


const App = () => {
  return (
    <Router>
      <Routes>
        {/* Public Route */}
        <Route path="/" element={<LandingPage />} />
        
        {/* Protected Route */}
        <Route path="/dashboard" element={
            <ProtectedRoute>
                <Dashboard />
            </ProtectedRoute>
        } />
        
        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
};

export default App;

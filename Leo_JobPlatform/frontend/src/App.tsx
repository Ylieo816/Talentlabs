import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import JobList from './components/JobList';
import JobForm from './components/JobForm';
import JobDetail from './components/JobDetail';
import SearchFilters from './components/SearchFilters';
import './App.css';

function App() {
  const [filters, setFilters] = useState({
    search: '',
    status: '',
    location: '',
    company: '',
    orderBy: 'posting_date',
    page: 1
  });

  const handleFilterChange = (newFilters: Partial<typeof filters>) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/create" className="nav-link">Post a Job</Link>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={
              <>
                <SearchFilters onFilterChange={handleFilterChange} />
                <JobList {...filters} />
              </>
            } />
            <Route path="/jobs/:id" element={<JobDetail />} />
            <Route path="/create" element={<JobForm />} />
            <Route path="/edit/:id" element={<JobForm />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 
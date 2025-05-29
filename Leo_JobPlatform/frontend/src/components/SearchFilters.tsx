import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

interface SearchFiltersProps {
  onFilterChange: (filters: {
    search?: string;
    status?: string;
    location?: string;
    company?: string;
    orderBy?: string;
    page?: number;
  }) => void;
}

const SearchFilters: React.FC<SearchFiltersProps> = ({ onFilterChange }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const searchParams = new URLSearchParams(location.search);

  const [filters, setFilters] = useState({
    search: searchParams.get('search') || '',
    status: searchParams.get('status') || '',
    location: searchParams.get('location') || '',
    company: searchParams.get('company') || '',
    orderBy: searchParams.get('order_by') || 'posting_date'
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  };

  const handleSearch = () => {
    const params = new URLSearchParams(location.search);
    
    // update all filters
    Object.entries(filters).forEach(([key, value]) => {
      if (value) {
        params.set(key === 'orderBy' ? 'order_by' : key, value);
      } else {
        params.delete(key === 'orderBy' ? 'order_by' : key);
      }
    });
    
    // reset page to the first page
    params.set('page', '1');
    navigate(`${location.pathname}?${params.toString()}`);
  };

  const handleReset = () => {
    // reset all filters to the default values
    setFilters({
      search: '',
      status: '',
      location: '',
      company: '',
      orderBy: 'posting_date'
    });
    
    // clear URL parameters, only keep the page number
    const params = new URLSearchParams();
    params.set('page', '1');
    navigate(`${location.pathname}?${params.toString()}`);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="search-filters">
      <div className="filter-group">
        <input
          type="text"
          name="search"
          placeholder="Search jobs..."
          value={filters.search}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          className="search-input"
        />
      </div>
      <div className="filter-group">
        <select
          name="status"
          value={filters.status}
          onChange={handleInputChange}
          className="filter-select"
        >
          <option value="">All Status</option>
          <option value="active">Active</option>
          <option value="expired">Expired</option>
          <option value="scheduled">Scheduled</option>
        </select>
      </div>
      <div className="filter-group">
        <input
          type="text"
          name="location"
          placeholder="Location"
          value={filters.location}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          className="filter-input"
        />
      </div>
      <div className="filter-group">
        <input
          type="text"
          name="company"
          placeholder="Company"
          value={filters.company}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          className="filter-input"
        />
      </div>
      <div className="filter-group">
        <select
          name="orderBy"
          value={filters.orderBy}
          onChange={handleInputChange}
          className="filter-select"
        >
          <option value="posting_date">Latest First</option>
          <option value="expiration_date">Expiring Soon</option>
        </select>
      </div>
      <div className="filter-group button-group">
        <button onClick={handleSearch} className="search-button">
          Search
        </button>
        <button onClick={handleReset} className="reset-button">
          Reset
        </button>
      </div>
    </div>
  );
};

export default SearchFilters; 
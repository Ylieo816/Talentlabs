import React from 'react';

interface SearchFiltersProps {
  onFilterChange: (filters: {
    search: string;
    status: string;
    location: string;
    company: string;
    orderBy: string;
  }) => void;
}

const SearchFilters: React.FC<SearchFiltersProps> = ({ onFilterChange }) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    onFilterChange({ [name]: value } as any);
  };

  return (
    <div className="search-filters">
      <div className="filter-group">
        <input
          type="text"
          name="search"
          placeholder="Search jobs..."
          onChange={handleChange}
          className="search-input"
        />
      </div>

      <div className="filter-group">
        <select name="status" onChange={handleChange} className="filter-select">
          <option value="">All Status</option>
          <option value="scheduled">Scheduled</option>
          <option value="active">Active</option>
          <option value="expired">Expired</option>
        </select>
      </div>

      <div className="filter-group">
        <input
          type="text"
          name="location"
          placeholder="Filter by location"
          onChange={handleChange}
          className="filter-input"
        />
      </div>

      <div className="filter-group">
        <input
          type="text"
          name="company"
          placeholder="Filter by company"
          onChange={handleChange}
          className="filter-input"
        />
      </div>

      <div className="filter-group">
        <select name="orderBy" onChange={handleChange} className="filter-select">
          <option value="posting_date">Sort by Posting Date</option>
          <option value="expiration_date">Sort by Expiration Date</option>
        </select>
      </div>
    </div>
  );
};

export default SearchFilters; 
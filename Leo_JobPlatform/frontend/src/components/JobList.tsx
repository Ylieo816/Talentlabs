import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLocation } from 'react-router-dom';

// Define job posting interface
interface Job {
  id: number;
  title: string;
  company: string;
  location: string;
  description: string;
  salary_range: string;
  required_skills: string[];
  posting_date: string;
  expiration_date: string;
  status: string;
}

// Define pagination response interface
interface PaginatedResponse {
  items: Job[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// JobList component for displaying and managing job postings
const JobList: React.FC = () => {
  // State for managing jobs data and UI states
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [pagination, setPagination] = useState({
    total: 0,
    page: 1,
    page_size: 10,
    total_pages: 0
  });
  const navigate = useNavigate();
  const location = useLocation();

  // Fetch jobs data from API with current search parameters
  const fetchJobs = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`http://localhost:8000/api/jobs${location.search}`);
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to fetch jobs');
      }
      
      const data: PaginatedResponse = await response.json();
      if (!data.items || !Array.isArray(data.items)) {
        throw new Error('Invalid response format');
      }
      
      setJobs(data.items);
      setPagination({
        total: data.total,
        page: data.page,
        page_size: data.page_size,
        total_pages: data.total_pages
      });
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred';
      setError(errorMessage);
      console.error('Error fetching jobs:', err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch jobs when search parameters change
  useEffect(() => {
    fetchJobs();
  }, [location.search]);

  // Navigate to job details page
  const handleJobClick = (jobId: number) => {
    try {
      navigate(`/jobs/${jobId}`);
    } catch (err) {
      console.error('Navigation error:', err);
      setError('Failed to navigate to job details');
    }
  };

  // Handle pagination navigation
  const handlePageChange = (newPage: number) => {
    try {
      const searchParams = new URLSearchParams(location.search);
      searchParams.set('page', newPage.toString());
      navigate(`${location.pathname}?${searchParams.toString()}`);
    } catch (err) {
      console.error('Pagination error:', err);
      setError('Failed to change page');
    }
  };

  // Show loading or error states
  if (loading) return <div>Loading...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="job-list-container">
      <div className="job-list">
        {jobs.map(job => (
          <div key={job.id} className="job-card" onClick={() => handleJobClick(job.id)}>
            <h2>{job.title}</h2>
            <h3>{job.company}</h3>
            <p>{job.location}</p>
            <p>{job.salary_range}</p>
            <div className="skills">
              {job.required_skills.map((skill, index) => (
                <span key={index} className="skill-tag">{skill}</span>
              ))}
            </div>
            <p>Posting Date: {job.posting_date.split('T')[0]}</p>
            <p>Expiration Date: {job.expiration_date.split('T')[0]}</p>
          </div>
        ))}
      </div>
      
      {/* Pagination controls */}
      {pagination.total_pages > 1 && (
        <div className="pagination">
          <button
            className="pagination-button"
            onClick={() => handlePageChange(pagination.page - 1)}
            disabled={pagination.page === 1}
          >
            Previous
          </button>
          
          <span className="page-info">
            Page {pagination.page} of {pagination.total_pages}
          </span>
          
          <button
            className="pagination-button"
            onClick={() => handlePageChange(pagination.page + 1)}
            disabled={pagination.page === pagination.total_pages}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default JobList; 
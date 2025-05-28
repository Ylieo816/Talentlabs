import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useLocation } from 'react-router-dom';

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

interface JobListProps {
  search?: string;
  status?: string;
  locationFilter?: string;
  company?: string;
  orderBy?: string;
  page?: number;
  pageSize?: number;
}

const JobList: React.FC<JobListProps> = ({
  search = '',
  status = '',
  locationFilter = '',
  company = '',
  orderBy = 'posting_date',
  page = 1,
  pageSize = 10
}) => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [totalPages, setTotalPages] = useState(1);
  const navigate = useNavigate();
  const routerLocation = useLocation();

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        setLoading(true);
        const params = new URLSearchParams({
          search,
          status,
          location: locationFilter,
          company,
          order_by: orderBy,
          page: page.toString(),
          page_size: pageSize.toString()
        });

        const response = await axios.get(`http://localhost:8000/api/jobs?${params}`);
        setJobs(response.data.items || response.data);
        setTotalPages(Math.ceil((response.data.total || response.data.length) / pageSize));
        setError(null);
      } catch (err) {
        setError('Failed to fetch jobs');
        console.error('Error fetching jobs:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchJobs();
  }, [search, status, locationFilter, company, orderBy, page, pageSize]);

  const handlePageChange = (newPage: number) => {
    const params = new URLSearchParams(routerLocation.search);
    params.set('page', newPage.toString());
    navigate(`${routerLocation.pathname}?${params.toString()}`);
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="job-list-container">
      <div className="job-list">
        {jobs.map(job => (
          <div key={job.id} className="job-card" onClick={() => navigate(`/jobs/${job.id}`)}>
            <h2>{job.title}</h2>
            <h3>{job.company}</h3>
            <p className="location">{job.location}</p>
            <p className="salary">{job.salary_range}</p>
            <div className="skills">
              {job.required_skills.map((skill, index) => (
                <span key={index} className="skill-tag">{skill}</span>
              ))}
            </div>
            <p className="description">{job.description}</p>
            <div className="dates">
              <span>Posted: {new Date(job.posting_date).toLocaleDateString()}</span>
              <br />
              <span>Expires: {new Date(job.expiration_date).toLocaleDateString()}</span>
            </div>
            {/* <div className="status">{job.status}</div> */}
          </div>
        ))}
      </div>
      
      {totalPages > 1 && (
        <div className="pagination">
          <button 
            onClick={() => handlePageChange(page - 1)}
            disabled={page === 1}
            className="pagination-button"
          >
            Previous
          </button>
          <span className="page-info">Page {page} of {totalPages}</span>
          <button 
            onClick={() => handlePageChange(page + 1)}
            disabled={page === totalPages}
            className="pagination-button"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default JobList; 
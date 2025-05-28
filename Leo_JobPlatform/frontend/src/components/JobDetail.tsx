import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

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

const JobDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [job, setJob] = useState<Job | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchJob = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`http://localhost:8000/api/jobs/${id}`);
        setJob(response.data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch job details');
        console.error('Error fetching job:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchJob();
  }, [id]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!job) return <div>Job not found</div>;

  return (
    <div className="job-detail">
      <button onClick={() => navigate(-1)} className="back-button">
        ← Back to Jobs
      </button>
      
      <div className="job-detail-card">
        <h1>{job.title}</h1>
        <h2>{job.company}</h2>
        
        <div className="job-meta">
          <p className="location">📍 {job.location}</p>
          <p className="salary">💰 {job.salary_range}</p>
          <p className="status">Status: {job.status}</p>
        </div>

        <div className="job-dates">
          <p>Posted: {new Date(job.posting_date).toLocaleDateString()}</p>
          <p>Expires: {new Date(job.expiration_date).toLocaleDateString()}</p>
        </div>

        <div className="job-description">
          <h3>Description</h3>
          <p>{job.description}</p>
        </div>

        <div className="job-skills">
          <h3>Required Skills</h3>
          <div className="skills-list">
            {job.required_skills.map((skill, index) => (
              <span key={index} className="skill-tag">{skill}</span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobDetail; 
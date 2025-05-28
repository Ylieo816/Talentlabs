import React, { useState } from 'react';
import axios from 'axios';

interface JobFormProps {
  jobId?: number;
  onSuccess?: () => void;
}

const JobForm: React.FC<JobFormProps> = ({ jobId, onSuccess }) => {
  const [formData, setFormData] = useState({
    title: '',
    company: '',
    location: '',
    description: '',
    salary_range: '',
    required_skills: '',
    posting_date: '',
    expiration_date: ''
  });

  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = {
        ...formData,
        required_skills: formData.required_skills.split(',').map(skill => skill.trim())
      };

      if (jobId) {
        await axios.put(`http://localhost:8000/api/jobs/${jobId}`, payload);
      } else {
        await axios.post('http://localhost:8000/api/jobs', payload);
      }

      setError(null);
      if (onSuccess) onSuccess();
    } catch (err) {
      setError('Failed to save job');
      console.error('Error saving job:', err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="job-form">
      {error && <div className="error">{error}</div>}
      
      <div className="form-group">
        <label htmlFor="title">Job Title</label>
        <input
          type="text"
          id="title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="company">Company</label>
        <input
          type="text"
          id="company"
          name="company"
          value={formData.company}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="location">Location</label>
        <input
          type="text"
          id="location"
          name="location"
          value={formData.location}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="salary_range">Salary Range</label>
        <input
          type="text"
          id="salary_range"
          name="salary_range"
          value={formData.salary_range}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="required_skills">Required Skills (comma-separated)</label>
        <input
          type="text"
          id="required_skills"
          name="required_skills"
          value={formData.required_skills}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="posting_date">Posting Date</label>
        <input
          type="date"
          id="posting_date"
          name="posting_date"
          value={formData.posting_date}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="expiration_date">Expiration Date</label>
        <input
          type="date"
          id="expiration_date"
          name="expiration_date"
          value={formData.expiration_date}
          onChange={handleChange}
          required
        />
      </div>

      <button type="submit" className="submit-button">
        {jobId ? 'Update Job' : 'Create Job'}
      </button>
    </form>
  );
};

export default JobForm; 
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';

interface JobFormData {
  title: string;
  company: string;
  location: string;
  description: string;
  salary_range: string;
  required_skills: string[];
  posting_date: string;
  expiration_date: string;
}

const JobForm: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const [formData, setFormData] = useState<JobFormData>({
    title: '',
    company: '',
    location: '',
    description: '',
    salary_range: '',
    required_skills: [],
    posting_date: new Date().toISOString().split('T')[0],
    expiration_date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
  });
  const [skillsInput, setSkillsInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    if (id) {
      const fetchJob = async () => {
        try {
          const response = await axios.get(`http://localhost:8000/api/jobs/${id}`);
          const job = response.data;
          setFormData({
            ...job,
            posting_date: new Date(job.posting_date).toISOString().split('T')[0],
            expiration_date: new Date(job.expiration_date).toISOString().split('T')[0]
          });
        } catch (err) {
          setError('Failed to fetch job details');
          console.error('Error fetching job:', err);
        }
      };
      fetchJob();
    }
  }, [id]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSkillsInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSkillsInput(e.target.value);
  };

  const handleSkillsInputKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && skillsInput.trim()) {
      e.preventDefault();
      if (!formData.required_skills.includes(skillsInput.trim())) {
        setFormData(prev => ({
          ...prev,
          required_skills: [...prev.required_skills, skillsInput.trim()]
        }));
      }
      setSkillsInput('');
    }
  };

  const removeSkill = (skillToRemove: string) => {
    setFormData(prev => ({
      ...prev,
      required_skills: prev.required_skills.filter(skill => skill !== skillToRemove)
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      if (id) {
        await axios.put(`http://localhost:8000/api/jobs/${id}`, formData);
      } else {
        await axios.post('http://localhost:8000/api/jobs', formData);
      }
      setSuccess(true);
      if (!id) {
        // 如果是創建新職位，清空表單
        setFormData({
          title: '',
          company: '',
          location: '',
          description: '',
          salary_range: '',
          required_skills: [],
          posting_date: new Date().toISOString().split('T')[0],
          expiration_date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
        });
        setSkillsInput('');
      }
    } catch (err) {
      setError('Failed to save job');
      console.error('Error saving job:', err);
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="success-message">
        <h2>Success!</h2>
        <p>{id ? 'Job has been updated successfully.' : 'Job has been created successfully.'}</p>
        <div className="success-actions">
          <button onClick={() => navigate('/')} className="button">
            View All Jobs
          </button>
          {!id && (
            <button onClick={() => setSuccess(false)} className="button">
              Create Another Job
            </button>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="job-form">
      <h1>{id ? 'Edit Job' : 'Post a New Job'}</h1>
      {error && <div className="error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Job Title</label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleInputChange}
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
            onChange={handleInputChange}
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
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleInputChange}
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
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="required_skills">Required Skills</label>
          <input
            type="text"
            value={skillsInput}
            onChange={handleSkillsInputChange}
            onKeyDown={handleSkillsInputKeyDown}
            placeholder="Type a skill and press Enter"
          />
          <div className="skills-list">
            {formData.required_skills.map((skill, index) => (
              <span key={index} className="skill-tag">
                {skill}
                <button
                  type="button"
                  onClick={() => removeSkill(skill)}
                  className="remove-skill"
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="posting_date">Posting Date</label>
          <input
            type="date"
            id="posting_date"
            name="posting_date"
            value={formData.posting_date}
            onChange={handleInputChange}
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
            onChange={handleInputChange}
            required
          />
        </div>

        <button type="submit" className="submit-button" disabled={loading}>
          {loading ? 'Saving...' : id ? 'Update Job' : 'Post Job'}
        </button>
      </form>
    </div>
  );
};

export default JobForm; 
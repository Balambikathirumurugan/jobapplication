import React, { useEffect, useState } from 'react';

function JobForm({ addJob, editingJob, updateJob, cancelEdit }) {
  const [company, setCompany] = useState('');
  const [role, setRole] = useState('');
  const [status, setStatus] = useState('Applied');

  // When editingJob changes, fill form fields
  useEffect(() => {
    if (editingJob) {
      setCompany(editingJob.company_name);
      setRole(editingJob.job_role);
      setStatus(editingJob.status);
    } else {
      setCompany('');
      setRole('');
      setStatus('Applied');
    }
  }, [editingJob]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!company || !role) return;

    const jobData = {
      company_name: company,
      job_role: role,
      status,
    };

    if (editingJob) {
      updateJob(editingJob.id, jobData);
    } else {
      addJob(jobData);
    }

    // Reset form if adding new job
    if (!editingJob) {
      setCompany('');
      setRole('');
      setStatus('Applied');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="job-form">
      <h2>{editingJob ? 'Edit Job' : 'Add Job'}</h2>
      <input
        type="text"
        placeholder="Company Name"
        value={company}
        onChange={(e) => setCompany(e.target.value)}
      />
      <input
        type="text"
        placeholder="Job Role"
        value={role}
        onChange={(e) => setRole(e.target.value)}
      />
      <select value={status} onChange={(e) => setStatus(e.target.value)}>
        <option>Applied</option>
        <option>Interviewing</option>
        <option>Offered</option>
        <option>Rejected</option>
      </select>
      <button type="submit">{editingJob ? 'Update Job' : 'Add Job'}</button>
      {editingJob && (
        <button type="button" onClick={cancelEdit} style={{ marginLeft: '10px' }}>
          Cancel
        </button>
      )}
    </form>
  );
}

export default JobForm;

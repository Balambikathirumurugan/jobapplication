import React, { useEffect, useState } from 'react';
import JobForm from './components/JobForm';
import JobList from './components/JobList';
import { getJobs, addJob as apiAddJob, updateJob, deleteJob } from './api';
import './App.css';

function App() {
  const [jobs, setJobs] = useState([]);
  const [editingJob, setEditingJob] = useState(null);

  // Load jobs from backend when component mounts
  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const response = await getJobs();
      setJobs(response.data);
    } catch (err) {
      console.error('Error fetching jobs:', err);
    }
  };

  const addJob = async (job) => {
    try {
      const response = await apiAddJob(job);
      setJobs([...jobs, response.data]);
    } catch (err) {
      console.error('Error adding job:', err);
    }
  };

  const editJob = (job) => {
    setEditingJob(job);
  };

  const updateJobDetails = async (id, updatedJob) => {
    try {
      const response = await updateJob(id, updatedJob);
      setJobs(jobs.map(job => job.id === id ? response.data : job));
      setEditingJob(null);
    } catch (err) {
      console.error('Error updating job:', err);
    }
  };

  const deleteJobById = async (id) => {
    try {
      await deleteJob(id);
      setJobs(jobs.filter(job => job.id !== id));
    } catch (err) {
      console.error('Error deleting job:', err);
    }
  };

  return (
    <div className="App">
      <JobForm
        addJob={addJob}
        editingJob={editingJob}
        updateJob={updateJobDetails}
        cancelEdit={() => setEditingJob(null)}
      />
      <JobList jobs={jobs} onEdit={editJob} onDelete={deleteJobById} />
    </div>
  );
}

export default App;

const JobList = ({ jobs, onEdit, onDelete }) => {
  return (
    <div className="job-list">
      <h2>Tracked Jobs</h2>
      <ul>
        {jobs.map((job) => (
          <li key={job.id}>
            <div>
              <strong>{job.company_name}</strong> - {job.job_role} <em>({job.status})</em>
            </div>
            <div className="job-item-buttons">
              <button onClick={() => onEdit(job)}>Edit</button>
              <button onClick={() => onDelete(job.id)}>Delete</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default JobList;

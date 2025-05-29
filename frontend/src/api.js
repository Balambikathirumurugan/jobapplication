import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/jobs';

export const getJobs = () => axios.get(API_URL);

export const addJob = (job) => axios.post(API_URL, job);

export const updateJob = (id, job) => axios.put(`${API_URL}/${id}`, job);

export const deleteJob = (id) => axios.delete(`${API_URL}/${id}`);

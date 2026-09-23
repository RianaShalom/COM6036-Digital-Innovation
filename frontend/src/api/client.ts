import axios from "axios";

// Creates the shared HTTP client used to communicate with the StudyBuddy API.
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// Adds the stored JWT to authenticated API requests.
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("studybuddy_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default apiClient;
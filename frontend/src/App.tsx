import { useEffect, useState } from "react";

import {
  getCurrentUser,
  logoutUser,
} from "./api/auth";
import type { User } from "./types/auth";

import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import DashboardPage from "./pages/DashboardPage";

type Page = "login" | "register" | "dashboard";

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [page, setPage] = useState<Page>("login");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("studybuddy_token");

    if (!token) {
      setLoading(false);
      return;
    }

    getCurrentUser()
      .then((currentUser) => {
        setUser(currentUser);
        setPage("dashboard");
      })
      .catch(() => {
        logoutUser();
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  function handleLogin(currentUser: User) {
    setUser(currentUser);
    setPage("dashboard");
  }

  function handleLogout() {
    logoutUser();
    setUser(null);
    setPage("login");
  }

  if (loading) {
    return (
      <main className="loading-screen">
        <p>Loading StudyBuddy...</p>
      </main>
    );
  }

  if (user && page === "dashboard") {
    return (
      <DashboardPage
        user={user}
        onLogout={handleLogout}
      />
    );
  }

  if (page === "register") {
    return (
      <RegisterPage
        onRegistered={() => setPage("login")}
        onLogin={() => setPage("login")}
      />
    );
  }

  return (
    <LoginPage
      onLogin={handleLogin}
      onRegister={() => setPage("register")}
    />
  );
}

export default App;
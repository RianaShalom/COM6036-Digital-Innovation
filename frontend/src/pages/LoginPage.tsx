import { useState } from "react";
import type { SubmitEvent } from "react";

import { getCurrentUser, loginUser } from "../api/auth";
import type { User } from "../types/auth";

interface LoginPageProps {
  onLogin: (user: User) => void;
  onRegister: () => void;
}

function LoginPage({
  onLogin,
  onRegister,
}: LoginPageProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: SubmitEvent) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      await loginUser(email, password);

      const user = await getCurrentUser();

      onLogin(user);
    } catch {
      setError("Incorrect email or password.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-card">
        <div className="brand">
          <h1>StudyBuddy</h1>
          <p>Plan your workload. Prioritise what matters.</p>
        </div>

        <h2>Sign in</h2>

        <form onSubmit={handleSubmit}>
          <label htmlFor="email">Email</label>

          <input
            id="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />

          <label htmlFor="password">Password</label>

          <input
            id="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />

          {error && (
            <p className="error-message">
              {error}
            </p>
          )}

          <button type="submit" disabled={loading}>
            {loading ? "Signing in..." : "Sign in"}
          </button>
        </form>

        <p className="auth-switch">
          Don't have an account?{" "}
          <button
            type="button"
            className="link-button"
            onClick={onRegister}
          >
            Create one
          </button>
        </p>
      </section>
    </main>
  );
}

export default LoginPage;
import { useState } from "react";
import type { SubmitEvent } from "react";

import { registerUser } from "../api/auth";

interface RegisterPageProps {
  onRegistered: () => void;
  onLogin: () => void;
}

function RegisterPage({
  onRegistered,
  onLogin,
}: RegisterPageProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmation, setConfirmation] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(
    event: SubmitEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setError("");

    if (password !== confirmation) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      await registerUser({
        email,
        password,
      });

      onRegistered();
    } catch (requestError: any) {
      if (requestError.response?.status === 409) {
        setError("An account with this email already exists.");
      } else {
        setError("Unable to create your account.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-card">
        <div className="brand">
          <h1>StudyBuddy</h1>
          <p>
            Build a clearer picture of your academic workload.
          </p>
        </div>

        <h2>Create account</h2>

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
            minLength={8}
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />

          <label htmlFor="confirmation">
            Confirm password
          </label>

          <input
            id="confirmation"
            type="password"
            minLength={8}
            value={confirmation}
            onChange={(event) =>
              setConfirmation(event.target.value)
            }
            required
          />

          {error && (
            <p className="error-message">
              {error}
            </p>
          )}

          <button type="submit" disabled={loading}>
            {loading
              ? "Creating account..."
              : "Create account"}
          </button>
        </form>

        <p className="auth-switch">
          Already have an account?{" "}
          <button
            type="button"
            className="link-button"
            onClick={onLogin}
          >
            Sign in
          </button>
        </p>
      </section>
    </main>
  );
}

export default RegisterPage;
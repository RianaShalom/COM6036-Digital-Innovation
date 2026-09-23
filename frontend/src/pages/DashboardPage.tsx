import { useEffect, useState } from "react";

import {
  completeTask,
  getPrioritisedTasks,
} from "../api/tasks";

import type { User } from "../types/auth";
import type { PrioritisedTask } from "../types/task";

interface DashboardPageProps {
  user: User;
  onLogout: () => void;
}

function DashboardPage({
  user,
  onLogout,
}: DashboardPageProps) {
  const [tasks, setTasks] = useState<PrioritisedTask[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadTasks() {
    try {
      setError("");

      const prioritisedTasks =
        await getPrioritisedTasks();

      setTasks(prioritisedTasks);
    } catch {
      setError("Unable to load your tasks.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadTasks();
  }, []);

  async function handleComplete(taskId: string) {
    try {
      await completeTask(taskId);

      await loadTasks();
    } catch {
      setError("Unable to complete the task.");
    }
  }

  return (
    <main className="dashboard">
      <header className="dashboard-header">
        <div>
          <p className="eyebrow">StudyBuddy</p>
          <h1>Your workload</h1>
          <p>{user.email}</p>
        </div>

        <button
          type="button"
          className="secondary-button"
          onClick={onLogout}
        >
          Sign out
        </button>
      </header>

      <section className="dashboard-intro">
        <h2>Prioritised tasks</h2>
        <p>
          Tasks are ordered using deadline, effort,
          difficulty and workload pressure.
        </p>
      </section>

      {error && (
        <p className="error-message">
          {error}
        </p>
      )}

      {loading ? (
        <p>Loading tasks...</p>
      ) : tasks.length === 0 ? (
        <section className="empty-state">
          <h3>No outstanding tasks</h3>
          <p>
            Create your first academic task to see
            StudyBuddy's prioritisation engine in action.
          </p>
        </section>
      ) : (
        <section className="task-list">
          {tasks.map((task) => (
            <article
              className="task-card"
              key={task.id}
            >
              <div className="task-card-header">
                <div>
                  <p className="task-module">
                    {task.module}
                  </p>

                  <h3>{task.title}</h3>
                </div>

                <span
                  className={`priority priority-${task.priority_level.toLowerCase()}`}
                >
                  {task.priority_level}
                </span>
              </div>

              <div className="task-details">
                <span>
                  Due{" "}
                  {new Date(
                    task.deadline,
                  ).toLocaleDateString()}
                </span>

                <span>
                  {task.estimated_hours} hours
                </span>

                <span>
                  Difficulty {task.difficulty}/5
                </span>

                <strong>
                  Priority {task.priority_score.toFixed(1)}
                </strong>
              </div>

              <button
                type="button"
                onClick={() => handleComplete(task.id)}
              >
                Mark complete
              </button>
            </article>
          ))}
        </section>
      )}
    </main>
  );
}

export default DashboardPage;
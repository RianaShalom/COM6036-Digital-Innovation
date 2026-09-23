import { useEffect, useState } from "react";

import {
  completeTask,
  createTask,
  getPrioritisedTasks,
} from "../api/tasks";

import type { User } from "../types/auth";
import type {
  CreateTaskRequest,
  PrioritisedTask,
} from "../types/task";

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
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const [title, setTitle] = useState("");
  const [module, setModule] = useState("");
  const [deadline, setDeadline] = useState("");
  const [estimatedHours, setEstimatedHours] = useState("2");
  const [difficulty, setDifficulty] = useState("3");
  const [description, setDescription] = useState("");

  async function loadTasks() {
    try {
      setError("");

      const prioritisedTasks = await getPrioritisedTasks();
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

  async function handleCreateTask(
    event: React.SubmitEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setError("");
    setSubmitting(true);

    const task: CreateTaskRequest = {
      title,
      module,
      deadline: new Date(deadline).toISOString(),
      estimated_hours: Number(estimatedHours),
      difficulty: Number(difficulty),
      ...(description.trim()
        ? { description: description.trim() }
        : {}),
    };

    try {
      await createTask(task);

      setTitle("");
      setModule("");
      setDeadline("");
      setEstimatedHours("2");
      setDifficulty("3");
      setDescription("");

      await loadTasks();
    } catch {
      setError("Unable to create the task.");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleComplete(taskId: string) {
    try {
      setError("");

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

      {error && <p className="error-message">{error}</p>}

      <section className="create-task-card">
        <div className="section-heading">
          <div>
            <p className="eyebrow">New task</p>
            <h2>Add an academic task</h2>
          </div>

          <p>
            StudyBuddy will calculate its priority using
            deadline, effort, difficulty and workload pressure.
          </p>
        </div>

        <form
          className="task-form"
          onSubmit={handleCreateTask}
        >
          <div className="form-field form-field-wide">
            <label htmlFor="task-title">Task title</label>
            <input
              id="task-title"
              type="text"
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              placeholder="e.g. Complete distributed systems report"
              maxLength={200}
              required
            />
          </div>

          <div className="form-field">
            <label htmlFor="task-module">Module</label>
            <input
              id="task-module"
              type="text"
              value={module}
              onChange={(event) => setModule(event.target.value)}
              placeholder="e.g. COM6036"
              maxLength={100}
              required
            />
          </div>

          <div className="form-field">
            <label htmlFor="task-deadline">Deadline</label>
            <input
              id="task-deadline"
              type="datetime-local"
              value={deadline}
              onChange={(event) => setDeadline(event.target.value)}
              required
            />
          </div>

          <div className="form-field">
            <label htmlFor="task-hours">
              Estimated hours
            </label>
            <input
              id="task-hours"
              type="number"
              min="0.25"
              max="100"
              step="0.25"
              value={estimatedHours}
              onChange={(event) =>
                setEstimatedHours(event.target.value)
              }
              required
            />
          </div>

          <div className="form-field">
            <label htmlFor="task-difficulty">
              Difficulty
            </label>
            <select
              id="task-difficulty"
              value={difficulty}
              onChange={(event) =>
                setDifficulty(event.target.value)
              }
            >
              <option value="1">1 — Very easy</option>
              <option value="2">2 — Easy</option>
              <option value="3">3 — Moderate</option>
              <option value="4">4 — Difficult</option>
              <option value="5">5 — Very difficult</option>
            </select>
          </div>

          <div className="form-field form-field-wide">
            <label htmlFor="task-description">
              Description <span>(optional)</span>
            </label>
            <textarea
              id="task-description"
              value={description}
              onChange={(event) =>
                setDescription(event.target.value)
              }
              placeholder="Add useful context about the task..."
              rows={3}
            />
          </div>

          <div className="form-actions">
            <button type="submit" disabled={submitting}>
              {submitting ? "Adding task..." : "Add task"}
            </button>
          </div>
        </form>
      </section>

      <section className="dashboard-intro">
        <div>
          <p className="eyebrow">Priority engine</p>
          <h2>Prioritised tasks</h2>
          <p>
            Outstanding tasks are ordered according to their
            calculated priority score.
          </p>
        </div>
      </section>

      {loading ? (
        <p>Loading tasks...</p>
      ) : tasks.length === 0 ? (
        <section className="empty-state">
          <h3>No outstanding tasks</h3>
          <p>
            Create your first academic task above to see
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

              {task.description && (
                <p className="task-description">
                  {task.description}
                </p>
              )}

              <div className="task-details">
                <span>
                  Due{" "}
                  {new Date(
                    task.deadline,
                  ).toLocaleString()}
                </span>

                <span>
                  {task.estimated_hours} hours
                </span>

                <span>
                  Difficulty {task.difficulty}/5
                </span>

                <strong>
                  Priority{" "}
                  {task.priority_score.toFixed(1)}
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
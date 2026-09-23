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
  // Stores the authenticated user's outstanding tasks.
  const [tasks, setTasks] = useState<PrioritisedTask[]>([]);

  // Controls the loading state while tasks are retrieved.
  const [loading, setLoading] = useState(true);

  // Controls the loading state while a new task is being created.
  const [submitting, setSubmitting] = useState(false);

  // Stores an error message that can be displayed to the user.
  const [error, setError] = useState("");

  // Stores the values entered into the new-task form.
  const [title, setTitle] = useState("");
  const [module, setModule] = useState("");
  const [deadline, setDeadline] = useState("");
  const [estimatedHours, setEstimatedHours] = useState("2");
  const [difficulty, setDifficulty] = useState("3");
  const [description, setDescription] = useState("");

  // Calculates the total estimated hours across all outstanding tasks.
  const totalHours = tasks.reduce(
    (total, task) =>
      total + Number(task.estimated_hours),
    0,
  );

  // Counts tasks in each priority category for the workload summary.
  const criticalCount = tasks.filter(
    (task) => task.priority_level === "Critical",
  ).length;

  const highCount = tasks.filter(
    (task) => task.priority_level === "High",
  ).length;

  const mediumCount = tasks.filter(
    (task) => task.priority_level === "Medium",
  ).length;

  const lowCount = tasks.filter(
    (task) => task.priority_level === "Low",
  ).length;

  // Retrieves the user's outstanding tasks from the prioritisation endpoint.
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

  // Loads the user's tasks when the dashboard is first displayed.
  useEffect(() => {
    loadTasks();
  }, []);

  // Sends a new academic task to the backend.
  async function handleCreateTask(
    event: React.SubmitEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setError("");
    setSubmitting(true);

    // Converts the form values into the structure expected by the API.
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

      // Clears the form after the task has been created successfully.
      setTitle("");
      setModule("");
      setDeadline("");
      setEstimatedHours("2");
      setDifficulty("3");
      setDescription("");

      // Reloads the prioritised list so the new task appears
      // in its calculated position.
      await loadTasks();
    } catch {
      setError("Unable to create the task.");
    } finally {
      setSubmitting(false);
    }
  }

  // Marks a task as completed and refreshes the dashboard.
  async function handleComplete(taskId: string) {
    try {
      setError("");

      await completeTask(taskId);

      // The completed task should no longer appear in the
      // outstanding prioritised task list.
      await loadTasks();
    } catch {
      setError("Unable to complete the task.");
    }
  }

  return (
    <main className="dashboard">
      {/* Displays the application identity and authenticated user. */}
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

      {/* Displays API errors without interrupting the dashboard. */}
      {error && (
        <p className="error-message">
          {error}
        </p>
      )}

      {/* Provides the form used to create a new academic task. */}
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
            <label htmlFor="task-title">
              Task title
            </label>

            <input
              id="task-title"
              type="text"
              value={title}
              onChange={(event) =>
                setTitle(event.target.value)
              }
              placeholder="e.g. Complete distributed systems report"
              maxLength={200}
              required
            />
          </div>

          <div className="form-field">
            <label htmlFor="task-module">
              Module
            </label>

            <input
              id="task-module"
              type="text"
              value={module}
              onChange={(event) =>
                setModule(event.target.value)
              }
              placeholder="e.g. COM6036"
              maxLength={100}
              required
            />
          </div>

          <div className="form-field">
            <label htmlFor="task-deadline">
              Deadline
            </label>

            <input
              id="task-deadline"
              type="datetime-local"
              value={deadline}
              onChange={(event) =>
                setDeadline(event.target.value)
              }
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
              <option value="1">
                1 — Very easy
              </option>

              <option value="2">
                2 — Easy
              </option>

              <option value="3">
                3 — Moderate
              </option>

              <option value="4">
                4 — Difficult
              </option>

              <option value="5">
                5 — Very difficult
              </option>
            </select>
          </div>

          <div className="form-field form-field-wide">
            <label htmlFor="task-description">
              Description{" "}
              <span>(optional)</span>
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
            <button
              type="submit"
              disabled={submitting}
            >
              {submitting
                ? "Adding task..."
                : "Add task"}
            </button>
          </div>
        </form>
      </section>

      {/* Displays a summary of the user's current academic workload. */}
      <section className="workload-summary">
        <div className="summary-card">
          <span>Outstanding tasks</span>

          <strong>{tasks.length}</strong>
        </div>

        <div className="summary-card">
          <span>Estimated workload</span>

          <strong>
            {totalHours.toFixed(1)}h
          </strong>
        </div>

        <div className="summary-card">
          <span>Critical</span>

          <strong>{criticalCount}</strong>
        </div>

        <div className="summary-card">
          <span>High</span>

          <strong>{highCount}</strong>
        </div>

        <div className="summary-card">
          <span>Medium</span>

          <strong>{mediumCount}</strong>
        </div>

        <div className="summary-card">
          <span>Low</span>

          <strong>{lowCount}</strong>
        </div>
      </section>

      {/* Introduces the calculated priority list. */}
      <section className="dashboard-intro">
        <div>
          <p className="eyebrow">
            Priority engine
          </p>

          <h2>Prioritised tasks</h2>

          <p>
            Outstanding tasks are ordered according
            to their calculated priority score.
          </p>
        </div>
      </section>

      {/* Shows an appropriate state while tasks are being retrieved. */}
      {loading ? (
        <p>Loading tasks...</p>
      ) : tasks.length === 0 ? (
        <section className="empty-state">
          <h3>No outstanding tasks</h3>

          <p>
            Create your first academic task above
            to see StudyBuddy's prioritisation
            engine in action.
          </p>
        </section>
      ) : (
        <section className="task-list">
          {tasks.map((task) => (
            <article
              className="task-card"
              key={task.id}
            >
              {/* Displays the task's module, title and calculated priority. */}
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

              {/* Displays the optional task description. */}
              {task.description && (
                <p className="task-description">
                  {task.description}
                </p>
              )}

              {/* Displays the basic task information and overall score. */}
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

              {/* Explains the individual factors contributing to the priority score. */}
              <div className="priority-explanation">
                <h4>Why this priority?</h4>

                <div className="factor-list">
                  <div>
                    <span>
                      Deadline urgency
                    </span>

                    <strong>
                      {task.priority_factors.urgency.toFixed(
                        1,
                      )}
                      /100
                    </strong>
                  </div>

                  <div>
                    <span>
                      Estimated effort
                    </span>

                    <strong>
                      {task.priority_factors.effort.toFixed(
                        1,
                      )}
                      /100
                    </strong>
                  </div>

                  <div>
                    <span>
                      Difficulty
                    </span>

                    <strong>
                      {task.priority_factors.difficulty.toFixed(
                        1,
                      )}
                      /100
                    </strong>
                  </div>

                  <div>
                    <span>
                      Workload pressure
                    </span>

                    <strong>
                      {task.priority_factors.workload_pressure.toFixed(
                        1,
                      )}
                      /100
                    </strong>
                  </div>
                </div>
              </div>

              {/* Allows the user to remove a completed task
                  from the outstanding workload. */}
              <button
                type="button"
                onClick={() =>
                  handleComplete(task.id)
                }
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
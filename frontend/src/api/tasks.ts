import apiClient from "./client";
import type {
  CreateTaskRequest,
  PrioritisedTask,
  Task,
} from "../types/task";

// Retrieves all tasks belonging to the authenticated user.
export async function getTasks(): Promise<Task[]> {
  const response = await apiClient.get<Task[]>("/api/tasks");

  return response.data;
}

// Retrieves outstanding tasks ordered by calculated priority.
export async function getPrioritisedTasks(): Promise<PrioritisedTask[]> {
  const response = await apiClient.get<PrioritisedTask[]>(
    "/api/tasks/prioritized",
  );

  return response.data;
}

// Creates a new task.
export async function createTask(
  data: CreateTaskRequest,
): Promise<Task> {
  const response = await apiClient.post<Task>(
    "/api/tasks",
    data,
  );

  return response.data;
}

// Marks a task as completed.
export async function completeTask(
  taskId: string,
): Promise<Task> {
  const response = await apiClient.post<Task>(
    `/api/tasks/${taskId}/complete`,
  );

  return response.data;
}
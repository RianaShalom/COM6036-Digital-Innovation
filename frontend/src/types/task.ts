export type TaskStatus = "pending" | "completed";

export interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  module: string;
  deadline: string;
  estimated_hours: string;
  difficulty: number;
  status: TaskStatus;
  created_at: string;
  completed_at: string | null;
}

export interface PrioritisedTask extends Task {
  priority_score: number;
  priority_level: string;
  priority_factors: PriorityFactors;
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
  module: string;
  deadline: string;
  estimated_hours: number;
  difficulty: number;
}

export interface PriorityFactors {
  urgency: number;
  effort: number;
  difficulty: number;
  workload_pressure: number;
}
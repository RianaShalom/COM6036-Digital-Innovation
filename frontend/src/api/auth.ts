import apiClient from "./client";
import type {
  RegisterRequest,
  TokenResponse,
  User,
} from "../types/auth";

// Registers a new StudyBuddy user.
export async function registerUser(
  data: RegisterRequest,
): Promise<User> {
  const response = await apiClient.post<User>(
    "/api/auth/register",
    data,
  );

  return response.data;
}

// Authenticates a user and stores the returned JWT.
export async function loginUser(
  email: string,
  password: string,
): Promise<TokenResponse> {
  const formData = new URLSearchParams();

  formData.append("username", email);
  formData.append("password", password);

  const response = await apiClient.post<TokenResponse>(
    "/api/auth/login",
    formData,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    },
  );

  localStorage.setItem(
    "studybuddy_token",
    response.data.access_token,
  );

  return response.data;
}

// Retrieves the currently authenticated user.
export async function getCurrentUser(): Promise<User> {
  const response = await apiClient.get<User>("/api/auth/me");

  return response.data;
}

// Removes the locally stored authentication token.
export function logoutUser(): void {
  localStorage.removeItem("studybuddy_token");
}
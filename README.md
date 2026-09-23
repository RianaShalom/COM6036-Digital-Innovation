# COM6036-Digital-Innovation
GitHub Repo for the assignment: You are required to individually design, develop and document a web-based distributed application or service that addresses a clearly defined real-world problem


## Current Progress

StudyBuddy currently provides the core backend foundation for workload-aware academic task planning.

### Implemented

* FastAPI backend with a layered architecture
* PostgreSQL database integration
* User registration and authentication
* Secure password hashing using Argon2
* JWT-based authentication and protected API endpoints
* User-specific task data isolation
* Task creation, retrieval, updating and deletion
* Task difficulty and estimated-effort modelling
* Explainable priority scoring based on:

  * Deadline urgency
  * Estimated effort
  * Task difficulty
  * Workload pressure
* Workload-pressure calculation based on outstanding work and available study capacity
* Automated unit tests for the priority and workload calculation logic
* OpenAPI/Swagger API documentation through FastAPI

### Testing

The current priority and workload calculation test suite contains **18 passing tests**.

```text
18 passed
```

### Next Steps

The next development milestone is to connect the workload calculation to the user's stored tasks and expose a prioritized task endpoint. This will allow StudyBuddy to dynamically calculate and return task priorities based on the user's actual outstanding workload.

Further planned functionality includes task completion, study-session tracking, dashboard statistics, frontend development and deployment.

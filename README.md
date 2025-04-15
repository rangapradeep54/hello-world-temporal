# hello-world-temporal
This app is dockerized and uses Podman Compose for orchestration.

🛠️ Prerequisites
Before you get started, make sure you have the following installed:

Podman (to run containers)

Podman Compose (for managing multi-container setups)

Python 3.11+ (for running the app code)

📦 Setup
1. Clone the repository
bash
Copy
Edit
git clone https://github.com/rangapradeep54/hello-world-temporal.git
cd hello-world-temporal
2. Build and start the containers
Use Podman Compose to set up the containers (Temporal server, Postgres, and the Python app):

podman-compose up --build -d
This will:

Start Temporal server (temporal container)

Start PostgreSQL (temporal-postgres container)

Start the Python app (your-python-app container)

🚀 Running the app
1. Running the Worker
To start the worker that will listen to the Temporal task queue, run:
podman-compose exec your-python-app python app.py worker

2. Triggering Workflows
To trigger workflows and observe the results:

podman-compose exec your-python-app python app.py trigger
The worker and workflow will run concurrently. Workflow results will be printed in the logs.

🔧 Configuration
The app uses Temporal's default configuration, which connects to the temporal:7233 server. If your server setup or Temporal network changes, update the Client.connect("temporal:7233") in app.py to reflect the correct address.

🧑‍💻 Code Overview
app.py
Defines one Temporal workflow and activity:

say_hello: An activity that says hello to a given name.

HelloWorkflow: A workflow that executes the say_hello activity.

The worker polls the Temporal task queue (hello-task-queue) for tasks to execute.

The trigger function initiates the workflow execution with a sample input.

Retry Logic
The connection to Temporal is set to retry up to 5 times with a 3-second delay, in case Temporal is not immediately available.

🌐 Temporal UI
You can access the Temporal Web UI at http://localhost:8088 to monitor the status of workflows and activities.

⚙️ Docker Compose Configuration
The docker-compose.yml file sets up the following services:

Postgres for Temporal's database.

Temporal Auto-Setup for running the Temporal server.

Temporal Web UI for monitoring workflows.

Your Python app for running the worker and triggering workflows.

Ports Exposed:
7233: Temporal API (for worker connection).

8088: Temporal Web UI.

5432: Postgres database (default).

📝 Notes
Temporal workflows and activities are defined with decorators (@workflow.defn and @activity.defn).

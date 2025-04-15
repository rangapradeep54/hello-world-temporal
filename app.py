import asyncio
from datetime import timedelta
from temporalio import workflow, activity
from temporalio.client import Client
from temporalio.worker import Worker


@activity.defn
async def say_hello(name: str) -> str:
    return f"Hello, {name}!"


@workflow.defn
class HelloWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_activity(
            say_hello,
            name,
            start_to_close_timeout=timedelta(seconds=5),
        )


async def connect_with_retry(retries: int = 5, delay: int = 3) -> Client:
    for attempt in range(1, retries + 1):
        try:
            print(f"Attempting to connect to Temporal (try {attempt}/{retries})...")
            client = await Client.connect("temporal:7233")
            print("Connected to Temporal!")
            return client
        except Exception as e:
            print(f"Connection attempt {attempt} failed: {e}")
            if attempt < retries:
                await asyncio.sleep(delay)
            else:
                raise RuntimeError("Failed to connect to Temporal after retries")


async def main():
    client = await connect_with_retry()

    # Run worker
    worker = Worker(
        client,
        task_queue="hello-task-queue",
        workflows=[HelloWorkflow],
        activities=[say_hello],
    )

    # Start the worker in the background
    asyncio.create_task(worker.run())

    # Delay briefly to let the worker start
    await asyncio.sleep(2)

    # Start a workflow execution
    result = await client.execute_workflow(
        HelloWorkflow.run,
        "World",
        id="hello-workflow-id",
        task_queue="hello-task-queue",
    )
    print(f"Workflow result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
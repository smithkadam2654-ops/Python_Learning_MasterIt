import asyncio
import time

async def fetch_data(task_id, delay):
    """Simulates an asynchronous data fetch operation."""
    print(f"Task {task_id}: Starting fetch (will take {delay} seconds)...")
    # asyncio.sleep is non-blocking, allowing other tasks to run
    await asyncio.sleep(delay)
    print(f"Task {task_id}: Fetch complete!")
    return f"Data from task {task_id}"

async def main():
    """Runs multiple asynchronous tasks concurrently."""
    start_time = time.time()
    
    print("Starting all tasks concurrently...")
    
    # Create a list of tasks to run concurrently
    # Even though total delay is 1+2+3 = 6 seconds, 
    # it will only take ~3 seconds total because they run concurrently!
    tasks = [
        fetch_data(1, 2.0),
        fetch_data(2, 1.0),
        fetch_data(3, 3.0)
    ]
    
    # Wait for all tasks to complete and gather their results
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"\nAll tasks finished in {end_time - start_time:.2f} seconds")
    print(f"Results: {results}")

if __name__ == "__main__":
    # The entry point for running asyncio programs
    asyncio.run(main())

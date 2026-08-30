import asyncio
import time

async def fetch_data(task_id, delay):
    print(f"Task {task_id}: Starting to fetch data (will take {delay} seconds)...")
    
    # Simulate an I/O bound operation (like a network request or database query)
    # Using asyncio.sleep instead of time.sleep lets other tasks run during the wait!
    await asyncio.sleep(delay)
    
    print(f"Task {task_id}: Finished fetching data.")
    return f"Data from task {task_id}"

async def main():
    start_time = time.time()
    
    print("Gathering tasks concurrently...")
    
    # asyncio.gather runs the tasks concurrently (at the same time) and waits for all to finish.
    # Task 1 takes 2 seconds, Task 2 takes 3 seconds, Task 3 takes 1 second
    results = await asyncio.gather(
        fetch_data(1, 2),
        fetch_data(2, 3),
        fetch_data(3, 1)
    )
    
    end_time = time.time()
    
    print("\nResults collected:", results)
    
    # Because they ran concurrently, the total time should be roughly 
    # equal to the longest individual task (3 seconds), rather than 2+3+1 = 6 seconds.
    print(f"Total execution time: {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    # This is how you start the event loop for an asyncio program
    asyncio.run(main())

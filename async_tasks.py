import asyncio
import time
import random

async def process_item(item_id: int) -> str:
    """Simulates an I/O bound task like a network request."""
    print(f"Task {item_id}: Starting...")
    # Simulate variable network delay
    delay = random.uniform(0.5, 2.0)
    await asyncio.sleep(delay)
    
    # Simulate potential failure
    if random.random() < 0.1:
        print(f"Task {item_id}: Failed!")
        raise RuntimeError(f"Simulated failure in task {item_id}")
        
    print(f"Task {item_id}: Completed in {delay:.2f}s")
    return f"Result of Task {item_id}"

async def main():
    print("Starting asynchronous batch processing...")
    start_time = time.perf_counter()
    
    # Create a batch of tasks
    tasks = [process_item(i) for i in range(1, 6)]
    
    # Run tasks concurrently and gather results, handling exceptions
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    end_time = time.perf_counter()
    
    print(f"\nAll tasks finished in {end_time - start_time:.2f} seconds.")
    print("Results:")
    for i, result in enumerate(results, 1):
        if isinstance(result, Exception):
            print(f"  Task {i} ended with an error: {result}")
        else:
            print(f"  Task {i} output: {result}")

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import time

async def fetch_data(id, delay):
    """An asynchronous coroutine simulating a network request or database query."""
    print(f"Task {id}: Starting fetch... (will take {delay} seconds)")
    
    # await gives control back to the event loop while we wait
    await asyncio.sleep(delay) 
    
    print(f"Task {id}: Finished fetch!")
    return f"Data for ID {id}"

async def main():
    """The main coroutine that manages the execution of other tasks."""
    print("--- Starting Async Execution ---")
    start_time = time.time()
    
    # Create a list of tasks we want to run concurrently
    tasks = [
        fetch_data(1, 2.0), # Takes 2 seconds
        fetch_data(2, 3.0), # Takes 3 seconds
        fetch_data(3, 1.0)  # Takes 1 second
    ]
    
    # asyncio.gather runs all tasks concurrently and waits for them all to finish
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    
    print("\n--- All Tasks Complete ---")
    print(f"Results: {results}")
    
    # Notice that it took ~3 seconds total (the longest task), not 6 seconds!
    print(f"Total time elapsed: {end_time - start_time:.2f} seconds")

def demonstrate_asyncio():
    # To run top-level async code, we need to pass it to the event loop
    asyncio.run(main())

if __name__ == "__main__":
    demonstrate_asyncio()

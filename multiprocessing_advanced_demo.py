import concurrent.futures
import time

def process_image(image_name):
    """Simulate CPU-bound work (like image processing)."""
    print(f"[{image_name}] Starting processing...")
    # Simulate heavy computation
    time.sleep(2)
    result = f"Processed {image_name}"
    print(f"[{image_name}] Finished processing!")
    return result

def demonstrate_concurrent_futures():
    """Demonstrate how to run CPU-bound tasks in parallel."""
    images = ['photo_1.jpg', 'photo_2.jpg', 'photo_3.jpg', 'photo_4.jpg']
    
    print("--- Using ProcessPoolExecutor ---")
    start_time = time.time()
    
    # ProcessPoolExecutor uses separate Python processes (bypassing the GIL)
    # This is perfect for CPU-bound tasks!
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # map() automatically handles chunking and running the function on all inputs
        results = executor.map(process_image, images)
        
        print("\nGathering results:")
        for res in results:
            print(res)
            
    end_time = time.time()
    
    # If run sequentially, 4 images * 2 seconds = 8 seconds.
    # With multiprocessing (assuming a multi-core CPU), it should take ~2-4 seconds!
    print(f"\nTotal time elapsed: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    # Required for Windows when using multiprocessing
    demonstrate_concurrent_futures()

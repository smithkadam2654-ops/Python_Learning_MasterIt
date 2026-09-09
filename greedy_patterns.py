"""
Greedy Algorithms - Common greedy problem patterns.
Features: Activity selection, interval scheduling, and optimization problems.
"""

from typing import List, Tuple


class GreedyPatterns:
    """Common greedy algorithm patterns and solutions."""
    
    @staticmethod
    def activity_selection(activities: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Select maximum number of non-overlapping activities.
        
        Args:
            activities: List of (start, end) tuples
            
        Returns:
            List of selected activities
        """
        # Sort by end time
        sorted_activities = sorted(activities, key=lambda x: x[1])
        
        selected = []
        last_end = -1
        
        for start, end in sorted_activities:
            if start >= last_end:
                selected.append((start, end))
                last_end = end
        
        return selected
    
    @staticmethod
    def interval_scheduling(intervals: List[Tuple[int, int]]) -> int:
        """
        Maximum number of non-overlapping intervals.
        
        Args:
            intervals: List of (start, end) tuples
            
        Returns:
            Maximum count
        """
        if not intervals:
            return 0
        
        intervals.sort(key=lambda x: x[1])
        
        count = 1
        last_end = intervals[0][1]
        
        for start, end in intervals[1:]:
            if start >= last_end:
                count += 1
                last_end = end
        
        return count
    
    @staticmethod
    def minimum_coins(coins: List[int], amount: int) -> List[int]:
        """
        Minimum number of coins to make amount (canonical coin systems only).
        
        Args:
            coins: List of coin denominations (sorted descending)
            amount: Target amount
            
        Returns:
            List of coins used
        """
        coins.sort(reverse=True)
        result = []
        
        for coin in coins:
            while amount >= coin:
                amount -= coin
                result.append(coin)
        
        return result if amount == 0 else []
    
    @staticmethod
    def fractional_knapsack(weights: List[int], values: List[int], 
                          capacity: int) -> Tuple[float, List[Tuple[int, float]]]:
        """
        Fractional knapsack problem (items can be divided).
        
        Args:
            weights: List of weights
            values: List of values
            capacity: Knapsack capacity
            
        Returns:
            Tuple of (total_value, list of (item_index, fraction_taken))
        """
        n = len(weights)
        # Calculate value per weight
        items = [(i, values[i] / weights[i], weights[i], values[i]) 
                for i in range(n)]
        # Sort by value per weight descending
        items.sort(key=lambda x: x[1], reverse=True)
        
        total_value = 0.0
        selected = []
        remaining_capacity = capacity
        
        for idx, ratio, weight, value in items:
            if remaining_capacity <= 0:
                break
            
            if weight <= remaining_capacity:
                total_value += value
                selected.append((idx, 1.0))
                remaining_capacity -= weight
            else:
                fraction = remaining_capacity / weight
                total_value += value * fraction
                selected.append((idx, fraction))
                remaining_capacity = 0
        
        return (total_value, selected)
    
    @staticmethod
    def job_sequencing(jobs: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
        """
        Job sequencing with deadlines (maximize profit).
        
        Args:
            jobs: List of (job_id, deadline, profit) tuples
            
        Returns:
            List of scheduled jobs
        """
        # Sort by profit descending
        jobs.sort(key=lambda x: x[2], reverse=True)
        
        max_deadline = max(job[1] for job in jobs) if jobs else 0
        slots = [None] * max_deadline
        scheduled = []
        
        for job_id, deadline, profit in jobs:
            # Find latest available slot
            for i in range(min(deadline, max_deadline) - 1, -1, -1):
                if slots[i] is None:
                    slots[i] = (job_id, deadline, profit)
                    scheduled.append((job_id, deadline, profit))
                    break
        
        return scheduled
    
    @staticmethod
    def huffman_encoding(frequencies: dict) -> dict:
        """
        Huffman encoding for lossless data compression.
        
        Args:
            frequencies: Dictionary of character to frequency
            
        Returns:
            Dictionary of character to binary code
        """
        import heapq
        
        # Create leaf nodes
        heap = [[freq, [char, ""]] for char, freq in frequencies.items()]
        heapq.heapify(heap)
        
        while len(heap) > 1:
            # Pop two smallest
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            
            # Add 0 to left, 1 to right
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            
            # Push combined node
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        
        # Extract codes
        codes = {}
        for char, code in heap[0][1:]:
            codes[char] = code
        
        return codes
    
    @staticmethod
    def minimum_platforms(arrivals: List[int], departures: List[int]) -> int:
        """
        Minimum number of platforms required for railway station.
        
        Args:
            arrivals: List of arrival times
            departures: List of departure times
            
        Returns:
            Minimum platforms needed
        """
        arrivals.sort()
        departures.sort()
        
        platforms_needed = 1
        max_platforms = 1
        i = 1  # arrival pointer
        j = 0  # departure pointer
        
        while i < len(arrivals) and j < len(departures):
            if arrivals[i] <= departures[j]:
                platforms_needed += 1
                i += 1
                max_platforms = max(max_platforms, platforms_needed)
            else:
                platforms_needed -= 1
                j += 1
        
        return max_platforms
    
    @staticmethod
    def minimum_number_of_arrows_to_burst_balloons(
        points: List[List[int]]) -> int:
        """
        Minimum arrows to burst balloons (overlapping intervals).
        
        Args:
            points: List of [xstart, xend] for each balloon
            
        Returns:
            Minimum arrows needed
        """
        if not points:
            return 0
        
        # Sort by end coordinate
        points.sort(key=lambda x: x[1])
        
        arrows = 1
        current_end = points[0][1]
        
        for start, end in points[1:]:
            if start > current_end:
                arrows += 1
                current_end = end
        
        return arrows
    
    @staticmethod
    def jump_game(nums: List[int]) -> bool:
        """
        Determine if you can reach the last index.
        
        Args:
            nums: List of maximum jump length at each position
            
        Returns:
            True if reachable
        """
        max_reach = 0
        
        for i, jump in enumerate(nums):
            if i > max_reach:
                return False
            max_reach = max(max_reach, i + jump)
        
        return True
    
    @staticmethod
    def jump_game_ii(nums: List[int]) -> int:
        """
        Minimum number of jumps to reach last index.
        
        Args:
            nums: List of maximum jump length at each position
            
        Returns:
            Minimum jumps
        """
        if len(nums) <= 1:
            return 0
        
        jumps = 0
        current_end = 0
        farthest = 0
        
        for i in range(len(nums) - 1):
            farthest = max(farthest, i + nums[i])
            
            if i == current_end:
                jumps += 1
                current_end = farthest
        
        return jumps
    
    @staticmethod
    def candy(ratings: List[int]) -> int:
        """
        Minimum candies to distribute with rating rules.
        
        Args:
            ratings: List of ratings
            
        Returns:
            Minimum total candies
        """
        n = len(ratings)
        candies = [1] * n
        
        # Left to right
        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                candies[i] = candies[i - 1] + 1
        
        # Right to left
        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                candies[i] = max(candies[i], candies[i + 1] + 1)
        
        return sum(candies)


def main() -> None:
    """Demonstrate greedy algorithms."""
    
    print("=== Greedy Algorithms Demo ===")
    
    # Activity selection
    print("\n--- Activity Selection ---")
    activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
    selected = GreedyPatterns.activity_selection(activities)
    print(f"Activities: {activities}")
    print(f"Selected: {selected}")
    print(f"Count: {len(selected)}")
    
    # Interval scheduling
    print("\n--- Interval Scheduling ---")
    intervals = [(1, 3), (2, 4), (3, 5), (0, 6), (5, 7), (8, 9), (5, 9)]
    print(f"Max intervals: {GreedyPatterns.interval_scheduling(intervals)}")
    
    # Minimum coins
    print("\n--- Minimum Coins ---")
    coins = [25, 10, 5, 1]
    amount = 67
    result = GreedyPatterns.minimum_coins(coins, amount)
    print(f"Coins: {coins}, Amount: {amount}")
    print(f"Used: {result} (total: {len(result)})")
    
    # Fractional knapsack
    print("\n--- Fractional Knapsack ---")
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50
    total_value, selected = GreedyPatterns.fractional_knapsack(weights, values, capacity)
    print(f"Total value: {total_value}")
    print(f"Selected: {selected}")
    
    # Job sequencing
    print("\n--- Job Sequencing ---")
    jobs = [(1, 2, 100), (2, 1, 19), (3, 2, 27), (4, 1, 25), (5, 3, 15)]
    scheduled = GreedyPatterns.job_sequencing(jobs)
    print(f"Scheduled jobs: {scheduled}")
    print(f"Total profit: {sum(job[2] for job in scheduled)}")
    
    # Huffman encoding
    print("\n--- Huffman Encoding ---")
    frequencies = {'a': 5, 'b': 9, 'c': 12, 'd': 13, 'e': 16, 'f': 45}
    codes = GreedyPatterns.huffman_encoding(frequencies)
    print(f"Frequencies: {frequencies}")
    print(f"Codes: {codes}")
    
    # Minimum platforms
    print("\n--- Minimum Platforms ---")
    arrivals = [900, 940, 950, 1100, 1500, 1800]
    departures = [910, 1200, 1120, 1130, 1900, 2000]
    print(f"Min platforms: {GreedyPatterns.minimum_platforms(arrivals, departures)}")
    
    # Burst balloons
    print("\n--- Burst Balloons ---")
    points = [[10, 16], [2, 8], [1, 6], [7, 12]]
    print(f"Min arrows: {GreedyPatterns.minimum_number_of_arrows_to_burst_balloons(points)}")
    
    # Jump game
    print("\n--- Jump Game ---")
    nums = [2, 3, 1, 1, 4]
    print(f"Can reach end: {GreedyPatterns.jump_game(nums)}")
    print(f"Min jumps: {GreedyPatterns.jump_game_ii(nums)}")
    
    # Candy distribution
    print("\n--- Candy Distribution ---")
    ratings = [1, 0, 2]
    print(f"Min candies: {GreedyPatterns.candy(ratings)}")


if __name__ == "__main__":
    main()

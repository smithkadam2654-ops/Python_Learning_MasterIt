"""
Greedy Algorithms - Implementation of classic greedy algorithms.
Features: Activity selection, Huffman coding, interval scheduling, and optimization.
"""

from typing import List, Tuple, Dict
from dataclasses import dataclass
import heapq
from collections import Counter


@dataclass
class Activity:
    """Activity for scheduling problems."""
    start: int
    end: int
    name: str = ""
    
    def __lt__(self, other: 'Activity') -> bool:
        """Compare activities by end time."""
        return self.end < other.end


def activity_selection(activities: List[Activity]) -> List[Activity]:
    """
    Select maximum number of non-overlapping activities.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Args:
        activities: List of activities with start and end times
        
    Returns:
        List of selected activities
    """
    if not activities:
        return []
    
    # Sort by end time
    sorted_activities = sorted(activities, key=lambda x: x.end)
    
    selected = [Activity(sorted_activities[0].start, sorted_activities[0].end)]
    last_end = selected[0].end
    
    for activity in sorted_activities[1:]:
        if activity.start >= last_end:
            selected.append(Activity(activity.start, activity.end))
            last_end = activity.end
    
    return selected


def fractional_knapsack(items: List[Tuple[str, int, int]], capacity: int) -> Tuple[float, List[Tuple[str, float]]]:
    """
    Solve fractional knapsack problem.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Args:
        items: List of (name, value, weight) tuples
        capacity: Maximum weight capacity
        
    Returns:
        Tuple of (max_value, list of (name, fraction_taken))
    """
    # Calculate value-to-weight ratio and sort
    items_with_ratio = [
        (name, value, weight, value / weight)
        for name, value, weight in items
    ]
    items_with_ratio.sort(key=lambda x: x[3], reverse=True)
    
    total_value = 0.0
    remaining_capacity = capacity
    taken_items = []
    
    for name, value, weight, ratio in items_with_ratio:
        if remaining_capacity <= 0:
            break
        
        if weight <= remaining_capacity:
            # Take whole item
            total_value += value
            remaining_capacity -= weight
            taken_items.append((name, 1.0))
        else:
            # Take fraction of item
            fraction = remaining_capacity / weight
            total_value += value * fraction
            taken_items.append((name, fraction))
            remaining_capacity = 0
    
    return total_value, taken_items


def huffman_encoding(text: str) -> Tuple[Dict[str, str], str]:
    """
    Perform Huffman encoding on text.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Args:
        text: Input text to encode
        
    Returns:
        Tuple of (encoding_dict, encoded_string)
    """
    if not text:
        return {}, ""
    
    # Count character frequencies
    freq = Counter(text)
    
    # Create priority queue
    heap = [[weight, [symbol, ""]] for symbol, weight in freq.items()]
    heapq.heapify(heap)
    
    # Build Huffman tree
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    
    # Extract encoding
    huffman_codes = {}
    for symbol, code in heap[0][1:]:
        huffman_codes[symbol] = code
    
    # Encode text
    encoded = ''.join(huffman_codes[char] for char in text)
    
    return huffman_codes, encoded


def minimum_coins(coins: List[int], amount: int) -> List[int]:
    """
    Find minimum number of coins to make amount (greedy approach).
    Note: Only works for canonical coin systems.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Args:
        coins: Available coin denominations
        amount: Target amount
        
    Returns:
        List of coins used
    """
    if amount <= 0:
        return []
    
    # Sort coins in descending order
    coins.sort(reverse=True)
    
    result = []
    remaining = amount
    
    for coin in coins:
        while remaining >= coin:
            result.append(coin)
            remaining -= coin
    
    if remaining != 0:
        return []  # Cannot make exact amount
    
    return result


def job_sequencing(jobs: List[Tuple[str, int, int]]) -> List[Tuple[str, int]]:
    """
    Schedule jobs to maximize profit (each job takes 1 unit of time).
    
    Time Complexity: O(n²)
    Space Complexity: O(n)
    
    Args:
        jobs: List of (name, deadline, profit) tuples
        
    Returns:
        List of scheduled jobs with their profits
    """
    if not jobs:
        return []
    
    # Sort by profit in descending order
    jobs_sorted = sorted(jobs, key=lambda x: x[2], reverse=True)
    
    # Find maximum deadline
    max_deadline = max(job[1] for job in jobs_sorted)
    
    # Track available slots
    slots = [False] * (max_deadline + 1)
    result = []
    total_profit = 0
    
    for job in jobs_sorted:
        name, deadline, profit = job
        
        # Find latest available slot
        for slot in range(deadline, 0, -1):
            if not slots[slot]:
                slots[slot] = True
                result.append((name, profit))
                total_profit += profit
                break
    
    return result


def interval_partitioning(intervals: List[Tuple[int, int]]) -> int:
    """
    Find minimum number of classrooms needed for all intervals.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Args:
        intervals: List of (start, end) tuples
        
    Returns:
        Minimum number of classrooms
    """
    if not intervals:
        return 0
    
    # Separate start and end times
    starts = sorted(interval[0] for interval in intervals)
    ends = sorted(interval[1] for interval in intervals)
    
    rooms = 0
    end_ptr = 0
    
    for start in starts:
        if start < ends[end_ptr]:
            rooms += 1
        else:
            end_ptr += 1
    
    return rooms


def jump_game(nums: List[int]) -> int:
    """
    Find minimum number of jumps to reach end of array.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Args:
        nums: Array where each element represents max jump length
        
    Returns:
        Minimum number of jumps, or -1 if impossible
    """
    if not nums or len(nums) == 1:
        return 0
    
    if nums[0] == 0:
        return -1
    
    jumps = 1
    max_reach = nums[0]
    steps = nums[0]
    
    for i in range(1, len(nums)):
        if i == len(nums) - 1:
            return jumps
        
        max_reach = max(max_reach, i + nums[i])
        steps -= 1
        
        if steps == 0:
            jumps += 1
            
            if i >= max_reach:
                return -1
            
            steps = max_reach - i
    
    return -1


def gas_station(gas: List[int], cost: List[int]) -> int:
    """
    Find starting gas station to complete circuit.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Args:
        gas: Amount of gas at each station
        cost: Cost to travel to next station
        
    Returns:
        Starting station index, or -1 if impossible
    """
    if len(gas) != len(cost):
        return -1
    
    total_gas = 0
    total_cost = 0
    current_gas = 0
    start = 0
    
    for i in range(len(gas)):
        total_gas += gas[i]
        total_cost += cost[i]
        current_gas += gas[i] - cost[i]
        
        if current_gas < 0:
            start = i + 1
            current_gas = 0
    
    if total_gas < total_cost:
        return -1
    
    return start


def partition_labels(s: str) -> List[int]:
    """
    Partition string into as many parts as possible.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Args:
        s: Input string
        
    Returns:
        List of partition sizes
    """
    if not s:
        return []
    
    # Last occurrence of each character
    last_occurrence = {char: i for i, char in enumerate(s)}
    
    result = []
    start = 0
    end = 0
    
    for i, char in enumerate(s):
        end = max(end, last_occurrence[char])
        
        if i == end:
            result.append(end - start + 1)
            start = i + 1
    
    return result


def main() -> None:
    """Demonstrate greedy algorithms."""
    
    print("=== Activity Selection ===")
    activities = [
        Activity(1, 4, "A1"),
        Activity(3, 5, "A2"),
        Activity(0, 6, "A3"),
        Activity(5, 7, "A4"),
        Activity(3, 9, "A5"),
        Activity(5, 9, "A6"),
        Activity(6, 10, "A7"),
        Activity(8, 11, "A8"),
        Activity(8, 12, "A9"),
        Activity(2, 14, "A10"),
        Activity(12, 16, "A11"),
    ]
    
    selected = activity_selection(activities)
    print(f"Selected {len(selected)} activities out of {len(activities)}")
    for activity in selected:
        print(f"  ({activity.start}, {activity.end})")
    
    print("\n=== Fractional Knapsack ===")
    items = [
        ("Item1", 60, 10),
        ("Item2", 100, 20),
        ("Item3", 120, 30),
    ]
    capacity = 50
    max_value, taken = fractional_knapsack(items, capacity)
    print(f"Max value: {max_value}")
    print(f"Items taken: {taken}")
    
    print("\n=== Huffman Encoding ===")
    text = "hello world"
    codes, encoded = huffman_encoding(text)
    print(f"Original: {text}")
    print(f"Codes: {codes}")
    print(f"Encoded: {encoded}")
    print(f"Compression ratio: {len(encoded)}/{len(text) * 8} = {len(encoded) / (len(text) * 8):.2f}")
    
    print("\n=== Minimum Coins ===")
    coins = [1, 5, 10, 25]
    amount = 67
    coin_list = minimum_coins(coins, amount)
    print(f"Coins for {amount}: {coin_list}")
    print(f"Number of coins: {len(coin_list)}")
    
    print("\n=== Job Sequencing ===")
    jobs = [
        ("J1", 2, 100),
        ("J2", 1, 19),
        ("J3", 2, 27),
        ("J4", 1, 25),
        ("J5", 3, 15),
    ]
    scheduled = job_sequencing(jobs)
    print(f"Scheduled jobs: {scheduled}")
    print(f"Total profit: {sum(profit for _, profit in scheduled)}")
    
    print("\n=== Interval Partitioning ===")
    intervals = [(30, 75), (0, 50), (60, 150)]
    rooms = interval_partitioning(intervals)
    print(f"Minimum classrooms needed: {rooms}")
    
    print("\n=== Jump Game ===")
    nums = [2, 3, 1, 1, 4]
    jumps = jump_game(nums)
    print(f"Array: {nums}")
    print(f"Minimum jumps: {jumps}")
    
    print("\n=== Gas Station ===")
    gas = [1, 2, 3, 4, 5]
    cost = [3, 4, 5, 1, 2]
    start = gas_station(gas, cost)
    print(f"Gas: {gas}")
    print(f"Cost: {cost}")
    print(f"Starting station: {start}")
    
    print("\n=== Partition Labels ===")
    s = "ababcbacadefegdehijhklij"
    partitions = partition_labels(s)
    print(f"String: {s}")
    print(f"Partition sizes: {partitions}")


if __name__ == "__main__":
    main()

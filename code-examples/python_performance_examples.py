#!/usr/bin/env python3
"""
Performance Optimization Examples for Python
Demonstrates inefficient vs efficient code patterns with timing comparisons
"""

import time
from functools import lru_cache
from typing import List, Set


def time_function(func):
    """Decorator to measure function execution time"""
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__}: {(end - start) * 1000:.4f} ms")
        return result
    return wrapper


# ============================================================================
# Example 1: String Concatenation
# ============================================================================

@time_function
def inefficient_string_concat(n: int = 10000) -> str:
    """Inefficient: O(n²) complexity due to string immutability"""
    result = ""
    for i in range(n):
        result += str(i) + ","
    return result


@time_function
def efficient_string_concat(n: int = 10000) -> str:
    """Efficient: O(n) complexity using join"""
    return ",".join(str(i) for i in range(n))


# ============================================================================
# Example 2: Membership Testing
# ============================================================================

@time_function
def inefficient_membership_test(data: List[int], lookups: int = 10000) -> int:
    """Inefficient: O(n) lookup in list for each search"""
    allowed = list(range(1000))
    count = 0
    for i in range(lookups):
        if i % 10 in allowed:
            count += 1
    return count


@time_function
def efficient_membership_test(data: Set[int], lookups: int = 10000) -> int:
    """Efficient: O(1) lookup in set for each search"""
    allowed = set(range(1000))
    count = 0
    for i in range(lookups):
        if i % 10 in allowed:
            count += 1
    return count


# ============================================================================
# Example 3: List Comprehension vs Loop
# ============================================================================

@time_function
def inefficient_list_building(n: int = 100000) -> List[int]:
    """Inefficient: Appending to list in loop"""
    result = []
    for i in range(n):
        if i % 2 == 0:
            result.append(i * i)
    return result


@time_function
def efficient_list_building(n: int = 100000) -> List[int]:
    """Efficient: List comprehension"""
    return [i * i for i in range(n) if i % 2 == 0]


# ============================================================================
# Example 4: Caching Expensive Computations
# ============================================================================

def fibonacci_no_cache(n: int) -> int:
    """Inefficient: Exponential time complexity O(2^n)"""
    if n < 2:
        return n
    return fibonacci_no_cache(n - 1) + fibonacci_no_cache(n - 2)


@lru_cache(maxsize=None)
def fibonacci_with_cache(n: int) -> int:
    """Efficient: O(n) with memoization"""
    if n < 2:
        return n
    return fibonacci_with_cache(n - 1) + fibonacci_with_cache(n - 2)


@time_function
def test_fibonacci_no_cache():
    """Time fibonacci without cache"""
    return fibonacci_no_cache(30)


@time_function
def test_fibonacci_with_cache():
    """Time fibonacci with cache"""
    return fibonacci_with_cache(30)


# ============================================================================
# Example 5: Avoiding Unnecessary Copies
# ============================================================================

@time_function
def inefficient_slice_copy(data: List[int]) -> int:
    """Inefficient: Creates copy of list slice"""
    total = 0
    for i in range(0, len(data), 100):
        chunk = data[i:i+100]  # Creates a copy
        total += sum(chunk)
    return total


@time_function
def efficient_slice_iteration(data: List[int]) -> int:
    """Efficient: Iterate without creating copies"""
    total = 0
    for i in range(0, len(data), 100):
        chunk_sum = sum(data[j] for j in range(i, min(i+100, len(data))))
        total += chunk_sum
    return total


# ============================================================================
# Example 6: Generator vs List
# ============================================================================

@time_function
def inefficient_process_large_data() -> int:
    """Inefficient: Creates entire list in memory"""
    data = [i * i for i in range(1000000)]
    return sum(x for x in data if x % 2 == 0)


@time_function
def efficient_process_large_data() -> int:
    """Efficient: Uses generator to process on-the-fly"""
    data = (i * i for i in range(1000000))
    return sum(x for x in data if x % 2 == 0)


# ============================================================================
# Example 7: Dictionary Get vs Try-Except
# ============================================================================

@time_function
def inefficient_dict_access(lookups: int = 100000):
    """Using try-except for expected cases"""
    data = {i: i * 2 for i in range(1000)}
    count = 0
    for i in range(lookups):
        try:
            count += data[i % 1000]
        except KeyError:
            count += 0


@time_function
def efficient_dict_access(lookups: int = 100000):
    """Using get() method with default"""
    data = {i: i * 2 for i in range(1000)}
    count = 0
    for i in range(lookups):
        count += data.get(i % 1000, 0)


# ============================================================================
# Main Benchmark Runner
# ============================================================================

def run_benchmarks():
    """Run all performance comparison benchmarks"""
    print("=" * 70)
    print("Python Performance Optimization Examples")
    print("=" * 70)
    
    print("\n1. String Concatenation (10,000 elements)")
    print("-" * 70)
    inefficient_string_concat()
    efficient_string_concat()
    
    print("\n2. Membership Testing (10,000 lookups)")
    print("-" * 70)
    inefficient_membership_test([])
    efficient_membership_test(set())
    
    print("\n3. List Building (100,000 elements)")
    print("-" * 70)
    inefficient_list_building()
    efficient_list_building()
    
    print("\n4. Fibonacci Calculation (n=30)")
    print("-" * 70)
    test_fibonacci_no_cache()
    fibonacci_with_cache.cache_clear()  # Clear cache for fair comparison
    test_fibonacci_with_cache()
    
    print("\n5. Large List Processing (1,000,000 elements)")
    print("-" * 70)
    large_data = list(range(100000))
    inefficient_slice_copy(large_data)
    efficient_slice_iteration(large_data)
    
    print("\n6. Generator vs List (1,000,000 elements)")
    print("-" * 70)
    inefficient_process_large_data()
    efficient_process_large_data()
    
    print("\n7. Dictionary Access (100,000 lookups)")
    print("-" * 70)
    inefficient_dict_access()
    efficient_dict_access()
    
    print("\n" + "=" * 70)
    print("Benchmark Complete!")
    print("=" * 70)


if __name__ == "__main__":
    run_benchmarks()

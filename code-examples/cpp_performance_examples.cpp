// Performance Optimization Examples for C++
// Compile with: g++ -std=c++17 -O2 -o cpp_performance_examples cpp_performance_examples.cpp
// Run with: ./cpp_performance_examples

#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <algorithm>
#include <unordered_set>
#include <set>
#include <memory>

using namespace std;
using namespace std::chrono;

// ============================================================================
// Timing Utility
// ============================================================================

template<typename Func>
void timeFunction(const string& name, Func func) {
    auto start = high_resolution_clock::now();
    func();
    auto end = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(end - start);
    cout << name << ": " << duration.count() / 1000.0 << " ms" << endl;
}

// ============================================================================
// Example 1: Pass by Value vs Pass by Reference
// ============================================================================

int sumByValue(vector<int> vec) {
    // Inefficient: Copies entire vector
    int sum = 0;
    for (int val : vec) {
        sum += val;
    }
    return sum;
}

int sumByReference(const vector<int>& vec) {
    // Efficient: No copy, uses reference
    int sum = 0;
    for (int val : vec) {
        sum += val;
    }
    return sum;
}

void testPassByReference() {
    vector<int> data(1000000);
    for (int i = 0; i < 1000000; i++) {
        data[i] = i;
    }
    
    cout << "\n1. Pass by Value vs Reference (1M elements)" << endl;
    cout << string(70, '-') << endl;
    
    timeFunction("Pass by Value (inefficient)", [&]() {
        volatile int result = sumByValue(data);
    });
    
    timeFunction("Pass by Reference (efficient)", [&]() {
        volatile int result = sumByReference(data);
    });
}

// ============================================================================
// Example 2: String Concatenation
// ============================================================================

void testStringConcatenation() {
    cout << "\n2. String Concatenation (10,000 elements)" << endl;
    cout << string(70, '-') << endl;
    
    timeFunction("Using += operator (inefficient)", []() {
        string result;
        for (int i = 0; i < 10000; i++) {
            result += to_string(i) + ",";
        }
    });
    
    timeFunction("Using reserve + += (efficient)", []() {
        string result;
        result.reserve(60000);  // Pre-allocate memory
        for (int i = 0; i < 10000; i++) {
            result += to_string(i) + ",";
        }
    });
}

// ============================================================================
// Example 3: Vector Reserve
// ============================================================================

void testVectorReserve() {
    cout << "\n3. Vector Reserve (100,000 elements)" << endl;
    cout << string(70, '-') << endl;
    
    timeFunction("Without reserve (inefficient)", []() {
        vector<int> vec;
        for (int i = 0; i < 100000; i++) {
            vec.push_back(i);  // May reallocate multiple times
        }
    });
    
    timeFunction("With reserve (efficient)", []() {
        vector<int> vec;
        vec.reserve(100000);  // Pre-allocate memory
        for (int i = 0; i < 100000; i++) {
            vec.push_back(i);  // No reallocation
        }
    });
}

// ============================================================================
// Example 4: emplace_back vs push_back
// ============================================================================

struct Point {
    int x, y, z;
    Point(int x, int y, int z) : x(x), y(y), z(z) {}
};

void testEmplaceBack() {
    cout << "\n4. emplace_back vs push_back (100,000 elements)" << endl;
    cout << string(70, '-') << endl;
    
    timeFunction("Using push_back (inefficient)", []() {
        vector<Point> points;
        points.reserve(100000);
        for (int i = 0; i < 100000; i++) {
            points.push_back(Point(i, i*2, i*3));  // Creates temp object
        }
    });
    
    timeFunction("Using emplace_back (efficient)", []() {
        vector<Point> points;
        points.reserve(100000);
        for (int i = 0; i < 100000; i++) {
            points.emplace_back(i, i*2, i*3);  // Constructs in-place
        }
    });
}

// ============================================================================
// Example 5: Set vs Unordered Set for Lookups
// ============================================================================

void testSetLookup() {
    cout << "\n5. Set vs Unordered Set (100,000 lookups)" << endl;
    cout << string(70, '-') << endl;
    
    set<int> orderedSet;
    unordered_set<int> unorderedSet;
    
    for (int i = 0; i < 10000; i++) {
        orderedSet.insert(i);
        unorderedSet.insert(i);
    }
    
    timeFunction("std::set lookup - O(log n)", [&]() {
        int count = 0;
        for (int i = 0; i < 100000; i++) {
            if (orderedSet.find(i % 10000) != orderedSet.end()) {
                count++;
            }
        }
    });
    
    timeFunction("std::unordered_set lookup - O(1)", [&]() {
        int count = 0;
        for (int i = 0; i < 100000; i++) {
            if (unorderedSet.find(i % 10000) != unorderedSet.end()) {
                count++;
            }
        }
    });
}

// ============================================================================
// Example 6: Cache Vector Size
// ============================================================================

void testCacheSize() {
    vector<int> data(1000000);
    for (int i = 0; i < 1000000; i++) {
        data[i] = i;
    }
    
    cout << "\n6. Caching Vector Size (1M iterations)" << endl;
    cout << string(70, '-') << endl;
    
    timeFunction("Calling size() in loop (inefficient)", [&]() {
        long long sum = 0;
        for (size_t i = 0; i < data.size(); i++) {  // size() called each iteration
            sum += data[i];
        }
    });
    
    timeFunction("Caching size (efficient)", [&]() {
        long long sum = 0;
        const size_t size = data.size();  // Cache size
        for (size_t i = 0; i < size; i++) {
            sum += data[i];
        }
    });
    
    timeFunction("Range-based for loop (most efficient)", [&]() {
        long long sum = 0;
        for (int val : data) {
            sum += val;
        }
    });
}

// ============================================================================
// Example 7: Move Semantics
// ============================================================================

vector<int> createLargeVector() {
    vector<int> vec(1000000);
    for (int i = 0; i < 1000000; i++) {
        vec[i] = i;
    }
    return vec;  // Return by value - move semantics
}

void testMoveSemantics() {
    cout << "\n7. Copy vs Move Semantics" << endl;
    cout << string(70, '-') << endl;
    
    timeFunction("Copy constructor (if used)", []() {
        vector<int> original(1000000, 42);
        vector<int> copy = original;  // Copies all elements
    });
    
    timeFunction("Move constructor (efficient)", []() {
        vector<int> original(1000000, 42);
        vector<int> moved = std::move(original);  // Just moves pointer
    });
    
    timeFunction("Return value optimization", []() {
        vector<int> result = createLargeVector();  // Optimized by compiler
    });
}

// ============================================================================
// Main
// ============================================================================

int main() {
    cout << string(70, '=') << endl;
    cout << "C++ Performance Optimization Examples" << endl;
    cout << string(70, '=') << endl;
    
    testPassByReference();
    testStringConcatenation();
    testVectorReserve();
    testEmplaceBack();
    testSetLookup();
    testCacheSize();
    testMoveSemantics();
    
    cout << "\n" << string(70, '=') << endl;
    cout << "Benchmark Complete!" << endl;
    cout << string(70, '=') << endl;
    
    return 0;
}

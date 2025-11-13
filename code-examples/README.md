# Performance Optimization Code Examples

This directory contains practical, runnable code examples demonstrating performance optimization techniques across different programming languages.

## Contents

- **python_performance_examples.py** - Python optimization patterns with benchmarks
- **cpp_performance_examples.cpp** - C++ optimization patterns with benchmarks  
- **cv_performance_examples.py** - Computer Vision & AI model optimization examples

## Running the Examples

### Python Examples

```bash
python3 python_performance_examples.py
```

**Requirements**: Python 3.6+

Expected output shows timing comparisons between inefficient and efficient implementations:
- String concatenation: O(n²) vs O(n)
- Membership testing: List vs Set lookups
- List building: Loops vs comprehensions
- Caching: Fibonacci with and without memoization
- Generators vs lists for memory efficiency
- Dictionary access patterns

### C++ Examples

```bash
# Compile with optimizations
g++ -std=c++17 -O2 -o cpp_performance_examples cpp_performance_examples.cpp

# Run
./cpp_performance_examples
```

**Requirements**: C++17 compatible compiler (g++, clang++)

Demonstrates:
- Pass by value vs reference
- String concatenation optimization
- Vector reserve and emplace_back
- Set vs unordered_set for lookups
- Caching vector size
- Move semantics

### Computer Vision Examples

```bash
python3 cv_performance_examples.py
```

**Requirements**:
```bash
pip install opencv-python numpy
# Optional for YOLO examples:
pip install ultralytics torch
```

Covers:
- Image resizing and preprocessing optimization
- Batch processing for ML models
- Frame skipping for real-time video
- Model loading and caching
- Multi-threading for video processing

## Key Takeaways

### Python
- Use `join()` for string concatenation
- Use sets for membership testing
- Prefer list comprehensions over loops
- Cache expensive computations with `@lru_cache`
- Use generators for large datasets

### C++
- Pass large objects by const reference
- Use `reserve()` for vectors when size is known
- Prefer `emplace_back()` over `push_back()`
- Use move semantics for large objects
- Choose appropriate container (unordered_set for O(1) lookup)

### Computer Vision / AI
- Load models once, reuse for multiple inferences
- Resize images to model's expected input size
- Process frames in batches when possible
- Use GPU acceleration when available
- Skip frames in video for real-time performance

## Learning Resources

See the main [PERFORMANCE_OPTIMIZATION_GUIDE.md](../PERFORMANCE_OPTIMIZATION_GUIDE.md) for comprehensive documentation.

## Contributing

Feel free to add more examples! Focus on:
- Real-world patterns
- Measurable performance differences
- Clear before/after comparisons
- Language-specific idioms

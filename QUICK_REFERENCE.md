# Quick Performance Optimization Reference

This is a quick-reference cheat sheet for common performance issues and solutions. For detailed explanations, see [PERFORMANCE_OPTIMIZATION_GUIDE.md](PERFORMANCE_OPTIMIZATION_GUIDE.md).

## Python - Common Issues

| ❌ Inefficient | ✅ Efficient | Why |
|---------------|-------------|-----|
| `result = ""; for x in list: result += str(x)` | `result = "".join(str(x) for x in list)` | O(n²) → O(n) |
| `if x in [1,2,3,4,5]` | `if x in {1,2,3,4,5}` | O(n) → O(1) lookup |
| `result = []; for x in range(n): result.append(x*2)` | `result = [x*2 for x in range(n)]` | Faster, more readable |
| Load model in loop | Load model once, reuse | Avoid repeated I/O |
| `def fib(n): return fib(n-1)+fib(n-2)` | `@lru_cache` on function | O(2^n) → O(n) |

## C++ - Common Issues

| ❌ Inefficient | ✅ Efficient | Why |
|---------------|-------------|-----|
| `void f(vector<int> v)` | `void f(const vector<int>& v)` | Avoid copy |
| `vec.push_back(Point(x,y))` | `vec.emplace_back(x,y)` | No temporary object |
| Loop without `reserve()` | `vec.reserve(size)` before loop | Avoid reallocations |
| `std::endl` in loops | `'\n'` | Avoid buffer flush |
| `for(int i=0; i<v.size(); i++)` | `for(const auto& x : v)` | Cleaner, may be faster |

## Algorithm Choices

| Operation | Bad Choice | Good Choice | Complexity |
|-----------|-----------|-------------|-----------|
| Find duplicates | Nested loops | Hash set | O(n²) → O(n) |
| Sorted search | Linear scan | Binary search | O(n) → O(log n) |
| Frequency count | Loop per element | Hash map | O(n²) → O(n) |
| Range sum | Loop each time | Prefix sum array | O(n) → O(1) per query |

## AI/Computer Vision - Best Practices

```python
# ❌ DON'T: Load model repeatedly
for image in images:
    model = YOLO('model.pt')  # Very slow!
    result = model(image)

# ✅ DO: Load once, reuse
model = YOLO('model.pt')  # Load once
for image in images:
    result = model(image)

# ❌ DON'T: Process every video frame
for frame in video:
    result = detect(frame)  # 30 FPS = expensive

# ✅ DO: Skip frames
for i, frame in enumerate(video):
    if i % 5 == 0:  # Process every 5th frame
        result = detect(frame)

# ❌ DON'T: Use full resolution
result = model(image_1920x1080)

# ✅ DO: Resize to model input size
resized = cv2.resize(image, (640, 640))
result = model(resized)
```

## Quick Profiling Commands

```bash
# Python
python -m cProfile -s cumulative script.py
python -m timeit "your_code_here"

# C++
g++ -pg program.cpp && ./a.out && gprof a.out

# System level
time ./program
perf stat ./program
```

## Memory vs Speed Tradeoffs

| Technique | Memory | Speed | When to Use |
|-----------|--------|-------|-------------|
| Caching/Memoization | ↑ More | ↑ Faster | Repeated computations |
| Generators | ↓ Less | ↓ Slower | Large datasets |
| Batch processing | ↑ More | ↑ Faster | ML/GPU operations |
| Streaming | ↓ Less | ↓ Slower | Can't fit in RAM |

## Decision Tree: Should I Optimize?

```
Is the code correct? 
  NO → Fix bugs first
  YES ↓
  
Have you profiled it?
  NO → Profile first! Don't guess
  YES ↓
  
Is it a bottleneck?
  NO → Don't optimize (yet)
  YES ↓
  
Can you improve the algorithm? (O(n²) → O(n log n))
  YES → Do this FIRST
  NO ↓
  
Can you cache/memoize?
  YES → Try this second
  NO ↓
  
Can you use better data structures?
  YES → Try this third
  NO ↓
  
Now try micro-optimizations
```

## Remember

1. **Measure first** - Profile before optimizing
2. **Algorithm > Implementation** - O(n) beats optimized O(n²)
3. **Readable > Fast** - Unless it's a proven bottleneck
4. **80/20 Rule** - 80% of time spent in 20% of code
5. **Test after** - Ensure optimizations don't break functionality

---

For more details and examples, see:
- [Full Performance Guide](PERFORMANCE_OPTIMIZATION_GUIDE.md)
- [Runnable Examples](code-examples/)

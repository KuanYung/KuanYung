# Performance Optimization Guide

This guide provides practical advice for identifying and improving slow or inefficient code across various programming languages and scenarios.

## Table of Contents
- [General Principles](#general-principles)
- [Python Optimization](#python-optimization)
- [C/C++ Optimization](#c-c-optimization)
- [Java Optimization](#java-optimization)
- [Algorithm Optimization](#algorithm-optimization)
- [Computer Vision & AI Model Optimization](#computer-vision--ai-model-optimization)
- [Profiling and Benchmarking Tools](#profiling-and-benchmarking-tools)

---

## General Principles

### 1. Measure Before Optimizing
- **Always profile first** - Don't guess where bottlenecks are
- Use appropriate benchmarking tools for your language
- Focus on hot paths (code that runs frequently)

### 2. Big-O Complexity Matters
- Algorithm choice has more impact than micro-optimizations
- O(n²) → O(n log n) is better than optimizing O(n²) code
- Consider space-time tradeoffs

### 3. Premature Optimization
- Write clear, correct code first
- Optimize only when measurements show it's necessary
- Maintain code readability

---

## Python Optimization

### Common Performance Issues

#### ❌ Inefficient: Repeatedly appending to strings
```python
result = ""
for item in large_list:
    result += str(item) + ","  # Creates new string each iteration - O(n²)
```

#### ✅ Efficient: Use list and join
```python
result = ",".join(str(item) for item in large_list)  # O(n)
```

#### ❌ Inefficient: Searching in lists
```python
allowed_values = [1, 2, 3, 4, 5, ...]  # List
if value in allowed_values:  # O(n) lookup
    process(value)
```

#### ✅ Efficient: Use sets for membership testing
```python
allowed_values = {1, 2, 3, 4, 5, ...}  # Set
if value in allowed_values:  # O(1) lookup
    process(value)
```

#### ❌ Inefficient: Loop with index
```python
for i in range(len(items)):
    process(items[i])
```

#### ✅ Efficient: Direct iteration
```python
for item in items:
    process(item)
```

### Python-Specific Tips
- Use list comprehensions instead of loops when building lists
- Leverage built-in functions (map, filter, sum) - they're optimized in C
- Use `itertools` for efficient iteration patterns
- Consider NumPy for numerical operations
- Use `__slots__` for classes with many instances
- Cache expensive function results with `@lru_cache`

---

## C/C++ Optimization

### Common Performance Issues

#### ❌ Inefficient: Passing large objects by value
```cpp
void process(std::vector<int> data) {  // Copies entire vector
    // ...
}
```

#### ✅ Efficient: Pass by const reference
```cpp
void process(const std::vector<int>& data) {  // No copy
    // ...
}
```

#### ❌ Inefficient: Unnecessary copies
```cpp
std::vector<int> vec = getData();
for (int i = 0; i < vec.size(); i++) {  // size() called every iteration
    std::cout << vec[i] << std::endl;  // std::endl flushes buffer
}
```

#### ✅ Efficient: Cache size and use '\n'
```cpp
std::vector<int> vec = getData();
const size_t size = vec.size();
for (size_t i = 0; i < size; i++) {
    std::cout << vec[i] << '\n';  // Faster than std::endl
}
```

### C/C++ Specific Tips
- Enable compiler optimizations (-O2, -O3)
- Use move semantics for large objects
- Prefer `reserve()` for vectors when size is known
- Use `emplace_back()` instead of `push_back()` for in-place construction
- Consider memory alignment and cache locality
- Use constexpr for compile-time computations

---

## Java Optimization

### Common Performance Issues

#### ❌ Inefficient: String concatenation in loops
```java
String result = "";
for (int i = 0; i < 1000; i++) {
    result += i + ",";  // Creates new String each iteration
}
```

#### ✅ Efficient: Use StringBuilder
```java
StringBuilder result = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    result.append(i).append(",");
}
String finalResult = result.toString();
```

#### ❌ Inefficient: Autoboxing in loops
```java
List<Integer> numbers = new ArrayList<>();
for (int i = 0; i < 1000000; i++) {
    numbers.add(i);  // Autoboxing: int → Integer
}
```

#### ✅ Efficient: Use primitive arrays when possible
```java
int[] numbers = new int[1000000];
for (int i = 0; i < 1000000; i++) {
    numbers[i] = i;  // No boxing overhead
}
```

### Java-Specific Tips
- Use appropriate collection classes (HashMap vs TreeMap)
- Avoid premature object creation
- Use try-with-resources to ensure proper resource cleanup
- Consider parallel streams for CPU-intensive operations
- Profile with JProfiler or VisualVM
- Be aware of garbage collection impact

---

## Algorithm Optimization

### Common Algorithmic Improvements

#### Example: Finding duplicates

❌ **O(n²) - Nested loops**
```python
def has_duplicates(arr):
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j]:
                return True
    return False
```

✅ **O(n) - Using a set**
```python
def has_duplicates(arr):
    seen = set()
    for item in arr:
        if item in seen:
            return True
        seen.add(item)
    return False
```

### Data Structure Selection

| Operation | Best Data Structure | Time Complexity |
|-----------|-------------------|-----------------|
| Fast lookup | Hash table/dict/set | O(1) average |
| Sorted data | Binary search tree | O(log n) |
| LIFO access | Stack | O(1) |
| FIFO access | Queue | O(1) |
| Priority queue | Heap | O(log n) |

---

## Computer Vision & AI Model Optimization

### YOLO Model Optimization (Relevant to your AI projects)

#### Model-Level Optimizations
```python
# ❌ Inefficient: Loading model every time
def detect_objects(image):
    model = YOLO('yolov8n.pt')  # Loads model each call
    results = model(image)
    return results

# ✅ Efficient: Load model once
class ObjectDetector:
    def __init__(self):
        self.model = YOLO('yolov8n.pt')  # Load once
    
    def detect(self, image):
        return self.model(image)
```

#### Input Processing Optimization
```python
# ❌ Inefficient: Processing full resolution
def process_frame(frame):
    results = model(frame)  # 1920x1080 or higher
    return results

# ✅ Efficient: Resize input appropriately
def process_frame(frame):
    # YOLO models typically use 640x640 input
    frame_resized = cv2.resize(frame, (640, 640))
    results = model(frame_resized)
    return results
```

#### Batch Processing
```python
# ❌ Inefficient: Process images one by one
for image in images:
    result = model(image)
    results.append(result)

# ✅ Efficient: Batch processing
results = model(images)  # Process multiple images together
```

### Performance Tips for AI/CV Projects
- **Use GPU when available**: torch.cuda.is_available()
- **Reduce model size**: Use lighter models (YOLOv8n vs YOLOv8x)
- **Quantization**: Convert FP32 to INT8 for faster inference
- **TensorRT optimization**: For NVIDIA GPUs
- **Frame skipping**: Process every Nth frame in video
- **Multi-threading**: Separate frame capture and processing threads
- **Use OpenCV optimizations**: cv2.setNumThreads()

---

## Profiling and Benchmarking Tools

### Python
```python
# cProfile - Built-in profiler
python -m cProfile -s cumulative script.py

# line_profiler - Line-by-line profiling
@profile
def slow_function():
    pass

# memory_profiler - Memory usage
@profile
def memory_intensive():
    pass

# timeit - Micro-benchmarking
import timeit
timeit.timeit('sum(range(100))', number=10000)
```

### C/C++
- **gprof**: GNU profiler
- **Valgrind**: Memory profiling and leak detection
- **perf**: Linux performance analysis
- **Google Benchmark**: Micro-benchmarking library

### Java
- **JProfiler**: Commercial profiler
- **VisualVM**: Free profiling tool
- **Java Flight Recorder**: Built-in profiling

---

## Quick Checklist

When reviewing code for performance:

- [ ] Are you using the right algorithm? (Check Big-O complexity)
- [ ] Are you using appropriate data structures?
- [ ] Are there unnecessary loops or nested loops?
- [ ] Are you doing repeated work that could be cached?
- [ ] Are you creating unnecessary objects or copies?
- [ ] Are you doing I/O efficiently (buffering, batching)?
- [ ] Have you profiled to find actual bottlenecks?
- [ ] Are you processing data in appropriate batch sizes?
- [ ] For AI models: Are you using GPU acceleration?
- [ ] For AI models: Is your input size optimal?

---

## Resources

### Books
- "High Performance Python" by Micha Gorelick & Ian Ozsvald
- "Effective C++" by Scott Meyers
- "Java Performance" by Scott Oaks

### Online Tools
- [Python Performance Tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [Java Performance Tuning Guide](https://docs.oracle.com/javase/8/docs/technotes/guides/vm/gctuning/)

---

## Contributing

Have performance tips to add? Feel free to contribute! Focus on:
- Real-world examples
- Measurable improvements
- Language-specific optimizations
- AI/ML and computer vision optimizations

---

*Last updated: 2025*

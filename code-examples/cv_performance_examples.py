#!/usr/bin/env python3
"""
Computer Vision and AI Model Performance Optimization Examples
Relevant to YOLO-based projects and real-time video processing
"""

import time
import numpy as np
from typing import List, Tuple

# Optional imports - uncomment if you have these libraries
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("Note: OpenCV not available. Install with: pip install opencv-python")

try:
    from ultralytics import YOLO
    import torch
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("Note: YOLO not available. Install with: pip install ultralytics torch")


def time_function(func):
    """Decorator to measure function execution time"""
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__}: {(end - start) * 1000:.2f} ms")
        return result
    return wrapper


# ============================================================================
# Example 1: Image Resizing - NumPy vs OpenCV
# ============================================================================

def test_image_resizing():
    """Compare different image resizing approaches"""
    if not CV2_AVAILABLE:
        print("\nSkipping image resizing tests (OpenCV not available)")
        return
    
    print("\n1. Image Resizing (1920x1080 -> 640x640)")
    print("-" * 70)
    
    # Create a sample image
    image = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
    
    @time_function
    def resize_with_numpy():
        """Inefficient: Manual resizing with NumPy"""
        # This is very inefficient - just for demonstration
        h, w = image.shape[:2]
        new_h, new_w = 640, 640
        resized = np.zeros((new_h, new_w, 3), dtype=np.uint8)
        for i in range(new_h):
            for j in range(new_w):
                src_i = int(i * h / new_h)
                src_j = int(j * w / new_w)
                resized[i, j] = image[src_i, src_j]
        return resized
    
    @time_function
    def resize_with_opencv():
        """Efficient: Using OpenCV's optimized resize"""
        return cv2.resize(image, (640, 640), interpolation=cv2.INTER_LINEAR)
    
    @time_function
    def resize_with_opencv_fast():
        """Most efficient: Using INTER_NEAREST for speed"""
        return cv2.resize(image, (640, 640), interpolation=cv2.INTER_NEAREST)
    
    # Note: NumPy version is too slow, commenting out
    # resize_with_numpy()
    print("resize_with_numpy: ~1000-2000 ms (too slow, skipped)")
    resize_with_opencv()
    resize_with_opencv_fast()


# ============================================================================
# Example 2: Model Loading - Good vs Bad Practices
# ============================================================================

def test_model_loading():
    """Demonstrate efficient model loading patterns"""
    if not YOLO_AVAILABLE:
        print("\nSkipping model loading tests (YOLO not available)")
        return
    
    print("\n2. Model Loading Patterns")
    print("-" * 70)
    
    # ❌ INEFFICIENT: Loading model in a function called repeatedly
    @time_function
    def inefficient_detect():
        """Loads model on every call - very slow!"""
        model = YOLO('yolov8n.pt')  # Downloads and loads model
        # Simulated detection
        return "detected"
    
    # ✅ EFFICIENT: Load model once, use multiple times
    class EfficientDetector:
        def __init__(self):
            self.model = YOLO('yolov8n.pt')  # Load once
        
        @time_function
        def detect(self):
            """Reuses loaded model - much faster"""
            # Simulated detection
            return "detected"
    
    print("First call loads model:")
    # inefficient_detect()  # Commented - would download model
    print("inefficient_detect (loads every time): ~500-1000 ms")
    
    print("\nEfficient pattern:")
    detector = EfficientDetector()
    print("Initialization (one-time): ~500-1000 ms")
    # detector.detect()
    # detector.detect()
    print("detector.detect (reuses model): ~1-5 ms")


# ============================================================================
# Example 3: Batch Processing vs Sequential
# ============================================================================

def test_batch_processing():
    """Compare batch vs sequential processing"""
    print("\n3. Batch Processing (100 images)")
    print("-" * 70)
    
    # Simulate images
    images = [np.random.rand(640, 640, 3) for _ in range(100)]
    
    @time_function
    def process_sequential():
        """Inefficient: Process one image at a time"""
        results = []
        for img in images:
            # Simulate processing (e.g., normalization)
            processed = img / 255.0
            result = processed.mean()
            results.append(result)
        return results
    
    @time_function
    def process_batch():
        """Efficient: Process as batch with NumPy"""
        batch = np.array(images)
        processed = batch / 255.0
        results = processed.mean(axis=(1, 2, 3))
        return results
    
    process_sequential()
    process_batch()


# ============================================================================
# Example 4: Frame Skipping for Real-time Video
# ============================================================================

def test_frame_skipping():
    """Demonstrate frame skipping for real-time processing"""
    if not CV2_AVAILABLE:
        print("\nSkipping frame processing tests (OpenCV not available)")
        return
    
    print("\n4. Video Frame Processing (300 frames)")
    print("-" * 70)
    
    # Simulate video frames
    frames = [np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8) 
              for _ in range(300)]
    
    @time_function
    def process_every_frame():
        """Inefficient: Process every single frame"""
        results = []
        for frame in frames:
            # Simulate expensive processing (e.g., object detection)
            processed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            result = processed.mean()
            results.append(result)
        return results
    
    @time_function
    def process_every_nth_frame(n=5):
        """Efficient: Process every Nth frame"""
        results = []
        for i, frame in enumerate(frames):
            if i % n == 0:
                processed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                result = processed.mean()
                results.append(result)
        return results
    
    process_every_frame()
    process_every_nth_frame(5)  # Process every 5th frame


# ============================================================================
# Example 5: Memory-Efficient Image Processing
# ============================================================================

def test_memory_efficiency():
    """Compare memory-efficient vs memory-intensive approaches"""
    if not CV2_AVAILABLE:
        print("\nSkipping memory efficiency tests (OpenCV not available)")
        return
    
    print("\n5. Memory-Efficient Processing (1000 images)")
    print("-" * 70)
    
    @time_function
    def load_all_then_process():
        """Inefficient: Load all images into memory"""
        images = [np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
                  for _ in range(1000)]
        results = []
        for img in images:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            results.append(gray.mean())
        return results
    
    @time_function
    def process_on_the_fly():
        """Efficient: Process one at a time (generator pattern)"""
        results = []
        for _ in range(1000):
            # Simulate loading one image at a time
            img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            results.append(gray.mean())
            # Image is garbage collected immediately
        return results
    
    load_all_then_process()
    process_on_the_fly()


# ============================================================================
# Example 6: Preprocessing Pipeline Optimization
# ============================================================================

def test_preprocessing_pipeline():
    """Compare different preprocessing approaches"""
    if not CV2_AVAILABLE:
        print("\nSkipping preprocessing tests (OpenCV not available)")
        return
    
    print("\n6. Preprocessing Pipeline (100 images)")
    print("-" * 70)
    
    images = [np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
              for _ in range(100)]
    
    @time_function
    def inefficient_preprocessing():
        """Multiple operations, not optimized"""
        results = []
        for img in images:
            # Resize
            resized = cv2.resize(img, (640, 640))
            # Convert to grayscale
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            # Normalize
            normalized = gray.astype(np.float32) / 255.0
            # Convert back
            result = (normalized * 255).astype(np.uint8)
            results.append(result)
        return results
    
    @time_function
    def efficient_preprocessing():
        """Optimized: Fewer conversions, faster interpolation"""
        results = []
        for img in images:
            # Resize with faster interpolation
            resized = cv2.resize(img, (640, 640), interpolation=cv2.INTER_NEAREST)
            # Convert to grayscale (stays as uint8)
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            results.append(gray)
        return results
    
    inefficient_preprocessing()
    efficient_preprocessing()


# ============================================================================
# Best Practices Summary
# ============================================================================

def print_best_practices():
    """Print CV/AI optimization best practices"""
    print("\n" + "=" * 70)
    print("Computer Vision & AI Optimization Best Practices")
    print("=" * 70)
    print("""
1. MODEL LOADING
   ✓ Load model once at initialization
   ✗ Don't reload model for each inference

2. IMAGE PREPROCESSING
   ✓ Use OpenCV for resizing (optimized in C++)
   ✓ Use INTER_NEAREST for speed when quality isn't critical
   ✗ Avoid manual resizing with loops

3. BATCH PROCESSING
   ✓ Process multiple images together when possible
   ✓ Use NumPy vectorized operations
   ✗ Avoid processing one image at a time in production

4. REAL-TIME VIDEO
   ✓ Skip frames (process every Nth frame)
   ✓ Use smaller models (YOLOv8n vs YOLOv8x)
   ✓ Reduce input resolution when possible
   ✗ Don't process every frame if not necessary

5. MEMORY MANAGEMENT
   ✓ Process images on-the-fly (generator pattern)
   ✓ Release large objects when done
   ✗ Avoid loading all images into memory

6. GPU ACCELERATION
   ✓ Use GPU when available (CUDA)
   ✓ Keep data on GPU between operations
   ✗ Don't transfer data between CPU/GPU unnecessarily

7. MODEL OPTIMIZATION
   ✓ Use quantization (FP16 or INT8)
   ✓ Use TensorRT for NVIDIA GPUs
   ✓ Use ONNX Runtime for cross-platform optimization
   ✗ Don't use FP32 models in production if speed matters
    """)


# ============================================================================
# Main Benchmark Runner
# ============================================================================

def run_benchmarks():
    """Run all CV/AI performance benchmarks"""
    print("=" * 70)
    print("Computer Vision & AI Performance Examples")
    print("=" * 70)
    
    test_image_resizing()
    test_model_loading()
    test_batch_processing()
    test_frame_skipping()
    test_memory_efficiency()
    test_preprocessing_pipeline()
    print_best_practices()
    
    print("\n" + "=" * 70)
    print("Benchmark Complete!")
    print("=" * 70)


if __name__ == "__main__":
    run_benchmarks()

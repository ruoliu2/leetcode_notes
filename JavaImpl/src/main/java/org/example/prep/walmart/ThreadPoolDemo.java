package org.example.prep.walmart;

// Main class to demonstrate the ThreadPool
public class ThreadPoolDemo {
  public static void main(String[] args) {
    ThreadPool threadPool = new ThreadPool(3); // Create a thread pool with 3 threads

    // Submit tasks to the thread pool
    for (int i = 1; i <= 10; i++) {
      final int taskNumber = i;
      threadPool.submit(new ExampleTask("Task " + taskNumber));
    }

    // Shutdown the thread pool
    threadPool.shutdown();
  }
}

package org.example.prep.walmart;

import java.util.LinkedList;
import java.util.Queue;

// Task interface representing a runnable task
interface Task {
  void execute();
}

// ThreadPool class
class ThreadPool {
  private final int numberOfThreads;
  private final Queue<Task> taskQueue;
  private final WorkerThread[] workerThreads;
  private boolean isShutdown = false;

  public ThreadPool(int numberOfThreads) {
    this.numberOfThreads = numberOfThreads;
    taskQueue = new LinkedList<>();
    workerThreads = new WorkerThread[numberOfThreads];

    for (int i = 0; i < numberOfThreads; i++) {
      workerThreads[i] = new WorkerThread();
      workerThreads[i].start();
    }
  }

  public synchronized void submit(Task task) {
    if (isShutdown) {
      throw new IllegalStateException("ThreadPool is shut down");
    }
    taskQueue.offer(task);
    notify(); // Notify a worker thread that a new task is available
  }

  public synchronized Task take() throws InterruptedException {
    while (taskQueue.isEmpty()) {
      wait(); // Wait until a task is available
    }
    return taskQueue.poll();
  }

  public synchronized void shutdown() {
    isShutdown = true;
    for (WorkerThread worker : workerThreads) {
      worker.interrupt(); // Interrupt all worker threads
    }
  }

  private class WorkerThread extends Thread {
    @Override
    public void run() {
      while (!isShutdown) {
        try {
          Task task = take(); // Wait for a task
          task.execute(); // Execute the task
        } catch (InterruptedException e) {
          // Thread is interrupted, exit
          break;
        }
      }
    }
  }
}

// Example Task implementation
class ExampleTask implements Task {
  private final String name;

  public ExampleTask(String name) {
    this.name = name;
  }

  @Override
  public void execute() {
    System.out.println("Executing task: " + name);
  }
}

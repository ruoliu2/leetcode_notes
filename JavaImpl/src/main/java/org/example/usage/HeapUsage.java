package org.example.usage;

import java.util.Collections;
import java.util.PriorityQueue;
import org.example.util.Tuple;

public class HeapUsage {
  public static void main(String[] args) {
    // maxheap
    PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());

    PriorityQueue<Tuple<Integer, Integer>> priorityQueue =
        new PriorityQueue<>(
            (a, b) -> a.getFirst().compareTo(b.getFirst()) // Order by first
            );

    // Adding elements to the heap
    maxHeap.add(10);
    maxHeap.add(20);
    maxHeap.add(5);
    maxHeap.add(15);

    // minheap
    PriorityQueue<Integer> minHeap = new PriorityQueue<>();
    minHeap.add(10);
    minHeap.add(20);
    minHeap.add(5);
    minHeap.add(15);

    // Displaying and removing elements from the heap
    System.out.println("Max-Heap elements in sorted order:");
    while (!maxHeap.isEmpty()) {
      System.out.println(maxHeap.poll()); // Removes the root (largest element)
    }

    System.out.println("Min-Heap elements in sorted order:");
    while (!minHeap.isEmpty()) {
      System.out.println(minHeap.poll()); // Removes the root (smallest element)
    }
  }
}

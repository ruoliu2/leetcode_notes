package org.example.graph;

import java.util.*;

public class TopSort {
  public boolean canFinish(int numCourses, int[][] prerequisites) {
    // Create in-degree and adjacency list (pre)
    Map<Integer, Integer> inDeg = new HashMap<>();
    Map<Integer, List<Integer>> pre = new HashMap<>();

    // Initialize the in-degree and adjacency list
    for (int[] pair : prerequisites) {
      int n1 = pair[0], n2 = pair[1];
      inDeg.put(n2, inDeg.getOrDefault(n2, 0) + 1);
      pre.computeIfAbsent(n1, k -> new ArrayList<>()).add(n2);
    }

    // Find all nodes with zero in-degree
    Queue<Integer> zeroDeg = new LinkedList<>();
    for (int i = 0; i < numCourses; i++) {
      if (!inDeg.containsKey(i)) {
        zeroDeg.offer(i);
      }
    }

    int visit = 0;
    Queue<Integer> q = new LinkedList<>(zeroDeg);

    // Process the queue
    while (!q.isEmpty()) {
      int cur = q.poll();
      visit++;
      if (!pre.containsKey(cur)) continue;
      for (int nei : pre.get(cur)) {
        inDeg.put(nei, inDeg.get(nei) - 1);
        if (inDeg.get(nei) == 0) {
          q.offer(nei);
        }
      }
    }

    // Check if we visited all the courses
    return visit == numCourses;
  }
}

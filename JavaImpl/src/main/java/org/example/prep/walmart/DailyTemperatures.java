package org.example.prep.walmart;

import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;

public class DailyTemperatures {
  public int[] dailyTemperatures(int[] temperatures) {
    int n = temperatures.length;
    int[] answer = new int[n];
    Deque<Integer> stack = new ArrayDeque<>();

    for (int i = 0; i < n; i++) {
      while (!stack.isEmpty() && temperatures[i] > temperatures[stack.peek()]) {
        int idx = stack.pop();
        answer[idx] = i - idx;
      }
      stack.push(i);
    }

    return answer;
  }

  public static void main(String[] args) {
    DailyTemperatures solution = new DailyTemperatures();
    int[] temperatures = {73, 74, 75, 71, 69, 72, 76, 73};
    int[] result = solution.dailyTemperatures(temperatures);

    System.out.println(Arrays.toString(result));
  }
}

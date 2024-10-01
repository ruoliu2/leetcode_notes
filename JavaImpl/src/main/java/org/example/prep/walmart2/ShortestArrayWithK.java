package org.example.prep.walmart2;

import java.util.HashMap;
import java.util.Map;

public class ShortestArrayWithK {
  public int smallestArrKDistinct(int[] arr, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    int l = 0;
    int res = Integer.MAX_VALUE;
    for (int r = 0; r < arr.length; r++) {
      freq.put(arr[r], freq.getOrDefault(arr[r], 0) + 1);
      while (freq.size() == k) {
        res = Math.min(res, r - l + 1);
        freq.put(arr[l], freq.get(arr[l]) - 1);
        if (freq.get(arr[l]) == 0) {
          freq.remove(arr[l]);
        }
        l++;
      }
    }
    return res == Integer.MAX_VALUE ? -1 : res;
  }

  public static void main(String[] args) {
    ShortestArrayWithK sol = new ShortestArrayWithK();
    int[] arr = {1, 2, 1, 2, 3};
    int k = 3;
    System.out.println(sol.smallestArrKDistinct(arr, k)); // Expected output: 2
  }
}

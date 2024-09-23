package org.example.search;

public class BinarySearch {

  public static int bisectLeft(int[] arr, int target) {
    int l = 0, r = arr.length;
    while (l < r) {
      int m = (l + r) / 2;
      if (arr[m] < target) {
        l = m + 1;
      } else {
        r = m;
      }
    }
    return l;
  }

  public static void main(String[] args) {
    int[] arr = {1, 3, 5, 7, 9};
    int target = 6;
    System.out.println(bisectLeft(arr, target)); // Output will be 3
  }
}

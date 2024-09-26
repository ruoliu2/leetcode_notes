package org.example.prep.walmart;

import java.util.Arrays;

public class SortArray {
  public static void sort(int[] arr) {
    Arrays.sort(arr);
  }

  public static void quickSort(int[] arr, int s, int e) {
    if (s >= e) return;
    int p = s;
    for (int i = s; i < e; i++) {
      if (arr[i] < arr[e]) {
        int temp = arr[i];
        arr[i] = arr[p];
        arr[p] = temp;
        p++;
      }
    }
    int temp = arr[e];
    arr[e] = arr[p];
    arr[p] = temp;
    quickSort(arr, s, p - 1);
    quickSort(arr, p + 1, e);
  }

  public static void main(String[] args) {
    int[] arr = {3, 2, 1, 5, 4};
    SortArray.quickSort(arr, 0, arr.length - 1);
    System.out.println(Arrays.toString(arr));
  }
}

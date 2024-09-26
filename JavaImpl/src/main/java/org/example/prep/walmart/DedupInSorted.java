package org.example.prep.walmart;

import java.util.Arrays;

public class DedupInSorted {
  public static int[] removeDuplicates(int[] sortedArr) {
    if (sortedArr.length == 0) {
      return new int[0]; // Return empty array if input is empty
    }

    // Pointer for tracking unique elements
    int uniqueIndex = 0;

    // Traverse the array and move unique elements to the front
    for (int i = 1; i < sortedArr.length; i++) {
      if (sortedArr[i] != sortedArr[uniqueIndex]) {
        uniqueIndex++;
        sortedArr[uniqueIndex] = sortedArr[i];
      }
    }

    // Copy the unique portion of the array into a new array
    return Arrays.copyOfRange(sortedArr, 0, uniqueIndex + 1);
  }

  public static void main(String[] args) {
    int[] sortedArr = {1, 1, 2, 2, 3, 4, 4, 5, 5, 5};
    int[] dedupedArr = DedupInSorted.removeDuplicates(sortedArr);
    System.out.println(Arrays.toString(dedupedArr));
  }
}

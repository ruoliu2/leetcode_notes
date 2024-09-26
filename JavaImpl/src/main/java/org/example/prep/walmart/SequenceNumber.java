package org.example.prep.walmart;

public class SequenceNumber {
  public static int[] generateSequence(int start, int end) {
    // If start is greater than or equal to end, return an empty array
    if (start >= end) {
      return new int[0];
    }

    // Create an array with the size equal to the difference between end and start
    int[] result = new int[end - start];

    // Fill the array with integers from start up to but not including end
    for (int i = 0; i < result.length; i++) {
      result[i] = start + i;
    }

    return result;
  }
}

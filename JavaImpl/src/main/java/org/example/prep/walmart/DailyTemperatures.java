package org.example.prep.walmart;

public class Temperatures {
  public int[] warmerTemp(int[] temperatures) {
    int[] result = new int[temperatures.length];

    for (int i = 0; i < temperatures.length; i++) {
      int currentTemp = temperatures[i];
      int days = 0;
      for (int j = i + 1; j < temperatures.length; j++) {
        if (temperatures[j] > currentTemp) {
          days = j - i;
          break;
        }
      }
      result[i] = days;
    }
    return result;
  }
}

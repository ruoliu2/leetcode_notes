package org.example.prep.walmart;

import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class NumberFrequency {
  public static void main(String[] args) {
    int[] array = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    // Convert int[] to Stream<Integer>, then group and count
    Map<Integer, Long> frequencyMap =
        Arrays.stream(array)
            .boxed()
            .collect(Collectors.groupingBy(element -> element, Collectors.counting()));

    List<Integer> arr = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

    Map<Integer, Long> frequencyMap2 =
        arr.stream().collect(Collectors.groupingBy(element -> element, Collectors.counting()));

    // Print the frequency of each number
    frequencyMap.forEach(
        (number, count) ->
            System.out.println("Number " + number + " appears " + count + " time(s)."));
  }
}

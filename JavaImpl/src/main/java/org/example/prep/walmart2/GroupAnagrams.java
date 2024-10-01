package org.example.prep.walmart2;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

class GroupAnagrams {
  public List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> anagrams = new HashMap<>();
    for (String word : strs) {
      int[] freq = new int[26];
      for (char c : word.toCharArray()) {
        freq[c - 'a']++;
      }

      StringBuilder key = new StringBuilder();
      for (int i = 0; i < 26; i++) {
        key.append("#").append(freq[i]);
      }

      String keyString = key.toString();
      if (!anagrams.containsKey(keyString)) {
        anagrams.put(keyString, new ArrayList<>());
      }
      anagrams.get(keyString).add(word);
    }
    return new ArrayList<>(anagrams.values());
  }
}

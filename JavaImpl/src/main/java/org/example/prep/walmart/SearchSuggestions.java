package org.example.prep.walmart;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

// 1268. Search Suggestions System
class SearchSuggestions {
  public List<List<String>> suggestedProducts(String[] products, String searchWord) {
    Arrays.sort(products);
    List<List<String>> result = new ArrayList<>();
    String prefix = "";
    int i = 0;

    for (char c : searchWord.toCharArray()) {
      prefix += c;
      int index = bisectLeft(products, prefix, i);
      List<String> suggestions = new ArrayList<>();

      for (int j = index; j < Math.min(products.length, index + 3); j++) {
        if (products[j].startsWith(prefix)) {
          suggestions.add(products[j]);
        }
        break;
      }
      result.add(suggestions);
      i = index; // Update i for next prefix search
    }
    return result;
  }

  private int bisectLeft(String[] products, String target, int start) {
    int l = start;
    int r = products.length;

    while (l < r) {
      int m = (l + r) / 2;
      if (products[m].compareTo(target) < 0) {
        l = m + 1;
      } else {
        r = m;
      }
    }

    return l;
  }
}

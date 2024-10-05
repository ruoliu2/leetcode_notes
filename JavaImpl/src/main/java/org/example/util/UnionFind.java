package org.example.util;

class UnionFind {
  private final int[] parent;
  private final int[] rank;

  public UnionFind(int n) {
    parent = new int[n];
    rank = new int[n];
    for (int i = 0; i < n; i++) {
      parent[i] = i;
      rank[i] = 1;
    }
  }

  public int find(int n1) {
    if (n1 != parent[n1]) {
      parent[n1] = find(parent[n1]); // Path compression
    }
    return parent[n1];
  }

  public int union(int n1, int n2) {
    int p1 = find(n1);
    int p2 = find(n2);
    if (p1 == p2) {
      return 0;
    }
    if (rank[p2] > rank[p1]) {
      int temp = p1;
      p1 = p2;
      p2 = temp;
    }
    parent[p2] = p1;
    rank[p1] += rank[p2];
    return 1;
  }
}

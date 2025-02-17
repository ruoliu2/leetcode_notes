from collections import OrderedDict


# Define the abstract base class for eviction policies.
class EvictionPolicy:
    def on_get(self, key, cache):
        """
        Called when a key is read from the cache.
        May modify the cache (e.g., evict the key after reading).
        """
        raise NotImplementedError("on_get must be implemented by the subclass.")

    def on_set(self, key, cache):
        """
        Called before inserting a new key.
        May modify the cache (e.g., evict an item if capacity is reached).
        """
        raise NotImplementedError("on_set must be implemented by the subclass.")


# Policy 1: Evict an item immediately after it is read.
class EvictAfterReadPolicy(EvictionPolicy):
    def on_get(self, key, cache):
        # Remove the key after reading.
        if key in cache._storage:
            # Debug output for demonstration.
            print(f"EvictAfterReadPolicy: Evicting key '{key}' after read.")
            del cache._storage[key]

    def on_set(self, key, cache):
        # No special action on set.
        pass


# Policy 2: Evict an item only after reaching the caching limit.
# We'll use FIFO (first-in, first-out) eviction in this example.
class EvictAfterLimitPolicy(EvictionPolicy):
    def on_get(self, key, cache):
        # No eviction on read.
        pass

    def on_set(self, key, cache):
        # Check if adding a new item would exceed capacity.
        if len(cache._storage) >= cache.capacity:
            # Evict the oldest item (FIFO)
            oldest_key, _ = cache._storage.popitem(last=False)
            print(
                f"EvictAfterLimitPolicy: Evicting oldest key '{oldest_key}' to make room."
            )


# The Cache class that uses a provided eviction policy.
class Cache:
    def __init__(self, capacity: int, eviction_policy: EvictionPolicy):
        self.capacity = capacity
        # Using an OrderedDict to keep track of insertion order for FIFO eviction.
        self._storage = OrderedDict()
        self.eviction_policy = eviction_policy

    def get(self, key):
        # Retrieve the value if present.
        if key not in self._storage:
            print(f"Cache miss for key '{key}'.")
            return None

        value = self._storage[key]
        # Let the eviction policy handle any actions upon reading.
        self.eviction_policy.on_get(key, self)
        return value

    def set(self, key, value):
        # Before setting, invoke the eviction policy to ensure there's room.
        self.eviction_policy.on_set(key, self)
        # Insert the new key-value pair.
        self._storage[key] = value
        # Maintain insertion order: if key already existed, move it to the end.
        self._storage.move_to_end(key)
        print(
            f"Set key '{key}' with value '{value}'. Current keys: {list(self._storage.keys())}"
        )


# --- Example Usage ---
if __name__ == "__main__":
    print("Using EvictAfterReadPolicy:")
    cache1 = Cache(capacity=3, eviction_policy=EvictAfterReadPolicy())
    cache1.set("A", 1)
    cache1.set("B", 2)
    cache1.set("C", 3)

    # Reading key "B" should cause it to be evicted immediately.
    print("Get 'B':", cache1.get("B"))
    # Attempt to get "B" again should result in a miss.
    print("Get 'B' again:", cache1.get("B"))
    print("Current keys in cache1:", list(cache1._storage.keys()))

    print("\nUsing EvictAfterLimitPolicy:")
    cache2 = Cache(capacity=3, eviction_policy=EvictAfterLimitPolicy())
    cache2.set("X", 10)
    cache2.set("Y", 20)
    cache2.set("Z", 30)
    # This next insertion should trigger eviction of the oldest key ("X")
    cache2.set("W", 40)
    print("Current keys in cache2:", list(cache2._storage.keys()))

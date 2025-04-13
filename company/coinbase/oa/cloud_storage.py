import math


class File:
    def __init__(self, name: str, size: int, owner: str):
        self.name = name
        self.size = size
        self.owner = owner


class User:
    def __init__(self, user_id: str, capacity: float):
        self.user_id = user_id
        self.capacity = capacity  # use float('inf') for admin
        self.used = 0
        self.files = set()  # set of file names


class CloudStorage:
    def __init__(self):
        self.files = {}  # maps file name -> File instance
        self.users = {}  # maps user_id -> User instance
        self.backups = {}  # maps user_id -> backup snapshot {file_name: size}
        # initialize admin with unlimited capacity
        self.users["admin"] = User("admin", float("inf"))

    # Level 1 operations
    def add_file(self, name: str, size: int) -> bool:
        # admin adds file by default
        return self.add_file_by("admin", name, size) is not None

    def get_file_size(self, name: str) -> int:
        if name in self.files:
            return self.files[name].size
        return None

    def delete_file(self, name: str) -> int:
        if name not in self.files:
            return None
        file = self.files.pop(name)
        user = self.users[file.owner]
        if name in user.files:
            user.files.remove(name)
            user.used -= file.size
        return file.size

    # Level 2: Get top-n largest files with a given prefix.
    def get_n_largest(self, prefix: str, n: int) -> [str]:
        # Filter files that start with prefix
        matching = [f for f in self.files.values() if f.name.startswith(prefix)]
        # Sort by size descending; on tie, lexicographical order of name
        matching.sort(key=lambda f: (-f.size, f.name))
        return [f.name for f in matching[:n]]

    # Level 3: User-specific operations
    def add_user(self, user_id: str, capacity: int) -> bool:
        if user_id in self.users:
            return False
        self.users[user_id] = User(user_id, capacity)
        return True

    def add_file_by(self, user_id: str, name: str, size: int) -> int:
        if user_id not in self.users or name in self.files:
            return None
        user = self.users[user_id]
        if user.used + size > user.capacity:
            return None  # would exceed capacity
        # Create file and add to storage
        file = File(name, size, user_id)
        self.files[name] = file
        user.files.add(name)
        user.used += size
        # Return remaining capacity (for admin, it will be inf)
        return math.inf if user.capacity == math.inf else user.capacity - user.used

    def merge_users(self, target_user_id: str, source_user_id: str) -> bool:
        # Merge source user's files into target user.
        if target_user_id not in self.users or source_user_id not in self.users:
            return False
        target = self.users[target_user_id]
        source = self.users[source_user_id]
        # Process each file from the source
        for fname in list(source.files):
            file = self.files.get(fname)
            # if target already has a file with same name, skip
            if fname in target.files:
                # remove the file from storage since duplicate is not merged
                self.files.pop(fname)
                source.used -= file.size
            # Otherwise, check capacity before moving
            elif target.used + file.size <= target.capacity:
                # Reassign file ownership to target user
                file.owner = target_user_id
                target.files.add(fname)
                target.used += file.size
            # Remove file from source regardless of merge outcome.
            source.files.remove(fname)
        # Delete source user and any backup
        self.users.pop(source_user_id)
        self.backups.pop(source_user_id, None)
        return True

    # Level 4: Backup and restore operations
    def backup_user(self, user_id: str) -> int:
        if user_id not in self.users:
            return None
        user = self.users[user_id]
        # Create snapshot: file name -> size
        backup_snapshot = {fname: self.files[fname].size for fname in user.files}
        self.backups[user_id] = backup_snapshot
        return len(backup_snapshot)

    def restore_user(self, user_id: str) -> int:
        if user_id not in self.users:
            return None
        user = self.users[user_id]
        # First, remove all current files owned by user from global storage.
        for fname in list(user.files):
            if fname in self.files:
                self.files.pop(fname)
        user.files.clear()
        user.used = 0

        restored = 0
        backup_snapshot = self.backups.get(user_id, {})
        for fname, fsize in backup_snapshot.items():
            # Only restore if file name is not taken by another user.
            if fname in self.files:
                continue
            # Restore file (assuming backup was valid so capacity is not exceeded)
            file = File(fname, fsize, user_id)
            self.files[fname] = file
            user.files.add(fname)
            user.used += fsize
            restored += 1
        return restored


# --- Example usage ---
if __name__ == "__main__":
    cs = CloudStorage()

    # Level 1: admin operations
    print(cs.add_file("/dir/file1.txt", 5))  # True
    print(cs.add_file("/dir/file2.txt", 20))  # True
    print(cs.add_file("/dir/deeper/file3.mov", 9))  # True
    print(cs.get_file_size("/dir/file1.txt"))  # 5
    print(cs.delete_file("/dir/file1.txt"))  # 5
    print(cs.get_file_size("/dir/file1.txt"))  # None

    # Level 2: get n largest files with a prefix
    print(cs.get_n_largest("/dir", 2))  # Should list the 2 largest under /dir

    # Level 3: add users and add file by user
    cs.add_user("user1", 50)
    print(cs.add_file_by("user1", "/user1/file.txt", 30))  # Remaining capacity 20
    print(cs.add_file_by("user1", "/user1/another.txt", 25))  # None (exceeds capacity)

    cs.add_user("user2", 40)
    cs.add_file_by("user2", "/user2/data.bin", 20)
    # Merge user2 into user1 (files that can be merged will be moved, others skipped)
    print(cs.merge_users("user1", "user2"))  # True

    # Level 4: backup and restore for user1
    cs.backup_user("user1")
    # Simulate deletion of all user1 files
    for f in list(cs.users["user1"].files):
        cs.delete_file(f)
    # Restore user1's backup
    print(cs.restore_user("user1"))  # Should restore backed-up files count

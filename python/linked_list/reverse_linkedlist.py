# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy, cur = None, head
        prev = dummy
        while cur:
            nxt = cur.next  # save next of cur
            cur.next = prev
            # move both ptrs
            prev, cur = cur, nxt
        return prev

        # 1 2 3 4
        # 4 3 2 1
        # 4 3 2
        if (not head) or (not head.next):
            return head
        p = self.reverseList(head.next)
        head.next.next = head
        head.next = None
        return p

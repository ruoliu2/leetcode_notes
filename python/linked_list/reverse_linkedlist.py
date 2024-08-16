class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy, cur = None, head
        prev = dummy
        while cur:
            nxt = cur.next  # save next of cur
            cur.next = prev
            prev, cur = cur, nxt  # move both ptrs
        return prev

    def reverseList2(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if (not head) or (not head.next):
            return head
        p = self.reverseList(head.next)
        head.next.next = head
        head.next = None
        return p

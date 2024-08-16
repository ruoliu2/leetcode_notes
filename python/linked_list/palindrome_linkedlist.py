# 234
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        rev = self.reverse(slow)
        while rev:
            if head.val != rev.val:
                return False
            head, rev = head.next, rev.next
        return True

    def reverse(self, head: ListNode) -> ListNode:
        pre, cur = None, head
        while cur:
            nxt = cur.next
            cur.next = pre
            pre, cur = cur, nxt
        return pre

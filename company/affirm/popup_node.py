"""
Pop Up Node (Affirm)

Given a DOM tree, when opening a POPUP node:
  1. Path from root to POPUP: hidden = False
  2. Siblings of nodes on path: hidden = True
  3. POPUP's siblings: hidden = True
  4. All other nodes: unchanged

Approach: DFS returns whether subtree contains POPUP.
  - If child has POPUP: child.hidden = False
  - If sibling of child with POPUP: sibling.hidden = True
"""


class DomNode:
    def __init__(self, id: str, children: list["DomNode"] = None):
        self.id = id
        self.children = children or []
        self.hidden = False


def open_popup(root: DomNode) -> bool:
    """Show path to POPUP, hide siblings on path. Returns True if POPUP found."""
    if not root:
        return False
    if root.id == "POPUP":
        root.hidden = False
        return True

    # Check which children have POPUP in subtree
    child_has_popup = {child: open_popup(child) for child in root.children}
    has_popup = any(child_has_popup.values())

    # If any child has POPUP, show that child, hide siblings
    if has_popup:
        for child in root.children:
            child.hidden = not child_has_popup[child]
        root.hidden = False

    return has_popup


def print_tree(node: DomNode, indent: int = 0):
    status = "hidden" if node.hidden else "visible"
    print("  " * indent + f"{node.id}: {status}")
    for child in node.children:
        print_tree(child, indent + 1)


if __name__ == "__main__":
    #       root
    #      /    \
    #     A      B
    #    / \      \
    #   C  POPUP   D

    tree = DomNode("root", [
        DomNode("A", [
            DomNode("C"),
            DomNode("POPUP"),
        ]),
        DomNode("B", [
            DomNode("D"),
        ]),
    ])

    print("Before:")
    print_tree(tree)

    open_popup(tree)

    print("\nAfter open_popup:")
    print_tree(tree)
    # root: visible (on path)
    # A: visible (on path)
    # C: hidden (sibling of POPUP)
    # POPUP: visible
    # B: hidden (sibling of A which is on path)
    # D: unchanged (not on path, not sibling of path)

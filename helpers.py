# helpers.py
from collections import deque
from typing import Union, List, Optional # Import what's needed for older Python versions

# Definition for a binary tree node, as used on LeetCode.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# CORRECTED for older Python versions
def build_tree(nodes: List[int]) -> Optional[TreeNode]:
    """Builds a binary tree from a LeetCode-style list representation."""
    if not nodes:
        return None

    root = TreeNode(nodes[0])
    queue = deque([root])
    i = 1
    while queue and i < len(nodes):
        node = queue.popleft()
        
        # Left child
        if i < len(nodes) and nodes[i] is not None:
            node.left = TreeNode(nodes[i])
            queue.append(node.left)
        i += 1
        
        # Right child
        if i < len(nodes) and nodes[i] is not None:
            node.right = TreeNode(nodes[i])
            queue.append(node.right)
        i += 1
            
    return root

# CORRECTED for older Python versions
def tree_to_list(root: Optional[TreeNode]) -> List:
    """Converts a binary tree back to a LeetCode-style list for comparison."""
    if not root:
        return []
    
    output = []
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        if node:
            output.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            output.append(None)
            
    # Trim trailing nulls
    while output and output[-1] is None:
        output.pop()
        
    return output

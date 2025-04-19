
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(node, value):
    if node is None:
        raise ValueError("BSPNode cannot be None")
    if value < node.value:
        if node.left is None:
            node.left = Node(value)
        else:
            insert(node.left, value)
    elif value > node.value:
        if node.right is None:
            node.right = Node(value)
        else:
            insert(node.right, value)
        
def traverse(node, player_pos):
    if not node:
        return
    else:
        if player_pos <= node.value:
            traverse(node.left, player_pos)
            print(node.value, end=' ')
            traverse(node.right, player_pos)
        else:
            traverse(node.right, player_pos)
            print(node.value, end=' ')
            traverse(node.left, player_pos)

if __name__ == "__main__":
    root = Node(0)
    [insert(root, value) for value in [-15, -8, 6, 12 ,20]]
    traverse(root, 8)
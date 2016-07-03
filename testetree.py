import testeLex4

def newToken():
    tok = testeLex4.retornaToken()
    return tok

def end(t):
    if not t:
        return true

class Node:
    def __init__(self, token):
        self.data = token.value
        self.children = []

    def addChild(self, node):
        self.children.append(node)


t = newToken()
tree = Node(t)
for i in range(10):
    t2 = newToken()
    q = Node(t2)
    tree.addChild(q)
for c in tree.children:
    print(c.data)
    
for i in range(10):
    t2 = newToken()
    q = Node(t2)
    tree.addChild(q)
for c in tree.children:
    print(c.data)

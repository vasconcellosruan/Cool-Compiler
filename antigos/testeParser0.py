import testeLex4

def newToken():
    tok = testeLex4.retornaToken()
    return tok

def end(t):
    if not t:
        return True

def error(t, STRING):
    print('Erro: o tipo %s era esperado na linha %d, mas nao apareceu.' % (STRING,t.lineno))

class Node: #Nossa arvore
    def __init__(self, data, token = None):
        self.data = data
        self.token = token
        self.children = []

    def addChild(self, node):
        self.children.append(node)

def isLeaf(no, t):
    no2 = Node(t.value,t)
    no.addChild(no2)
    
def inClass(t, tree):
        no = Node('CLASS')
        tree.addChild(no)
        #no2 = Node(t.value,t)
        #no.addChild(no2)
        isLeaf(no, t)
        t = newToken()
        if((t.type) == 'TYPE'):
            no = Node('TYPE')
            tree.addChild(no)
            isLeaf(no, t)
            t = newToken()
            if(t.type == 'INHERITS'):
                no = Node('INHERITS')
                tree.addChild(no)
                isLeaf(no, t)
                t = newToken()
                if(t.type == 'TYPE'):
                    no = Node('TYPE')
                    tree.addChild(no)
                    isLeaf(no, t)
                    t = newToken()
                else:
                    error(t, 'TYPE')         
            if(t.type == 'CHAVE_E'):
                no = Node('CHAVE_E')
                tree.addChild(no)
                isLeaf(no, t)
                t = newToken()
                if(t.type == 'ID'):
                    inFeature(t, tree)#chamada para FEATURE
                elif(t.type == 'CHAVE_D'):
                    no = Node('CHAVE_D')
                    tree.addChild(no)
                    isLeaf(no, t)
                else:
                    error(t, 'CHAVE_D')
            else:
                error(t, 'CHAVE_E')        
        else:
           error(t, 'TYPE') 


def inFeature(t, tree):
    #while True:
    pass


'''            
def isFormal():
def isExp():
'''

       
aux=0
#t1 = newToken()
while True: #loop infinito
    #t2 = newToken() #pega novo token
    t = newToken()#nao tinha o t = newToken() aqui
    if(not end(t)): #enquanto nao chegar ao final dos tokens
        if(not aux): #se for a primeira linha do programa
            tree = Node('PROGRAM')
            #tinha o t = newToken() aqui
            if(t.type == 'CLASS'):
                inClass(t,tree)
                print(tree.data)
                for i in tree.children:
                    print(i.data)
                    for j in i.children:
                        print(j.data)
            else:
                error()
                

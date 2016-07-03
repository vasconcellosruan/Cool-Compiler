import testeLex5

def newToken():
    tok = testeLex5.retornaToken()
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
                    t = inFeature(t, tree)#chamada para FEATURE
                if(t.type == 'CHAVE_D'):#testando: antes tinha elif
                    no = Node('CHAVE_D')
                    isLeaf(no, t)
                    tree.addChild(no)
                else:
                    error(t, '}')
            else:
                error(t, '{')        
        else:
           error(t, 'TYPE') 


def inFeature(t, tree):
    isEnd = False
    
    while not isEnd:#Enquanto nao for o fim - Lembrar do if(t.type == 'ID'): no final do while
        no = Node('FEATURE')
        tree.addChild(no)
        no2 = Node('ID')
        isLeaf(no2, t)
        no.addChild(no2)
        t = newToken()
        if(t.type == 'COLON'):
            no2 = Node('COLON')
            no.addChild(no2)
            isLeaf(no2, t)
            t = newToken()
            if(t.type == 'TYPE'):
                no2 = Node('TYPE')
                no.addChild(no2)
                isLeaf(no2, t)
                t = newToken()
                if(t.type == 'ATRIB'):
                    no2 = Node('ATRIB')
                    no.addChild(no2)
                    isLeaf(no2, t)
                    t = newToken()
                    if(isExp(t)):#Se for verdadeiro, chama inExp
                        inExp()
                    else:
                        error(t, 'EXPRESSÃO')
                if(t.type == 'CHAVE_D' and t.type != 'ID'):#TA FODA, MAS NOIS E TRETUDO KKK]
                    break
                else:
                    error(t, '}')
            else:
                error(t, 'TYPE')    
        else: #Jefferson, quero ver entender esse pedaço! HA HA HA
            if(t.type != 'PAREN_E'):
                error(t, ': ou (')
                break            
            if(t.type == 'PAREN_E'):
                pass
    return t
                

            
        
'''
no = Node('CHAVE_E')
tree.addChild(no)
isLeaf(no, t)
t = newToken()
'''
  
def isExp(t):
    aux = False
    if(t.type == 'ID'):
        aux = True
    if(t.type == 'IF'):
        aux = True
    if(t.type == 'WHILE'):
        aux = True
    if(t.type == 'CHAVE_E'):
        aux = True
    if(t.type == 'LET'):
        aux = True
    if(t.type == 'CASE'):
        aux = True
    if(t.type == 'NEW'):
        aux = True
    if(t.type == 'ISVOID'):
        aux = True
    if(t.type == 'OP'):
        aux = True
    if(t.type == 'TIL'):
        aux = True
    if(t.type == 'COMP'):
        aux = True
    if(t.type == 'NOT'):
        aux = True
    if(t.type == 'PAREN_E'):
        aux = True
    if(t.type == 'NUMBER'):
        aux = True
    if(t.type == 'STRING'):
        aux = True
    if(t.type == 'TRUE'):
        aux = True
    if(t.type == 'FALSE'):
        aux = True
    return aux
        

def inExp():
    pass


'''            
def inFormal():
'''


       
aux=0
tree = Node('PROGRAM')
#t1 = newToken()
while True: #loop infinito
    #t2 = newToken() #pega novo token
    t = newToken()#nao tinha o t = newToken() aqui
    if(not end(t)): #enquanto nao chegar ao final dos tokens
        if(not aux): #se for a primeira linha do programa
            #tree = Node('PROGRAM')
            #tinha o t = newToken() aqui
            if(t.type == 'CLASS'):
                inClass(t,tree)
            else:
                error(t, 'DEU PAU')
    else:
        break
    
print(tree.data)
for i in tree.children:
    print(i.data)
    for j in i.children:
        print(j.data)
        for k in j.children:
            print(k.data)

print("\n\nACABOU !!!")
    
                

# Alunos: Ruan Vasconcellos, Jefferson Garcia, Lucas Branco
#===============================================================================================================================================================
import testeLex7 as lex #SE MUDAR A VERSAO DO LEXICO TEM QUE ATUALIZAR AQUI E NO newToken()

def newToken():                     #chama novo token
    tok = lex.retornaToken()        #OBS: Não importa se é em loop ou em recursão, um novo token é sempre novo,
    return tok                      #chamado de qualquer lugar ou a qualquer hora no programa. USE SÓ QUANDO NECESSARIO

def end(t):#Verifica se acabou os tokens
    if not t:
        return True

def error(t, STRING): #Mensagem de erro padrão  
    if(STRING == 'ERROR'):
        print('Erro: %s na linha %d. Provalmente há algum simbolo repetido inexperado pela linguagem ou fora de uma CLASSE.' % (STRING, t.lineno))
    else:
        print('Erro: o tipo %s era esperado na linha %d.' % (STRING,t.lineno))

class Node: #Nossa arvore - Arvore genérica, cada nó tem N filhos
    def __init__(self, data, token = None):#O parametro 'token=None' permite "sobrecarga"
        self.data = data
        self.token = token
        self.children = []

    def addChild(self, node):#Adiciona filho à lista de filhos do nó
        self.children.append(node)


def isLeaf(no, t):          #Trata os nós que são folhas
    no2 = Node(str(t.value)+"\n",t)   #Não, não escolhemos um jeito bonitinho de ver se era folha. Sabemos quando vai ser pela gramática.
    no.addChild(no2)
    
def inClass(t, tree):       #Passando o último token e a raiz da árvore                  
        no = Node('CLASS')  #Essas linhas são bem padrões:                         #Devo criar um método para substituir essas 4 linhas tão comuns
        tree.addChild(no)   #Criamos um no e adiocinamos ele como filho
        isLeaf(no, t)       #Tratamos se forem folhas
        t = newToken()      #Pegamos um novo token
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
                if(t.type == 'TYPE' or t.type == 'IO'):
                    no = Node(t.type)
                    tree.addChild(no)
                    isLeaf(no, t)
                    t = newToken()
                else:
                    error(t, 'TYPE') #Erro passando t para pegarmos o número da linha e o que faltava        
            if(t.type == 'CHAVE_E'):
                no = Node('CHAVE_E')
                tree.addChild(no)
                isLeaf(no, t)
                t = newToken()
                if(t.type == 'ID'): #Caso especial - TODO FEATURE começa com ID
                    t = inFeature(t, tree)#chamada para FEATURE - Note que na volta da função o token nao muda, por isso forçamos com o retorno a mudar
                if(t.type == 'CHAVE_D'):
                    no = Node('CHAVE_D')
                    isLeaf(no, t)
                    tree.addChild(no)
                    t = newToken()
                else:
                    error(t, '} ou ID')
            else:
                error(t, '{')
        else:
           error(t, 'TYPE')
        if(t.type == 'SEMICOLON'):
            no = Node('SEMICOLON')
            tree.addChild(no)
            isLeaf(no, t)
        else:
            error(t, '; no final da CLASSE')


def inFeature(t, tree):
    while True:#Enquanto nao for o fim - Lembrar do if(t.type == 'ID'): no final do while
        no = Node('FEATURE')
        tree.addChild(no)#PERCEBA A MALDADE DO TREE, NO E NO2 A PARTIR DESSE PONTO KKKKK
        no2 = Node('ID')
        isLeaf(no2, t)
        no.addChild(no2)#Essa ordem com a linha de cima importa?
        t = newToken()
        if(t.type == 'COLON'): #COLON é :
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
                        t = inExp(t, no)#Provavelmente vai ter que ter um retorno t
                    else:
                        error(t, 'EXPRESSÃO')
                if(t.type == 'SEMICOLON'):
                    no2 = Node('SEMICOLON')
                    no.addChild(no2)
                    isLeaf(no2, t)
                    t = newToken()
                    if(t.type != 'ID'):
                        break
                else:
                    error(t, ';')
                    break
            else:
                error(t, 'TYPE')    
        else: #Jefferson, quero ver entender esse pedaço! HA HA HA
            if(t.type != 'PAREN_E'):
                error(t, ': ou (')
                break
            if(t.type == 'PAREN_E'):                
                no2 = Node('PAREN_E')
                no.addChild(no2)
                isLeaf(no2, t)
                t = newToken()
                if(t.type == 'ID'): #Aqui vai começar o FORMAL, por isso verifico se é um 'ID'
                    t = inFormal(t, no)#Provavelmente vai ter que ter um retorno t
                else:
                    if(t.type != 'PAREN_D'):
                        error(t, 'FORMAL do tipo: " ID : TYPE " ou )')
                if(t.type == 'PAREN_D'):
                    no2 = Node('PAREN_D')
                    no.addChild(no2)
                    isLeaf(no2, t)
                    t = newToken()
                    if(t.type == 'COLON'):
                        no2 = Node('COLON')
                        no.addChild(no2)
                        isLeaf(no2, t)
                        t = newToken()
                        if(t.type == 'TYPE' or t.type == 'SELF_TYPE'):
                            no2 = Node(t.type)
                            no.addChild(no2)
                            isLeaf(no2, t)
                            t = newToken()
                            if(t.type == 'CHAVE_E'):
                                no2 = Node('CHAVE_E')
                                no.addChild(no2)
                                isLeaf(no2, t)
                                t = newToken()
                                if(isExp(t)):#Se for verdadeiro, chama inExp
                                    t = inExp(t, no)#Provavelmente vai ter que ter um retorno t
                                    if(t.type == 'CHAVE_D'):
                                        no2 = Node('CHAVE_D')
                                        no.addChild(no2)
                                        isLeaf(no2, t)
                                        t = newToken()
                                        if(t.type == 'SEMICOLON'):
                                            no2 = Node('SEMICOLON')
                                            no.addChild(no2)
                                            isLeaf(no2, t)
                                            t = newToken()
                                            if(t.type != 'ID'):
                                                break
                                        else:
                                            error(t, ';')
                                    else:
                                        error(t, '}')
                                else: 
                                    error(t, 'EXPRESSÃO') 
                            else:
                                error(t, '{')
                                break
                        else:
                            error(t, 'TYPE')
                    else:
                        error(t, ':')
                else:
                    error(t, ')')
    return t
                

def isExp(t): #Método para verificar se um token é ou nao uma expressão - só pode ser usado em pontos específicos [?]
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
    if(t.type == 'SELF'):
        aux = True
    return aux
        
       
def inFormal(t, tree):#falta implementar
    while True:
        no = Node('FORMAL')
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
                if(t.type == 'COMMA'):
                    no2 = Node('COMMA')
                    no.addChild(no2)
                    isLeaf(no2, t)
                    t = newToken()
                    if(t.type != 'ID'):
                        error(t, 'ID')
                        break
                else:
                    if(t.type != 'PAREN_D'):
                        error(t, '" , " ou " ) "')
                        break 
            else:
                error(t, 'TYPE')
        else:
            error(t, ':')
        if(t.type == 'PAREN_D'):
            break
    return t

def inExp(t, tree, aux = None): 
    while True:
        no = Node('EXP')
        tree.addChild(no)
        if(t.type == 'SELF'):#SE FOR SELF
            no2 = Node('SELF')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            break
        if(t.type == 'TRUE'):#SE FOR TRUE
            no2 = Node('TRUE')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            break
        if(t.type == 'FALSE'):#SE FOR FALSE
            no2 = Node('FALSE')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            break
        if(t.type == 'STRING'):#SE FOR STRING
            no2 = Node('STRING')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            break
        if(t.type == 'NUMBER'):#SE FOR INTEGER
            no2 = Node('NUMBER')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            break
        if(t.type == 'NEW'):#SE FOR NEW
            no2 = Node('NEW')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            if(t.type == 'TYPE'):#SE FOR TYPE
                no2 = Node('TYPE')
                isLeaf(no2, t)
                no.addChild(no2)
                t = newToken()
            else:
                error(t, 'TYPE')
            break
        if(t.type == 'ID'):#SE FOR ID
            no2 = Node('ID')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            if(t.type == 'AT' or t.type == 'DOT'):#TESTANDO
                t = inExp2(t, no)
            if(t.type == 'ATRIB'):#SE FOR ATRIB
                no2 = Node('ATRIB')
                isLeaf(no2, t)
                no.addChild(no2)
                t = newToken()
                if(isExp(t)):
                    t = inExp(t, no)
                    t = inExp2(t, no)
                else:
                    error(t, 'EXPRESSÃO')
                    break
            if(t.type == 'PAREN_E'):#SE FOR PAREN_E
                no2 = Node('PAREN_E')
                isLeaf(no2, t)
                no.addChild(no2)
                t = newToken()
                while True:
                    if(isExp(t)):
                        t = inExp(t, no)
                        t = inExp2(t, no)
                        if(t.type == 'COMMA'):#SE FOR COMMA
                            no2 = Node('COMMA')
                            isLeaf(no2, t)
                            no.addChild(no2)
                            t = newToken()
                            if(not isExp(t)):
                                error(t, 'EXPRESSÃO')
                                break                                
                        else:
                            if(t.type != 'PAREN_D'):
                                error(t, ',')
                            break
                    else:
                        if(t.type != 'PAREN_D'):
                            error(t, 'EXPRESSÃO')
                        break
                if(t.type == 'PAREN_D'):#SE FOR PAREN_D
                    no2 = Node('PAREN_D')
                    isLeaf(no2, t)
                    no.addChild(no2)
                    t = newToken()
                else:
                    error(t, ')') # até aqui é se for ID                
            return t
        if(t.type == 'ISVOID'):#Se for isvoid
            no2 = Node('ISVOID')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            if(isExp(t)):
                t = inExp(t, no)
                t = inExp2(t, no)
                break
            else:
                error(t, 'EXPRESSÃO')
        if(t.type == 'TIL'):#Se for TIL
            no2 = Node('TIL')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            if(isExp(t)):
                t = inExp(t, no)
                t = inExp2(t, no)
                break
            else:
                error(t, 'EXPRESSÃO')
        if(t.type == 'NOT'):#Se for NOT
            no2 = Node('NOT')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            if(isExp(t)):
                t = inExp(t, no)
                t = inExp2(t, no)
                break
            else:
                error(t, 'EXPRESSÃO')
                break
        if(t.type == 'PAREN_E'):#Se for PAREN_E
            no2 = Node('PAREN_E')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            if(isExp(t)):
                t = inExp(t, no)
                t = inExp2(t, no)
                if(t.type == 'PAREN_D'):#Se for PAREN_E
                    no2 = Node('PAREN_D')
                    isLeaf(no2, t)
                    no.addChild(no2)
                    t = newToken()
                    break
                else:
                    error(t, ')')
                    break
            else:
                error(t, 'EXPRESSÃO')

        if(t.type == 'IF'):#SE FOR IF
            no2 = Node('IF')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            if(isExp(t)):
                t = inExp(t, no)
                t = inExp2(t, no)
            else:
                error(t, 'EXPRESSÃO')
                break
            if(t.type == 'THEN'):
                no2 = Node('THEN')
                isLeaf(no2, t)
                no.addChild(no2)
                t = newToken()
                if(isExp(t)):
                    t = inExp(t, no)
                    t = inExp2(t, no)
                else:
                    error(t, 'EXPRESSÃO')
                    break
                if(t.type == 'ELSE'):
                    no2 = Node('ELSE')
                    isLeaf(no2, t)
                    no.addChild(no2)
                    t = newToken()
                    if(isExp(t)):
                        t = inExp(t, no)
                        t = inExp2(t, no)
                    else:
                        error(t, 'EXPRESSÃO')
                        break
                    if(t.type == 'FI'):
                        no2 = Node('FI')
                        isLeaf(no2, t)
                        no.addChild(no2)
                        t = newToken()
                        break
                    else:
                        error(t, 'FI')
                else:
                    error(t, 'ELSE')
            else:
                error(t, 'THEN')
            break 
        if(t.type == 'WHILE'):#SE FOR WHILE
            no2 = Node('WHILE')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            if(isExp(t)):
                t = inExp(t, no)
                t = inExp2(t, no)#TESTANDO
            else:
                error(t, 'EXPRESSÃO')
                break
            if(t.type == 'LOOP'):
                no2 = Node('LOOP')
                isLeaf(no2, t)
                no.addChild(no2)
                t = newToken()
                if(isExp(t)):
                    t = inExp(t, no)
                    t = inExp2(t, no)#TESTANDO
                else:
                    error(t, 'EXPRESSÃO')
                    break
                if(t.type == 'POOL'):
                    no2 = Node('POOL')
                    isLeaf(no2, t)
                    no.addChild(no2)
                    t = newToken()
                    if(isExp(t)):
                        t = inExp(t, no)
                        t = inExp2(t, no)#TESTANDO
                    '''else:#TESTANDO SEM ISSO
                        error(t, 'EXPRESSÃO')
                        break'''
                else:
                    error(t, 'POOL')
            else:
                error(t, 'LOOP')
            break
        if(t.type == 'CASE'):#SE FOR CASE
            no2 = Node('CASE')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            if(isExp(t)):
                t = inExp(t, no)
                t = inExp2(t, no)#TESTANDO
            else:
                error(t, 'EXPRESSÃO')
                break
            if(t.type == 'OF'):
                no2 = Node('OF')
                isLeaf(no2, t)
                no.addChild(no2)
                t = newToken()
                while True:
                    if(t.type == 'ID'):
                        no2 = Node('ID')
                        isLeaf(no2, t)
                        no.addChild(no2)
                        t = newToken()
                        if(t.type == 'COLON'):
                            no2 = Node('COLON')
                            isLeaf(no2, t)
                            no.addChild(no2)
                            t = newToken()
                            if(t.type == 'TYPE'):
                                no2 = Node('TYPE')
                                isLeaf(no2, t)
                                no.addChild(no2)
                                t = newToken()
                                if(t.type == 'IMPLICA'):
                                    no2 = Node('IMPLICA')
                                    isLeaf(no2, t)
                                    no.addChild(no2)
                                    t = newToken()
                                    if(isExp(t)):
                                        t = inExp(t, no)
                                        t = inExp2(t, no)#TESTANDO
                                    else:
                                        error(t, 'EXPRESSÃO')
                                    if(t.type == 'SEMICOLON'):
                                        no2 = Node('SEMICOLON')
                                        isLeaf(no2, t)
                                        no.addChild(no2)
                                        t = newToken()
                                        if(t.type == 'ESAC'):
                                            no2 = Node('ESAC')
                                            isLeaf(no2, t)
                                            no.addChild(no2)
                                            t = newToken()
                                            break
                                        else:
                                            if(t.type != 'ID'):
                                                error(t, 'ESAC ou ID')
                                    else:
                                        error(t, ';')
                                else:
                                    error(t, '=>')                                   
                            else:
                                error(t, 'TYPE')
                        else:
                            error(t, ':')
                    else:
                        error(t, 'ID')
                        break
                break  

        if(t.type == 'LET'): #se for LET
            no2 = Node('LET')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            if(t.type == 'ID'):
                no2 = Node('ID')
                isLeaf(no2, t)
                no.addChild(no2)
                t = newToken()
                if(t.type == 'COLON'):
                    no2 = Node('COLON')
                    isLeaf(no2, t)
                    no.addChild(no2)
                    t = newToken()
                    if(t.type == 'TYPE'):
                        no2 = Node('TYPE')
                        isLeaf(no2, t)
                        no.addChild(no2)
                        t = newToken()
                        if(t.type == 'ATRIB'):
                            no2 = Node('ATRIB')
                            isLeaf(no2, t)
                            no.addChild(no2)
                            t = newToken()
                            if(isExp(t)):
                                t = inExp(t, no)
                                t = inExp2(t, no)
                            else:
                                error(t, 'EXPRESSÃO')
                                break
                        while True:
                            if(t.type == 'COMMA'):
                                no2 = Node('COMMA')
                                isLeaf(no2, t)
                                no.addChild(no2)
                                t = newToken()
                                if(t.type == 'ID'):
                                    no2 = Node('ID')
                                    isLeaf(no2, t)
                                    no.addChild(no2)
                                    t = newToken()
                                    if(t.type == 'COLON'):
                                        no2 = Node('COLON')
                                        isLeaf(no2, t)
                                        no.addChild(no2)
                                        t = newToken()
                                        if(t.type == 'TYPE'):
                                            no2 = Node('TYPE')
                                            isLeaf(no2, t)
                                            no.addChild(no2)
                                            t = newToken()
                                            if(t.type == 'ATRIB'):
                                                no2 = Node('ATRIB')
                                                isLeaf(no2, t)
                                                no.addChild(no2)
                                                t = newToken()
                                                if(isExp(t)):
                                                    t = inExp(t, no)
                                                    t = inExp2(t, no)#TESTANDO
                                                else:
                                                    error(t, 'EXPRESSÃO')
                                                    break
                                            if(t.type != 'COMMA'):
                                                break
                                        else:
                                            error(t, 'TYPE')
                                    else:
                                        error(t, ':')
                                else:
                                    error(t, 'ID')
                            else:
                                if(t.type != 'IN'):
                                    error(t, ',')
                                break

                        if(t.type == 'IN'):
                            no2 = Node('IN')
                            isLeaf(no2, t)
                            no.addChild(no2)
                            t = newToken()                
                            if(isExp(t)):
                                t = inExp(t, no)
                                t = inExp2(t, no)#TESTANDO
                                break
                            else:
                                error(t, 'EXPRESSÃO')
                                break
                        else:
                            error(t, 'IN')
                    else:
                        error(t, 'TYPE')
                else:
                    error(t, 'COLON')
            else:
                error(t, 'ID')
            break
        
        if(t.type == 'CHAVE_E'):# CASO {[EXP;]+}
            no2 = Node('CHAVE_E')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            while True:
                if(isExp(t)):
                    t = inExp(t, no)
                    '''if(t.type != 'SEMICOLON'):
                        error(t, ';')
                        break'''
                    t = inExp2(t, no)#TESTANDO
                    if(t.type == 'SEMICOLON'):#SE FOR SEMICOLON
                        no2 = Node('SEMICOLON')
                        isLeaf(no2, t)
                        no.addChild(no2)
                        t = newToken()
                        if(not isExp(t)):
                            if(t.type != 'CHAVE_D'):
                                error(t, 'EXPRESSÃO')#Depois de virgula tem que ser espressão
                                t = newToken()#Passa o token para nao dar looping infinito no erro ",;"
                                break   
                    else:
                        #if(t.type != 'CHAVE_D'):    <------------------------------------------------- Mudança recente
                            error(t, ';')
                            t = newToken()#Passa o token para nao dar looping infinito no erro ";,"
                            break
                        
                else:
                    if(t.type != 'CHAVE_D'):
                        error(t, 'EXPRESSÃO')
                    break
        if(t.type == 'CHAVE_D'):
            no2 = Node('CHAVE_D')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            break
        
        if(t.type == 'OP' or t.type == 'COMP'):#tenho que colocar na árvore?
            error(t, 'OPERADOR ou COMPARADOR não')
            t = newToken()
            break
        if(not isExp(t)):#GAMBIARRA!!! FUNCIONA???
            t = newToken()
            
    return t 


#TRATAMENTO DE RECURÇÃO À ESQUERDA
def inExp2(t , tree):
    cont = 0
    while True:
        if(t.type == 'OP'):
            no = Node('OP')
            isLeaf(no, t)
            tree.addChild(no)
            t = newToken()
            cont = cont + 1
            if(isExp(t)):
                t = inExp(t, tree)
            else:
                error(t, 'EXPRESSÃO')
                break
        elif(t.type == 'COMP'):
            no = Node('COMP')
            isLeaf(no, t)
            tree.addChild(no)
            t = newToken()
            cont = cont + 1
            if(isExp(t)):
                t = inExp(t, tree)
            else:
                error(t, 'EXPRESSÃO')
                break
            
        else:
            if(t.type == 'AT'):#Se for @
                no = Node('AT')
                isLeaf(no, t)
                tree.addChild(no)
                t = newToken()
                if(t.type == 'TYPE'):#Se for TYPE
                    no2 = Node('TYPE')
                    isLeaf(no2, t)
                    no.addChild(no2)
                    t = newToken()
                else:
                    error(t, 'TYPE')
                    break
            if(t.type == 'DOT'):#Se for DOT
                no = Node('DOT')
                isLeaf(no, t)
                tree.addChild(no)
                t = newToken()
                if(t.type == 'ID'):#Se for ID
                    t = inExp(t, no)
                    break
                else:
                    error(t, 'ID')
            else:
                break
        
    return t
        
def printChildren(tree, cont):
    for i in tree.children:
        print(i.data)
        cont = printChildren(i, cont + 1)        
    return cont

def tprint():
    cont = 0
    print(tree.data)
    cont = printChildren(tree, 0)
    print("\n\n A árvore tem %d nós" % cont)

#========================================================================================================    
                      
#Aqui começa o equivalente a Main, vulgo: MEIN INERITS AIOOOOU!!!!!    
aux = 0#Isso tinha um propósito, ainda descobrirei qual... kkkk
tree = Node('PROGRAM')
#t1 = newToken()
while True: #loop infinito
    t = newToken()
    if(not end(t)): #enquanto nao chegar ao final dos tokens
        if(t.type == 'CLASS'):
            inClass(t,tree)
        else:
            aux = aux + 1
            if(aux < 10):
                error(t, 'ERROR')
    else: #Se chegou ao fim dos tokens então break pra sair do loop infinito
        break

print("\n\n============= COMPILADO ============= ")#ACABOU 
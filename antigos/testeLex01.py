 # ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex

# List of token names.   This is always required

reserved = {
   'if': 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'int' : 'INT',
   'float' : 'FLOAT',
   'class' : 'CLASS',
   'fi' : 'FI',
   'loop' : 'LOOP',
   'pool' : 'POOL',
   'false' : 'FALSE',
   'in' : 'IN',
   'inherits' : 'INHERITS',
   'isvoid' : 'ISVOID',
   'let' : 'LET',
   'case' : 'CASE',
   'esac' : 'ESAC',
   'new' : 'NEW',
   'of' : 'OF',
   'not' : 'NOT',
   'true' : 'TRUE',
      
}

tokens = [
   'NUMBER',
   'LPAREN',
   'RPAREN',
   'EQUAL',
   'ID',
   'ERROR',
   'OP',
   'LOE',
   'HOE',
   'LOGOP',
   'QUOTE',
   'STRING',
   'DEFINE',
   'EXTEN',

] + list(reserved.values())

#Tratamento geral dos simbolos em tokens
def t_ID(t):
    r'[a-zA-z][a-zA-Z_0-9]*'
    aux = 0;
    if (((t.value.lower() != 'true') and (t.value.lower() != 'false'))):
        aux = in_reserved(t,aux)
        if((aux == 0) and (isUPPER(t.value) or t.value[0] == '_')):
            t.type = 'ERROR'
            return t
        else:
            t.type = reserved.get(t.value.lower(),'ID')
            return t
    else:
        if ((t.value[0] == 't' and t.value.lower() == 'true')):
            t.type = reserved.get(t.value.lower(),'ID')
            return t
        else:
            if((t.value[0] == 'f' and t.value.lower() == 'false')):
                t.type = reserved.get(t.value.lower(),'ID')
                return t
    aux = 0
    t.type = 'ERROR'
    return t

# Regular expression rules for simple tokens
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_OP = r'[-+\*/]'
t_LOE = r'[<]+[=]' #Menor ou igual - Lower Or Equal
t_HOE = r'[>]+[=]' #Maior ou igual - Higher Or Equal
t_LOGOP = r'[<>!=]'
t_QUOTE = r'"'
t_STRING = r'\"([^\\\n]|(\\.))*?\"' #Pega tudo entre " "
t_DEFINE = r':' #TEM QUE VER SE É ISSO MESMO
t_EXTEN = r'\.' #TEM QUE VER SE É ISSO MESMO

#áàâãéèêíìóòôõúùç <--- Caso Precise

#Verifica se a palavra esta na lista de reservadas
def in_reserved (t, aux):
    for word in list(reserved.values()):
        if (t.value.lower() == word.lower()):
            aux = aux+1
    return aux

#Verifica se o caracter é maiusculo
def isUPPER(x):
    return 'A' <= x <= 'Z'

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
def t_code_comment(t):
    r'(\(\*(.|\n)*?\*\))|(--.*)'
    pass

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out
data = '''
3 + 4 = 10
  + -20 *2
  2<3
  5<=8
  7>=6
  2=>6
  "teste"
  ""teste
  "test!%#//--"
  "teste""
  oi"oi"oi"oi.¬¬
  (*0teste
  tes0te
  teste0
  teste 0
  -- no cool dos outros é refresco
  Z
  A a
  AAAA
  int a
  a.a
  case
  CAse
  a_a*)
  _a
  true
  True
  tRue
  false
  fasle
  False
  fALSE
  tFALSE
  FALSE
  TREU
  TRUE
  class
  Class
  CLasS
  if
  IF
  iF
  If
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)


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
   #'int' : 'INT',
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
   #'SELF_TYPE' : 'SELF_TYPE',
   #'self' : 'SELF',
}

types = {
    'Int' : 'TYPE',
    'Bool': 'TYPE',
    'SELF_TYPE' : 'SELF_TYPE',
    'self' : 'SELF',
}

tokens = [
   'NUMBER',
   'ID',
   'ERROR',
   #'TYPE',
   'OP',
   'COMP',
   'ATRIB',
   'LOGOP',
   'QUOTE',
   'STRING',
   'DOISPONTOS',
   'EXTEN',
   'PONTO',
   'ARROBA',
   'TIL',
   'PV',
   'CHAVES_E',
   'CHAVES_D',
   'PAREN_E',
   'PAREN_D',
   'COLCH_E',
   'COLCH_D',
   'VIRGULA',

] + list(reserved.values()) + list(types.values())

#Tratamento geral dos simbolos em tokens
def t_ID(t):
    r'[a-zA-z][a-zA-Z_0-9]*'
    if ((t.value.lower() != 'true') and (t.value.lower() != 'false')):
        if(t.value[0] == '_'):
            t.type = 'ERROR'
            return t
        if(in_types(t)):
            t.type = types.get(t.value,'ID')
            return t
        if((not in_reserved(t)) and t.value[0].isupper()):
            t.type = 'TYPE'
            return t
        '''if((t.value.lower() == 'self' and t.value[0].isupper())):
            t.type = 'TYPE'
            return t'''
        t.type = reserved.get(t.value,'ID')
        return t
    else:
        if (t.value[0] == 't' and t.value.lower() == 'true'):
            t.type = reserved.get(t.value.lower(),'ID')
            return t
        else:
            if(t.value[0] == 'f' and t.value.lower() == 'false'):
                t.type = reserved.get(t.value.lower(),'ID')
                return t
    t.type = 'TYPE'
    return t

# Regular expression rules for simple tokens

t_OP = r'[-+\*/]'
t_COMP = r'<=|=|<'
t_LOGOP = r'not'
t_ATRIB = r'<-'                    
t_QUOTE = r'"'
t_STRING = r'(\"(.|\\\n)*?\")' #Pega tudo entre " "
t_DOISPONTOS = r':'
t_PONTO = r'\.'
t_ARROBA = r'\@'
t_TIL = r'\~'
t_PV = r'\;'
t_CHAVES_E = r'\{'
t_CHAVES_D = r'\}'
t_PAREN_E  = r'\('
t_PAREN_D  = r'\)'
t_COLCH_E = r'\['
t_COLCH_D = r'\]'
t_VIRGULA = r'\,'
#áàâãéèêíìóòôõúùç <--- Caso Precise

#Verifica se a palavra esta na lista de reservadas
def in_reserved (t):
    for word in list(reserved.values()):
        if (t.value.lower() == word.lower()):
            return True
    return False

def in_types (t):
    for word in list(types):
        #print (word)
        if (t.value == word):
            return True
    return False

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
Aa
Int int
self
SELF_TYPE
Self
sELF_TYPE
SELF_type
[(
[AAA]
aA
aa
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
  If*)
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)


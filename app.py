from flask import Flask, render_template, request
import ply.lex as lex
import ply.yacc as yacc

app = Flask(__name__)

# List of token names
tokens = [
    'ID', 'NUMBER', 'STRING_LITERAL',
    'PLUS', 'EQUAL', 'OPEN_PAREN', 'CLOSE_PAREN',
    'OPEN_BRACE', 'CLOSE_BRACE', 'COMMA', 'SEMICOLON',
    'DOT', 'LBRACKET', 'RBRACKET', 'PRINTLN', 'FOR', 'LT', 'PLUSPLUS'
]

# Reserved words
reserved = {
    'public': 'PUBLIC',
    'class': 'CLASS',
    'static': 'STATIC',
    'void': 'VOID',
    'main': 'MAIN',
    'String': 'STRING',
    'int': 'INT',
    'for': 'FOR',
    'System.out.println': 'PRINTLN'
}

tokens = tokens + list(reserved.values())

# Token regex definitions
t_PLUS = r'\+'
t_EQUAL = r'='
t_OPEN_PAREN = r'\('
t_CLOSE_PAREN = r'\)'
t_OPEN_BRACE = r'\{'
t_CLOSE_BRACE = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'
t_DOT = r'\.'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LT = r'<'
t_PLUSPLUS = r'\+\+'
t_STRING_LITERAL = r'\"([^\\\n]|(\\.))*?\"'
t_ignore = ' \t\n\r'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Yacc Parsing rules
def p_program(p):
    '''program : PUBLIC CLASS ID OPEN_BRACE main_method CLOSE_BRACE'''
    p[0] = ('program', p[3], p[5])

def p_main_method(p):
    '''main_method : PUBLIC STATIC VOID MAIN OPEN_PAREN STRING LBRACKET RBRACKET ID CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE'''
    p[0] = ('main_method', p[11])

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : println_statement
                 | for_statement'''
    p[0] = p[1]

def p_println_statement(p):
    '''println_statement : PRINTLN OPEN_PAREN STRING_LITERAL CLOSE_PAREN SEMICOLON'''
    p[0] = ('println', p[3])

def p_for_statement(p):
    '''for_statement : FOR OPEN_PAREN INT ID EQUAL NUMBER SEMICOLON ID LT NUMBER SEMICOLON ID PLUSPLUS CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE'''
    p[0] = ('for', p[4], p[6], p[9], p[11], p[13], p[16])

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
        raise SyntaxError(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")
        raise SyntaxError("Syntax error at EOF")

parser = yacc.yacc()

# Semantic analysis
def semantic_analysis(parsed_code):
    declared_variables = set()
    errors = []

    def check_statement(statement):
        if statement[0] == 'for':
            _, var_name, init_val, cond_var, cond_val, inc_var, body = statement
            if var_name != cond_var or cond_var != inc_var:
                errors.append(f"Semantic error: Variable '{var_name}' is used inconsistently in the for loop")
            if var_name in declared_variables:
                errors.append(f"Semantic error: Variable '{var_name}' is redeclared in the for loop")
            declared_variables.add(var_name)
            for stmt in body:
                check_statement(stmt)
        elif statement[0] == 'println':
            _, string_literal = statement
            # No semantic checks needed for println in this context

    for stmt in parsed_code:
        check_statement(stmt)

    return errors

@app.route('/', methods=['GET', 'POST'])
def index():
    counters = {tok: 0 for tok in tokens}
    counters.update({val: 0 for val in reserved.values()})
    token_data = []
    lexical_errors = []
    syntax_errors = []
    semantic_errors = []
    syntax_correct = False
    code = ''
    if request.method == 'POST':
        code = request.form.get('code', '')
        lexer.input(code)
        while True:
            tok = lexer.token()
            if not tok:
                break
            entry = {'token': tok.value, 'PR': '', 'ID': '', 'SIM': '', 'ERROR': ''}
            if tok.type in reserved.values():
                entry['PR'] = 'X'
            elif tok.type == 'ID':
                entry['ID'] = 'X'
            elif tok.type == 'PRINTLN':
                entry['PR'] = 'X'
            elif tok.type == 'ERROR':
                entry['ERROR'] = 'X'
                lexical_errors.append(f"Error Léxico: '{tok.value}'")
            else:
                entry['SIM'] = 'X'
            counters[tok.type] += 1
            token_data.append(entry)

        # Syntax analysis
        try:
            parsed_code = parser.parse(code, lexer=lexer)
            syntax_correct = True
            # Semantic analysis
            semantic_errors = semantic_analysis(parsed_code)
        except SyntaxError as e:
            syntax_errors.append(str(e))

    total_reserved = sum(counters[val] for val in reserved.values())
    total_errors = counters['ERROR'] if 'ERROR' in counters else 0

    return render_template("index.html", token_data=token_data, counters=counters, total_reserved=total_reserved,
                           lexical_errors=lexical_errors, total_errors=total_errors, syntax_errors=syntax_errors,
                           semantic_errors=semantic_errors, syntax_correct=syntax_correct, code=code)

if __name__ == "__main__":
    app.run(debug=True)
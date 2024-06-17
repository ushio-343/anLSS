from flask import Flask, request, render_template, jsonify
import ply.lex as lex
import ply.yacc as yacc

app = Flask(__name__)

# Definición del lexer
tokens = (
    'INT', 'SEMICOLON', 'ID', 'EQUALS', 'NUMBER', 'FOR', 'LPAREN', 'RPAREN',
    'LT', 'GT', 'LE', 'GE', 'EQ', 'NE', 'PLUSPLUS', 'LBRACE', 'RBRACE', 'PRINTLN'
)

t_ignore = ' \t'
t_SEMICOLON = r';'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_PLUSPLUS = r'\+\+'

def t_INT(t):
    r'int'
    return t

def t_FOR(t):
    r'for'
    return t

def t_PRINTLN(t):
    r'System\.out\.println'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

# Definición del parser
variables = set()
errors = []
syntax_errors = []

def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : declaration
                 | for_loop
                 | block
                 | println'''
    p[0] = p[1]

def p_declaration(p):
    '''declaration : INT ID SEMICOLON'''
    var_name = p[2]
    if var_name in variables:
        errors.append(f"Línea {p.lineno(1)}: La variable '{var_name}' ya está declarada.")
    else:
        variables.add(var_name)

def p_for_loop(p):
    '''for_loop : FOR LPAREN assignment SEMICOLON condition SEMICOLON increment RPAREN block'''
    var_name = p[3][0]
    if p[3][1] not in variables:
        errors.append(f"Línea {p.lineno(1)}: La variable '{p[3][1]}' usada en la asignación no está declarada.")
    if p[5][0] not in variables:
        errors.append(f"Línea {p.lineno(1)}: La variable '{p[5][0]}' usada en la condición no está declarada.")
    if p[7][0] not in variables:
        errors.append(f"Línea {p.lineno(1)}: La variable '{p[7][0]}' usada en el incremento no está declarada.")
    if var_name != p[5][0] or var_name != p[7][0]:
        errors.append(f"Línea {p.lineno(1)}: La variable usada en la estructura for no es consistente.")

def p_assignment(p):
    '''assignment : ID EQUALS NUMBER'''
    p[0] = (p[1], p[1])

def p_condition(p):
    '''condition : ID LT NUMBER
                 | ID GT NUMBER
                 | ID LE NUMBER
                 | ID GE NUMBER
                 | ID EQ NUMBER
                 | ID NE NUMBER'''
    p[0] = (p[1], p[1])

def p_increment(p):
    '''increment : ID PLUSPLUS'''
    p[0] = (p[1], p[1])

def p_block(p):
    '''block : LBRACE statement_list RBRACE'''
    p[0] = p[2]

def p_println(p):
    '''println : PRINTLN LPAREN ID RPAREN SEMICOLON'''
    var_name = p[3]
    if var_name not in variables:
        errors.append(f"Línea {p.lineno(1)}: La variable '{var_name}' usada en println no está declarada.")
    else:
        p[0] = True

def p_error(p):
    if p:
        syntax_errors.append(f"Error de sintaxis en '{p.value}' en la línea {p.lineno}")
    else:
        syntax_errors.append("Error de sintaxis al final del archivo")

parser = yacc.yacc()

def perform_lexical_analysis(code):
    lexer.input(code)
    token_list = []
    totals = {'Reservada': 0, 'Identificador': 0, 'Número': 0, 'Símbolo': 0, 'Error': 0}
    while True:
        tok = lexer.token()
        if not tok:
            break
        category = categorize_token(tok.type)
        token_list.append({
            'value': tok.value,
            'type': tok.type,
            'category': category
        })
        totals[category] += 1
    return token_list, totals

def categorize_token(token_type):
    if token_type in ['INT', 'FOR', 'PRINTLN']:
        return 'Reservada'
    elif token_type == 'ID':
        return 'Identificador'
    elif token_type == 'NUMBER':
        return 'Número'
    elif token_type in ['SEMICOLON', 'EQUALS', 'LPAREN', 'RPAREN', 'LT', 'GT', 'LE', 'GE', 'EQ', 'NE', 'PLUSPLUS', 'LBRACE', 'RBRACE']:
        return 'Símbolo'
    else:
        return 'Error'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    global variables, errors, syntax_errors
    code = request.form['code']
    if not code:
        return jsonify({"error": "No se proporcionó código"}), 400

    variables = set()
    errors = []
    syntax_errors = []
    lexer.lineno = 1

    token_list, totals = perform_lexical_analysis(code)
    parser.parse(code)

    if not errors and not syntax_errors:
        return jsonify({"message": "El código es correcto", "lexical": token_list, "totals": totals, "syntax_errors": []}), 200
    else:
        return jsonify({"errors": errors, "lexical": token_list, "totals": totals, "syntax_errors": syntax_errors}), 200

if __name__ == '__main__':
    app.run(debug=True)

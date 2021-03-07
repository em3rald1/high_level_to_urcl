def cr(a):
    na = []
    for i in a:
        if i != '': na.append(i)
    return na

def split(s):
    n = ''
    t = []
    inc = False
    for c in s:
        if c == '\n':
            inc = False
        if inc:
            continue
        if c == ' ':
            if n != '':
                t.append(n)
            n = ''
        elif c == ';':
            if n != '':
                t.append(n)
            t.append(c)
            n = ''
        elif c == '/':
            if n == '/':
                inc = True
            else:
                if n != '':
                    t.append(n)
                n = '/'
        elif c == '+':
            if n == '+':
                t.append('++')
                n = ''
            else:
                t.append(n)
                n = "+"
        elif c == '-':
            if n == '-':
                t.append('--')
                n = ''
            else:
                t.append(n)
                n = '-'
        elif c == '=':
            if n == '+':
                t.append('+=')
                n = ''
            elif n == '-':
                t.append('-=')
                n = ''
            elif n == '=':
                t.append('==')
                n = ''
            else:
                if n != '':
                    t.append(n)
                n = '='
        elif c == '(':
            if n != '':
                t.append(n)
            t.append('(')
            n = ''
        elif c == ')':
            if n != "":
                t.append(n)
            t.append(')')
            n = ''
        elif c == ',':
            if n != '':
                t.append(n)
           #t.append(',')
            n = ''
        elif c=='\n':
            if n!='':
                t.append(n)
            n = ''
        elif c == '<':
            if n != '':
                t.append(n)
            t.append('<')
            n = ''
        elif c == '>':
            if n != '':
                t.append(n)
            t.append('>')
            n = ''
        else:
            if n == '=':
                t.append(n)
                n = ''
            n += c
    if n != '': t.append(n)
    return cr(t)

def tk(d, t): return [d, t]

def throw(en, em):
    print(f'Unexpected {en} occured!: {em}')
    exit(1)

class Lexer:
    def __init__(self, s):
        self.s = s
        self.output = []
        self.cti = -1
    def f(self):
        self.cti+=1
        return self.s[self.cti]
    def l(self):
        d = self.f()
        while True:
            if d == 'int':
                # declare integer ( 16 bit )
                var_name = self.f()
                if var_name.isascii() and not var_name.isnumeric():
                    eqs = self.f()
                    if eqs == '=':
                        data = self.f()
                        if data.isnumeric():
                            try:
                                semi_colon = self.f()
                            except IndexError:
                                throw('syntax_error', f'no semi-colon! [ {d} {var_name} = {data} ]')
                            if semi_colon == ';':
                                self.output.append(tk('INT_DECLARE', [var_name, data]))
                            else:
                                throw('syntax_error', f'no semi-colon! [ {d} {var_name} = {data} ]')
                        elif data.startswith('*'):
                            # int* data
                            try:
                                semi_colon = self.f()
                            except IndexError:
                                throw ('syntax_error', f'no semi-colon! [ {d} {var_name} = {data} ]')
                            if semi_colon == ';':
                                self.output.append(tk('INT_DECLARE_INT_PTR_READ', [var_name, data[1:]]))
                            else:
                                throw ('syntax_error', f'no semi-colon! [ {d} {var_name} = {data} ]')
                        else:
                            semi_colon = self.f()
                            if semi_colon == ';':
                                self.output.append(tk('INT_DECLARE_VAR', [var_name, data]))
                            elif semi_colon == '(':
                                args = []
                                #t2 = self.f()
                                d2 = self.f()
                                while d2 != ')':
                                    args.append(d2)
                                    #t2 = self.f()
                                    d2 = self.f()
                                self.output.append(tk('INT_DECLARE_FUNCTION_CALL', [var_name, data, args]))
                            else:
                                throw('syntax_error', f'no semi-colon! [ {d} {var_name} = {data} ]')
                    elif eqs == '(':
                        # int fuckme(int x) {}
                        args = []
                        at1 = self.f()
                        an1 = self.f()
                        while at1 != ')':
                            args.append([at1, an1])
                            at1 = self.f()
                            try:
                                an1 = self.f()
                            except IndexError: break
                        self.output.append(tk('INT_FUNCTION_DEC', [var_name, args]))
            elif d == 'char':
                var_name = self.f()
                if var_name.isascii() and not var_name.isnumeric():
                    eqs = self.f()
                    if eqs == '=':
                        data = self.f()
                        if data.isnumeric():
                            try:
                                semi_colon = self.f()
                            except IndexError:
                                throw('syntax_error', f'no semi-colon! [ {d} {var_name} = {data} ]')
                            if semi_colon == ';':
                                self.output.append(tk("CHAR_DECLARE", [var_name, str(int(data) & 0xff)]))
                            else:
                                throw('syntax_error', f'no semi-colon! [ {d} {var_name} = {data} ]')
                        elif data.startswith('\'') and data.endswith('\'') and len(data) == 3:
                            chdata = ord(data[1:-1])
                            try:
                                semi_colon = self.f()
                            except IndexError:
                                throw('syntax_error', f'no semi-colon! [ {d} {var_name} = {data} ]')
                            if semi_colon == ';':
                                self.output.append(tk('CHAR_DECLARE', [var_name, str(int(chdata) & 0xff)]))
                            else:
                                throw('syntax_error', f'no semi-colon! [ {d} {var_name} = {data} ]')
                        else:
                            try:
                                semi_colon = self.f()
                            except IndexError:
                                throw('syntax_error', f'no semi-colon! [ {d} {var_name} = {data} ]')
                            if semi_colon == ';':
                                self.output.append(tk('CHAR_DECLARE_VAR', [var_name, data]))
                            elif semi_colon == '(':
                                args = []
                                #t2 = self.f()
                                d2 = self.f()
                                while d2 != ')':
                                    args.append(d2)
                                    #t2 = self.f()
                                    d2 = self.f()
                                self.output.append(tk('CHAR_DECLARE_FUNCTION_CALL', [var_name, data, args]))
                            else:
                                throw('syntax_error', f'no semi-colon! [ {d} {var_name} = {data} ]')
                    elif eqs == '(':
                        # int fuckme(int x) {}
                        args = []
                        at1 = self.f()
                        an1 = self.f()
                        while at1 != ')':
                            args.append([at1, an1])
                            at1 = self.f()
                            try:
                                an1 = self.f()
                            except IndexError: break
                        self.output.append(tk('CHAR_FUNCTION_DEC', [var_name, args]))
            elif d == 'int*':
                var_name = self.f()
                if var_name.isascii():
                    eqs = self.f()
                    if eqs == '=':
                        data = self.f()
                        if data.startswith('&'):
                            try:
                                semi_colon = self.f()
                            except IndexError:
                                throw('syntax_error', f'no semi-colon! [ {d} {var_name} = {data} ]')
                            if semi_colon == ';':
                                self.output.append(tk('INT_POINTER_DECLARE_VAR_REF', [var_name, data]))
                            else:
                                throw('syntax_error', f'no semi-colon! [ {d} {var_name} = {data} ]')
                        elif data.isnumeric():
                            try:
                                semi_colon = self.f()
                            except IndexError:
                                throw('syntax_error', f'no semi-colon! [ {d} {var_name} = {data} ]')
                            if semi_colon == ';':
                                self.output.append(tk('INT_POINTER_DECLARE_ADDR', [var_name, data]))
                            else:
                                throw('syntax_error', f'no semi-colon! [ {d} {var_name} = {data} ]')
                        elif data.isascii():
                            try:
                                semi_colon = self.f()
                            except IndexError:
                                throw('syntax_error', f'no semi-colon! [ {d} {var_name} = {data} ]')
                            if semi_colon == ';':
                                self.output.append(tk('INT_POINTER_DECLARE_ADDR_IN_VAR', [var_name, data]))
                            elif semi_colon == '(':
                                args = []
                                #t2 = self.f()
                                d2 = self.f()
                                while d2 != ')':
                                    args.append(d2)
                                    #t2 = self.f()
                                    d2 = self.f()
                                self.output.append(tk('INT_PTR_DECLARE_FUNCTION_CALL', [var_name, data, args]))
                    elif eqs == '(':
                        # int fuckme(int x) {}
                        args = []
                        at1 = self.f()
                        an1 = self.f()
                        while at1 != ')':
                            args.append([at1, an1])
                            at1 = self.f()
                            try:
                                an1 = self.f()
                            except IndexError: break
                        self.output.append(tk('INT_PTR_FUNCTION_DEC', [var_name, args]))
            elif d == 'bool':
                var_name = self.f()
                if var_name.isascii():
                    d2 = self.f()
                    if d2 == '=':
                        # var assignment
                        data = self.f()
                        if data == 'true' or data == 'false':
                            semi_colon = self.f()
                            if semi_colon == ';':
                                self.output.append(tk('BOOL_DECLARE', [var_name, 1 if data == 'true' else 0]))
                        else:
                            semi_colon = self.f()
                            if semi_colon == ';':
                                self.output.append(tk('BOOL_DECLARE_VAR', [var_name, data]))
                            elif semi_colon == '(':
                                args = []
                                t1 = self.f()
                                while t1 != ')':
                                    args.append(t1)
                                    t1 = self.f()
                                semi_colon2 = self.f()
                                if semi_colon2 == ';':
                                    self.output.append(tk('BOOL_DECLARE_FUNCTION_CALL', [var_name, data, args]))
                            elif semi_colon == '==':
                                d3 = self.f()
                                if d3.isnumeric():
                                    if data.isnumeric():
                                        self.output.append(tk('BOOL_DECLARE_EQ_II', [var_name, d3, data]))
                                    else:
                                        self.output.append(tk('BOOL_DECLARE_EQ_IV', [var_name, d3, data]))
                                else:
                                    if data.isnumeric():
                                        self.output.append(tk('BOOL_DECLARE_EQ_VI', [var_name, d3, data]))
                                    else:
                                        self.output.append(tk('BOOL_DECLARE_EQ_VV', [var_name, d3, data]))
                            elif semi_colon == '>':
                                d3 = self.f()
                                if d3.isnumeric():
                                    if data.isnumeric():
                                        self.output.append(tk('BOOL_DECLARE_GR_II', [var_name, d3, data]))
                                    else:
                                        self.output.append(tk('BOOL_DECLARE_GR_IV', [var_name, d3, data]))
                                else:
                                    if data.isnumeric():
                                        self.output.append(tk('BOOL_DECLARE_GR_VI', [var_name, d3, data]))
                                    else:
                                        self.output.append(tk('BOOL_DECLARE_GR_VV', [var_name, d3, data]))
                            elif semi_colon == '<':
                                d3 = self.f()
                                if d3.isnumeric():
                                    if data.isnumeric():
                                        self.output.append(tk('BOOL_DECLARE_LS_II', [var_name, d3, data]))
                                    else:
                                        self.output.append(tk('BOOL_DECLARE_LS_IV', [var_name, d3, data]))
                                else:
                                    if data.isnumeric():
                                        self.output.append(tk('BOOL_DECLARE_LS_VI', [var_name, d3, data]))
                                    else:
                                        self.output.append(tk('BOOL_DECLARE_LS_VV', [var_name, d3, data]))
                    elif d2 == '(':
                        args = []
                        t3 = self.f()
                        d3 = self.f()
                        while t3 != ")":
                            args.append([t3,d3])
                            t3 = self.f()
                            try:
                                d3 = self.f()
                            except IndexError:
                                break
                        self.output.append(tk('BOOL_FUNCTION_DECLARE', [var_name, args]))
            elif d == 'return':
                data = self.f()
                tmp_k = self.f()
                if data.isnumeric():
                    self.output.append(tk('LITERAL_RETURN_STATEMENT', [data]))
                elif tmp_k == '(':
                    args = []
                    d1 = self.f()
                    while d1 != ')':
                        args.append(d1)
                        d1 = self.f()
                    self.output.append(tk('FUNCTION_CALL_RETURN_STATEMENT', [data, args]))
                elif tmp_k == ';':
                    self.cti -= 1
                    #self.output.append(tk('VAR_RETURN_STATEMENT', [data]))
                    if data.startswith('&'):
                        self.output.append(tk('VAR_PTR_RETURN_STATEMENT', [data[1:]]))
                    elif data == 'false' or data == 'true':
                        self.output.append(tk('LITERAL_RETURN_STATEMENT', [1 if data == 'true' else 0]))
                    else:
                        self.output.append(tk('VAR_RETURN_STATEMENT', [data]))
            elif d.startswith('#'):
                if d[1:] == 'include':
                    path = self.f()
                    if path.startswith('"'):
                        if not path.endswith('"'):
                            while not path.endswith('"'):
                                path += self.f()
                        self.output.append(tk('INCLUDE_STATEMENT', [path[1:-1]]))
            elif d.startswith('}'):
                #fname = self.f()
                self.output.append(tk('END_FUNCTION', []))
            elif d.isascii() and not d.startswith('*'):
                op = self.f()
                print(d, op)
                if op == ';' or d == ';': 
                    self.cti -= 1
                elif op == '++':
                    self.output.append(tk('INCREMENT_INT', [d]))
                elif op == '--':
                    self.output.append(tk('DECREMENT_INT', [d]))
                elif op == '+=':
                    d2 = self.f()
                    if d2.isnumeric():
                        self.output.append(tk('ADD_IN_PLACE_INT_INT', [d, d2]))
                    elif d2 == '(':
                        typCast = self.f()
                        if typCast.isascii():
                            cb = self.f()
                            if cb == ')':
                                d3 = self.f()
                                if d3.isnumeric():
                                    self.output.append(tk('ADD_IN_PLACE_INT_INT_CASTED', [d, typCast, d3]))
                                else:
                                    self.output.append(tk('ADD_IN_PLACE_INT_VAR_CASTED', [d, typCast, d3]))
                    else:
                        self.output.append(tk('ADD_IN_PLACE_INT_VAR', [d, d2]))
                elif op == '-=':
                    d2 = self.f()
                    if d2.isnumeric():
                        self.output.append(tk('SUB_IN_PLACE_INT_INT', [d,d2]))
                    elif d2 == '(':
                        typCast = self.f()
                        if typCast.isascii():
                            cb = self.f()
                            if cb == ')':
                                d3 = self.f()
                                if d3.isnumeric():
                                    self.output.append(tk('SUB_IN_PLACE_INT_INT_CASTED', [d, typCast, d3]))
                                else:
                                    self.output.append(tk('SUB_IN_PLACE_INT_VAR_CASTED', [d, typCast, d3]))
                    else:
                        self.output.append(tk('SUB_IN_PLACE_INT_VAR', [d,d2]))
                elif op == '=':
                    d2 = self.f()
                    if d2.isnumeric():
                        self.output.append(tk('REASSIGN_INT', [d, d2]))
                    elif d2 == '(':
                        typCast = self.f()
                        if typCast.isascii():
                            cb = self.f()
                            if cb == ')':
                                d3 = self.f()
                                if d3.isnumeric():
                                    self.output.append(tk('REASSIGN_INT_CASTED', [d, typCast, d3]))
                                else:
                                    self.output.append(tk('REASSIGN_VAR_CASTED', [d, typCast, d3]))
                    else:
                        self.output.append(tk('REASSIGN_VAR', [d, d2]))
            try:
                d = self.f()
            except IndexError:
                return self.output
        return self.output

VAROFF = 0x200

class Compiler:
    def __init__(self, lex, d=True):
        self.l = lex
        self.cti = -1
        #self.output = 'CAL .main\n'
        self.output = ('CAL .clear_memory\nCAL .main\nHLT\n' if d else '')
        self.after_out = (".clear_memory\nIMM R1, 400\n._clear__iter__\nSTR R1, 0\nADD R1, R1, 1\nCMP R1, 65535\nBNZ ._clear__iter__\nRET\n" if d else '')
        self.vars = {}
        self.funcs = {}
        self.cf = []
        self.off = 0
    def p(self, ln):
        self.output += ln + '\n'
    def p2(self, ln):
        self.output += ln + '\n'
    def f(self):
        self.cti += 1
        return self.l[self.cti]
    def c(self):
        d = self.f()
        while True:
            if d[0] == 'INCLUDE_STATEMENT':
                data1 = open(d[1][0], 'r').read()
                data2 = split(data1)
                data3 = Lexer(data2).l()
                #print(data3)
                data4 = Compiler(data3, False).c()
                #print(f'Fuck me:{data4[0]}')
                #print(data4[1:])
                self.vars.update(data4[1])
                self.funcs.update(data4[2])
                self.after_out += data4[0]
            # integer_declarations
            if d[0] == 'INT_DECLARE':
                if d[1][0] in self.vars:
                    throw('compile_error', f'variable {d[1][0]} already exist!')
                self.vars[d[1][0]] = ['int', self.off]
                self.p(f'STR {VAROFF+self.off}, {d[1][1]}')
                self.off += 1
            elif d[0] == 'INT_DECLARE_VAR':
                if d[1][0] in self.vars:
                    throw('compile_error', f'variable {d[1][0]} already exist!')
                self.vars[d[1][0]] = ['int', self.off]
                self.p(f'LOD R1, {VAROFF+self.vars[d[1][1]][1]}')
                self.p(f'STR {VAROFF+self.off}, R1')
                self.off+=1
            elif d[0] == 'INT_DECLARE_FUNCTION_CALL':
                if d[1][0] in self.vars:
                    throw('compile_error', f'variable {d[1][0]} already exist!')
                elif not self.funcs[d[1][1]][0] == 'int':
                    throw('compile_error', f'function {d[1][1]} return type isn\'t \'int\'')
                self.vars[d[1][0]] = ['int', self.off]
                for param in d[1][2]:
                    if param.isnumeric():
                        self.p(f'PSH {param}')
                    else:
                        self.p(f'LOD R1, {VAROFF+self.vars[param][1]}')
                        self.p(f'PSH R1')
                self.p(f'CAL .{d[1][1]}')
                self.p(f'STR {VAROFF+self.off}, R1')
                self.off+=1
            elif d[0] == 'INT_FUNCTION_DEC':
                if d[1][0] in self.funcs:
                    throw('compile_error', f'function {d[1][0]} already exist!')
                self.funcs[d[1][0]] = ['int', d[1][1]]
                self.p(f'.{d[1][0]}')
                self.cf.append(d[1][0])
                for param in d[1][1]:
                    if param[0] == 'int':
                        self.vars[param[1]] = ['int', self.off]
                        self.p(f'POP R1')
                        self.p(f'STR {VAROFF+self.off}, R1')
                        self.off+=1
            elif d[0] == 'VAR_RETURN_STATEMENT':
                #if self.funcs[self.cf][0] == 'int':
                self.p(f'LOD R1, {VAROFF+self.vars[d[1][0]][1]}')
                self.p(f'RET')
            elif d[0] == 'LITERAL_RETURN_STATEMENT':
                self.p(f'IMM R1, {d[1][0]}')
                self.p(f'RET')
            elif d[0] == 'REASSIGN_INT':
                if not d[1][0] in self.vars:
                    throw('compile_error', f'variable {d[1][0]} doesn\'t exist!')
                self.p(f'STR {VAROFF+self.vars[d[1][0]][1]}, {d[1][1]}')
            elif d[0] == 'REASSIGN_VAR':
                if not d[1][0] in self.vars:
                    throw('compile_error', f'variable {d[1][0]} doesn\'t exist!')
                elif not d[1][1] in self.vars:
                    throw('compile_error', f'variable {d[1][1]} doesn\'t exist!')
                self.p(f'LOD R1, {VAROFF+self.vars[d[1][1]][1]}')
                self.p(f'STR {VAROFF+self.vars[d[1][0]][1]}, R1')
            elif d[0] == 'CHAR_DECLARE':
                self.vars[d[1][0]] = ['char', self.off]
                self.p(f'STR {VAROFF+self.off}, {int(d[1][1]) & 0xff}')
            elif d[0] == 'CHAR_DECLARE_VAR':
                if not d[1][1] in self.vars:
                    throw('compile_error', f'variable {d[1][1]} doesn\'t exist!')
                if self.vars[d[1][1]][0] != 'char':
                    throw('compile_error', f'variable {d[1][1]} type isn\'t \'char\'')
                self.vars[d[1][0]] = ['char',self.off]
                self.p(f'LOD R1, {VAROFF+self.vars[d[1][1]][1]}')
                self.p(f'STR {VAROFF+self.off}, R1')
                self.off+=1
            elif d[0] == 'CHAR_DECLARE_FUNCTION_CALL':
                if self.funcs[d[1][1]][0] != 'char':
                    throw('compile_error', f'function {d[1][1]} return type isn\'t \'char\'')
                self.vars[d[1][0]] = ['char', self.off]
                for p in d[1][2]:
                    if p.isnumeric():
                        self.p(f'PSH {p}')
                    else:
                        if not p in self.vars:
                            throw('compile_error', f'variable {p} doesn\'t exist! (threw while calling {d[1][1]})')
                        self.p(f'LOD R1, {VAROFF+self.vars[p][1]}')
                        self.p(f'PSH R1')
                self.p(f'CAL .{d[1][1]}')
                self.p(f'STR {VAROFF+self.off}, R1')
                self.off+=1
            elif d[0] == 'CHAR_FUNCTION_DEC':
                if d[1][0] in self.funcs:
                    throw('compile_error', f'function {d[1][0]} already exists!')
                self.funcs[d[1][0]] = ['char', d[1][1]]
                self.p(f'.{d[1][0]}')
                self.cf.append(d[1][0])
                for p in d[1][1]:
                    print(p)
                    self.vars[p[1]] = [p[0], self.off]
                    print(self.vars)
                    self.p(f'POP R1')
                    self.p(f'STR {VAROFF+self.off}, R1')
                    self.off+=1
            elif d[0] == 'ADD_IN_PLACE_INT_INT':
                if not d[1][0] in self.vars:
                    throw('compile_error', f'variable {d[1][0]} doesn\'t exist')
                self.p(f'LOD R1, {VAROFF+self.vars[d[1][0]][1]}')
                self.p(f'ADD R1, R1, {d[1][1]}')
                self.p(f'STR {VAROFF+self.vars[d[1][0]][1]}, R1')
            elif d[0] == 'SUB_IN_PLACE_INT_INT':
                if not d[1][0] in self.vars:
                    throw('compile_error', f'variable {d[1][0]} doesn\'t exist')
                self.p(f'LOD R1, {VAROFF+self.vars[d[1][0]][1]}')
                self.p(f'SUB R1, R1, {d[1][1]}')
                self.p(f'STR {VAROFF+self.vars[d[1][0]][1]}, R1')
            elif d[0] == 'ADD_IN_PLACE_INT_VAR':
                if not d[1][0] in self.vars:
                    throw('compile_error', f'variable {d[1][0]} doesn\'t exist')
                elif not d[1][1] in self.vars:
                    throw('compile_error', f'variable {d[1][1]} doesn\'t exist')
                elif self.vars[d[1][0]][0] != self.vars[d[1][1]][0]:
                    throw('compile_error', f'variable types aren\'t the same')
                self.p(f'LOD R1, {VAROFF+self.vars[d[1][0]][1]}')
                self.p(f'LOD R2, {VAROFF+self.vars[d[1][1]][1]}')
                self.p(f'ADD R1, R1, R2')
                self.p(f'STR {VAROFF+self.vars[d[1][0]][1]}, R1')
            elif d[0] == 'SUB_IN_PLACE_INT_VAR':
                if not d[1][0] in self.vars:
                    throw('compile_error', f'variable {d[1][0]} doesn\'t exist')
                elif not d[1][1] in self.vars:
                    throw('compile_error', f'variable {d[1][1]} doesn\'t exist')
                elif self.vars[d[1][0]][0] != self.vars[d[1][1]][0]:
                    throw('compile_error', f'variable types aren\'t the same')
                self.p(f'LOD R1, {VAROFF+self.vars[d[1][0]][1]}')
                self.p(f'LOD R2, {VAROFF+self.vars[d[1][1]][1]}')
                self.p(f'SUB R1, R1, R2')
                self.p(f'STR {VAROFF+self.vars[d[1][0]][1]}, R1')
            elif d[0] == 'SUB_IN_PLACE_INT_VAR_CASTED':
                if not d[1][0] in self.vars:
                    throw('compile_error', f'variable {d[1][0]} doesn\'t exist')
                elif not d[1][2] in self.vars:
                    throw('compile_error', f'variable {d[1][2]} doesn\'t exist')
                elif self.vars[d[1][0]][0] == self.vars[d[1][2]][0]:
                    throw('compile_error', f'variable\'s {d[1][0]} type equals to type of variable {d[1][2]}')
                elif not d[1][1] == self.vars[d[1][0]][0]:
                    throw('compile_error', f'casting to wrong type ({d[1][1]})')
                self.p(f'LOD R1, {VAROFF+self.vars[d[1][0]][1]}')
                self.p(f'LOD R2, {VAROFF+self.vars[d[1][2]][1]}')
                self.p(f'SUB R1, R1, R2')
                self.p(f'STR {VAROFF+self.vars[d[1][0]][1]}, R1')
            elif d[0] == 'ADD_IN_PLACE_INT_VAR_CASTED':
                if not d[1][0] in self.vars:
                    throw('compile_error', f'variable {d[1][0]} doesn\'t exist')
                elif not d[1][2] in self.vars:
                    throw('compile_error', f'variable {d[1][2]} doesn\'t exist')
                elif self.vars[d[1][0]][0] == self.vars[d[1][2]][0]:
                    throw('compile_error', f'variable\'s {d[1][0]} type equals to type of variable {d[1][2]}')
                elif not d[1][1] == self.vars[d[1][0]][0]:
                    throw('compile_error', f'casting to wrong type ({d[1][1]})')
                self.p(f'LOD R1, {VAROFF+self.vars[d[1][0]][1]}')
                self.p(f'LOD R2, {VAROFF+self.vars[d[1][2]][1]}')
                self.p(f'ADD R1, R1, R2')
                self.p(f'STR {VAROFF+self.vars[d[1][0]][1]}, R1')
            elif d[0] == 'REASSIGN_VAR_CASTED':
                if not d[1][0] in self.vars:
                    throw('compile_error', f'variable {d[1][0]} doesn\'t exist')
                elif not d[1][2] in self.vars:
                    throw('compile_error', f'variable {d[1][0]} doesn\'t exist')
                elif d[1][1] == self.vars[d[1][2]][0]:
                    throw('compile_error', f'variable {d[1][0]} casted wrongly ({d[1][1]})')
                elif d[1][1] != self.vars[d[1][0]][0]:
                    throw('compile_error', f'cast is wrong ({d[1][1]})')
                self.p(f'LOD R1, {VAROFF+self.vars[d[1][2]][1]}')
                self.p(f'STR {VAROFF+self.vars[d[1][0]][1]}, R1')
            elif d[0] == 'BOOL_FUNCTION_DECLARE':
                if d[1][0] in self.funcs:
                    throw('compile_error', f'function {d[1][0]} already exist')
                self.funcs[d[1][0]] = ['bool', d[1][1]]
                self.p(f'.{d[1][0]}')
                for param in d[1][1]:
                    self.vars[param[1]] = [param[0], self.off]
                    self.p(f'POP R1')
                    self.p(f'STR {VAROFF+self.off}, R1')
                    self.off+=1
                self.cf.append(d[1][0])
            elif d[0] == 'BOOL_DECLARE_FUNCTION_CALL':
                self.vars[d[1][0]] = ['bool', self.off]
                for p in d[1][2]:
                    if p.isnumeric():
                        self.p(f'PSH {p}')
                    else:
                        self.p(f'LOD R1, {VAROFF+self.vars[p][1]}')
                        self.p(f'PSH R1')
                self.p(f'CAL .{d[1][1]}')
                self.p(f'STR {VAROFF+self.off}, R1')
                self.off+=1
            elif d[0] == 'BOOL_DECLARE_EQ_II':
                self.vars[d[1][0]] = ['bool', self.off]
                self.p(f'SUB R1, {d[1][1]}, {d[1][2]}')
                self.p(f'CMP R1, 0')
                self.p(f'BNZ .not_z{self.off}')
                self.p(f'STR {VAROFF+self.off}, 1')
                self.p(f'BRA .continue{self.off}')
                self.p(f'.not_z{self.off}')
                self.p(f'STR {VAROFF+self.off}, 0')
                self.p(f'.continue{self.off}')
                self.off+=1
            elif d[0] == 'BOOL_DECLARE_EQ_IV':
                self.vars[d[1][0]] = ['bool', self.off]
                self.p(f'LOD R2, {VAROFF+self.vars[d[1][2]][1]}')
                self.p(f'SUB R1, {d[1][1]}, R2')
                self.p(f'CMP R1, 0')
                self.p(f'BNZ .not_z{self.off}')
                self.p(f'STR {VAROFF+self.off}, 1')
                self.p(f'BRA .continue{self.off}')
                self.p(f'.not_z{self.off}')
                self.p(f'STR {VAROFF+self.off}, 0')
                self.p(f'.continue{self.off}')
                self.off+=1
            elif d[0] == 'BOOL_DECLARE_EQ_VI':
                self.vars[d[1][0]] = ['bool', self.off]
                self.p(f'LOD R2, {VAROFF+self.vars[d[1][1]][1]}')
                self.p(f'SUB R1, R2, {d[1][2]}')
                self.p(f'CMP R1, 0')
                self.p(f'BNZ .not_z{self.off}')
                self.p(f'STR {VAROFF+self.off}, 1')
                self.p(f'BRA .continue{self.off}')
                self.p(f'.not_z{self.off}')
                self.p(f'STR {VAROFF+self.off}, 0')
                self.p(f'.continue{self.off}')
                self.off+=1
            elif d[0] == 'BOOL_DECLARE_EQ_VV':
                self.vars[d[1][0]] = ['bool', self.off]
                self.p(f'LOD R2, {VAROFF+self.vars[d[1][1]][1]}')
                self.p(f'LOD R3, {VAROFF+self.vars[d[1][2]][1]}')
                self.p(f'SUB R1, R2, R3')
                self.p(f'CMP R1, 0')
                self.p(f'BNZ .not_z{self.off}')
                self.p(f'STR {VAROFF+self.off}, 1')
                self.p(f'BRA .continue{self.off}')
                self.p(f'.not_z{self.off}')
                self.p(f'STR {VAROFF+self.off}, 0')
                self.p(f'.continue{self.off}')
                self.off+=1
                
            elif d[0] == 'END_FUNCTION':
                print(self.cf)
                self.cf.pop()
            try:
                d = self.f()
            except IndexError:
                return self.output + self.after_out, self.vars, self.funcs, self.cf

        
import sys
data = split(open(sys.argv[1], 'r').read())
print(data)

data2 = Lexer(data).l()
print(data2)

data3 = Compiler(data2).c()
print(data3[0])
print(data3[1])
print(data3[2])
print(data3[3])

open(sys.argv[2], 'w').write(data3[0])
def cr(a):
    na = []
    for i in a:
        if i != '': na.append(i)
    return na

def split(s):
    n = ''
    t = []
    for c in s:
        if c == ' ':
            if n != '':
                t.append(n)
            n = ''
        elif c == ';':
            if n != '':
                t.append(n)
            t.append(c)
            n = ''
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
                                self.output.append(tk('CHAR_DECLARE_VAR', [var_name, str(int(data) & 0xff)]))
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
                    else:
                        self.output.append(tk('VAR_RETURN_STATEMENT', [data]))
            elif d.startswith('}'):
                #fname = self.f()
                self.output.append(tk('END_FUNCTION', []))
            elif d.isascii():
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
                    else:
                        self.output.append(tk('ADD_IN_PLACE_INT_VAR', [d, d2]))
                elif op == '-=':
                    d2 = self.f()
                    if d2.isnumeric():
                        self.output.append(tk('SUB_IN_PLACE_INT_INT', [d,d2]))
                    else:
                        self.output.append(tk('SUB_IN_PLACE_INT_VAR', [d,d2]))
            try:
                d = self.f()
            except IndexError:
                return self.output
        return self.output

VAROFF = 0x200

class Compiler:
    def __init__(self, lex):
        self.l = lex
        self.cti = -1
        #self.output = 'CAL .main\n'
        self.output = 'CAL .main\nHLT\n'
        self.after_out = ''
        self.vars = {}
        self.funcs = {}
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
            if d[0] == 'INT_DECLARE':
                self.vars[d[1][0]] = self.off
                self.p(f'STR {VAROFF+self.off}, {d[1][1]}')
                self.off += 2
            elif d[0] == 'INT_DECLARE_VAR':
                if not d[1][1] in self.vars.keys():
                    throw('compile_error', f'variable {d[1][1]} doesn\'t exist')
                else:
                    self.vars[d[1][0]] = self.off
                    self.p(f'LOD R1, {VAROFF+self.vars[d[1][1]]}')
                    self.p(f'STR {VAROFF+self.off}, R1')
                    self.off += 2
            elif d[0] == 'INT_DECLARE_FUNCTION_CALL':
                #if not d[1][1] in self.funcs:
                #    throw('compile_error', f'function {d[1][1]} doesn\'t exist')
                
                for param in d[1][2]:
                    if param.isnumeric():
                        self.p(f'PSH {param}')
                    else:
                        self.p(f'LOD R1, {VAROFF+self.vars[param]}')
                        self.p(f'PSH R1')
                self.p(f'CAL .{d[1][1]}')
                self.vars[d[1][0]] = self.off
                self.p(f'STR {VAROFF+self.vars[d[1][0]]}, R1')
                self.off+=2
            elif d[0] == 'INT_FUNCTION_DEC':
                self.funcs[d[1][0]] = d[1][1]
                self.p(f'.{d[1][0]}')
                for param in d[1][1]:
                    self.vars[param[1]] = self.off
                    self.p(f'POP R1')
                    self.p(f'STR {VAROFF+self.off}, R1')
                    self.off += 2
            elif d[0] == 'INCREMENT_INT':
                self.p(f'LOD R1, {VAROFF+self.vars[d[1][0]]}')
                self.p(f'ADD R1, R1, 1')
                self.p(f'STR {VAROFF+self.vars[d[1][0]]}, R1')
            elif d[0] == 'DECREMENT_INT':
                self.p(f'LOD R1, {VAROFF+self.vars[d[1][0]]}')
                self.p(f'SUB R1, R1, 1')
                self.p(f'STR {VAROFF+self.vars[d[1][0]]}, R1')
            elif d[0] == 'ADD_IN_PLACE_INT_INT':
                self.p(f'LOD R1, {VAROFF+self.vars[d[1][0]]}')
                self.p(f'ADD R1, R1, {d[1][1]}')
                self.p(f'STR {VAROFF+self.vars[d[1][0]]}, R1')
            elif d[0] == 'SUB_IN_PLACE_INT_INT':
                self.p(f'LOD R1, {VAROFF+self.vars[d[1][0]]}')
                self.p(f'SUB R1, R1, {d[1][1]}')
                self.p(f'STR {VAROFF+self.vars[d[1][0]]}, R1')
            elif d[0] == 'ADD_IN_PLACE_INT_VAR':
                self.p(f'LOD R1, {VAROFF+self.vars[d[1][0]]}')
                self.p(f'LOD R2, {VAROFF+self.vars[d[1][1]]}')
                self.p(f'ADD R1, R1, R2')
                self.p(f'STR {VAROFF+self.vars[d[1][0]]}, R1')
            elif d[0] == 'SUB_IN_PLACE_INT_VAR':
                self.p(f'LOD R1, {VAROFF+self.vars[d[1][0]]}')
                self.p(f'LOD R2, {VAROFF+self.vars[d[1][1]]}')
                self.p(f'SUB R1, R1, R2')
                self.p(f'STR {VAROFF+self.vars[d[1][0]]}, R1')
            elif d[0] == 'LITERAL_RETURN_STATEMENT':
                self.p(f'IMM R1, {d[1][0]}')
                self.p('RET')
            elif d[0] == "VAR_RETURN_STATEMENT":
                self.p(f'LOD R1, {VAROFF+self.vars[d[1][0]]}')
                self.p(f'RET')
            
            try:
                d = self.f()
            except IndexError:
                return self.output + self.after_out

        
import sys
data = split(open(sys.argv[1], 'r').read())
print(data)

data2 = Lexer(data).l()
print(data2)

data3 = Compiler(data2).c()
print(data3)
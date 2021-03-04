OP1_MATH_OPS = ['+', '-']
OP2_MATH_OPS = ['+=', '-=']
LOAD_OP = '='
CMP_OP = '=='

def clear_array(a):
    na = []
    for i in a:
        if i != '':
            na.append(i)
    return na

def tokenize(st):
    nss = ''
    tokens = []
    incomment = False
    for ch in st:
        if ch == '\n':
            incomment = False
        if incomment:
            continue
        if ch == ' ' and (nss != '' and nss != ' '):
            tokens.append(nss)
            nss = ''
        elif ch == '+':
            if nss == '+':
                tokens.append('++')
                nss = ''
            else:
                tokens.append(nss)
                nss = ''
                nss += '+'
        elif ch == ';':
            incomment = True
            tokens.append(nss)
            nss = ''
        elif ch == ',':
            tokens.append(nss)
            nss = ''
        elif ch == '(':
            if nss != '':
                tokens.append(nss)
            tokens.append('(')
            nss = ''
        elif ch == ')':
            if nss != '':
                tokens.append(nss)
            tokens.append(')')
            nss = ''
        elif ch == '-':
            if nss == '-':
                tokens.append('--')
                nss = ''
            else:
                tokens.append(nss)
                nss += '-'
        elif ch == '=':
            if nss == '-':
                tokens.append('-=')
                nss = ''
            elif nss == '+':
                tokens.append('+=')
                nss = ''
            elif nss == '=':
                tokens.append('==')
                nss = ''
            else:
                nss += '='
        elif ch == '\n':
            #print(1)
            tokens.append(nss)
            incomment = False
            nss = ''
        else:
            if ch != ' ' and ch != '':
                nss += ch
    if nss != '':
        tokens.append(nss.strip())
    return clear_array(tokens)



def tok(d, i):
    return [d, i]

def only_num(d):
    return d.isnumeric()

class Lexer:
    def __init__(self,tokens=[]):
        self.tokens = tokens
        self.output = []
        self.cti = -1
    def f(self):
        self.cti += 1
        return self.tokens[self.cti]
    def l(self):
        ct = self.f()
        while True:
            if ct == '_retq':
                self.output.append(tok('HALT', []))
            elif ct == 'call':
                d2 = self.f()
                if d2.isascii() and not d2.isnumeric():
                    d3 = self.f()
                    args = []
                    if d3 == '(':
                        d4 = self.f()
                        #print()
                        while d4 != ')':
                            args.append(d4)
                            d4 = self.f()
                        nargs = []
                        for i in args:
                            if i.endswith(','): nargs.append(i[:-1])
                            else: nargs.append(i)
                    #self.cti -= 1
                        self.output.append(tok("CALL FUNCTION", [d2, nargs]))
            elif ct == 'cycle':
                d2 = self.f()
                if d2 == '(':
                    d3 = self.f()
                    if d3.isnumeric():
                        d4 = self.f()
                        if d4 == ')':
                            lbl = self.f()
                            args = []
                            d5 = self.f()
                            if d5 == '(':
                                d5 = self.f()
                                while d5 != ')':
                                    args.append(d5)
                                    d5 = self.f()
                                self.output.append(tok('CYCLE', [d3,lbl, args]))
            elif ct == 'return':
                d2 = self.f()
                if d2.isascii() and not d2.isnumeric():
                    self.output.append(tok("RETURN_VAR", [d2]))
                elif d2.isnumeric():
                    self.output.append(tok('RETURN_INT', [d2]))
            elif ct.isascii() and not ct.isnumeric():
                d2 = self.f()
                #print(ct, d2, self.tokens[self.cti+1])
                if d2 == '=':
                    d3 = self.f()
                    #if d3.isnumeric():
                    self.output.append(tok('ASSIGNMENT_INT', [ct, d3]))
                elif d2 == '(':
                    args = []
                    d4 = self.f()
                        #print()
                    while d4 != ')':
                        args.append(d4)
                        d4 = self.f()
                    nargs = []
                    for i in args:
                        if i.endswith(','): nargs.append(i[:-1])
                        else: nargs.append(i)
                    #self.cti -= 1
                    self.output.append(tok("CALL FUNCTION", [ct, nargs]))
                elif d2 == '+=':
                    d3 = self.f()
                    #if d3.isnumeric():
                    self.output.append(tok('ADD_IN_PLACE', [ct, d3]))
                elif d2 == '-=':
                    d3 = self.f()
                    #if d3.isnumeric():
                    self.output.append(tok("SUB_IN_PLACE", [ct,d3]))
                elif d2 == '++':
                    #d3 = self.f()
                    #if d3.isnumeric():
                    self.output.append(tok('INCREMENT', [ct]))
                elif d2 == '--':
                    #d3 = self.f()
                    #if d3.isnumeric():
                    self.output.append(tok('DECREMENT', [ct]))

               # print(ct,d2)
                elif ct == 'def':
                    tmp = d2
                    #print(ct, d2)
                    d2 = self.f()
                #print(d2)
                    if d2.isascii() and not d2.isnumeric():
                       #d3 = self.f()
                        #rint(ct, d2, d3)
                        if d2 == '(':
                            d4 = self.f()
                            #print(ct, d2, d4)
                            args = []
                            while d4 != ')':
                                args.append(d4)
                                d4 = self.f()
                            #print(args)
                            nargs =[]
                            for i in args:
                                if i.endswith(','):
                                    nargs.append(i[:-1])
                                else: nargs.append(i)
                            self.output.append(tok('FUNCTION_DECLARE', [tmp, nargs]))
            try:
                ct =self.f()
            except IndexError:
                return self.output

VAR_OFFSET = 0x400

class Compiler:
    def __init__(self, lexems=[]):
        self.lex = lexems
        self.output = 'BITS == 16\nMINRAM == 4096\nMINREGS == 10\n'
        self.off = 0
        self.cti = -1
        self.vars = {}
        self.after_out = ''
    def f(self):
        self.cti += 1
        return self.lex[self.cti]
    def var(self, val, nm):
        self.vars[nm] = self.off
        self.p(f'IMM R1, {val}')
        self.p(f'STR {VAR_OFFSET+self.off}, R1')
        self.off += 4
    def p(self, ln):
        self.output += ln + "\n"
    def p2(self, ln):
        self.after_out += ln +'\n'
    def c(self):
        ct = self.f()
        while True:
            if ct[0] == 'ASSIGNMENT_INT':
                #self.p(f'PUSH R1')
                if ct[1][1].isnumeric():
                    if not ct[1][0] in self.vars.keys():
                        self.var(ct[1][1], ct[1][0])
                    else:
                        self.p(f'IMM R1, {ct[1][1]}')
                        self.p(f'STR {VAR_OFFSET+self.vars[ct[1][0]]}, R1')
                else:
                    if not ct[1][0] in self.vars.keys():
                        self.vars[ct[1][0]] = self.off
                        self.p(f'LOD R1, {VAR_OFFSET+self.vars[ct[1][1]]}')
                        self.p(f'STR {VAR_OFFSET+self.off}, R1')
                        self.off += 4
                    else:
                        self.p(f'LOD R1, {VAR_OFFSET+self.vars[ct[1][1]]}')
                        self.p(f'STR {VAR_OFFSET+self.vars[ct[1][0]]}, R1')
                #self.p(f"POP R1")
            elif ct[0] == 'FUNCTION_DECLARE':
                self.p(f'.{ct[1][0]}')
                for i in ct[1][1]:
                    self.vars[i] = self.off
                    self.p('POP R1')
                    self.p(f'STR {VAR_OFFSET+self.off}, R1')
                    self.off += 4
            elif ct[0] == 'HALT':
                self.p('HLT')
            elif ct[0] == 'CALL FUNCTION':
                for arg in ct[1][1]:
                    if arg.isnumeric():
                        self.p(f'PSH {arg}')
                    else:
                        self.p(f'LOD R1, {VAR_OFFSET+self.vars[arg]}')
                        self.p(f'PSH R1')
                self.p(f'CAL .{ct[1][0]}')
            elif ct[0] == 'RETURN_INT':
                self.p(f'IMM R1, {ct[1][0]}')
                self.p('RET')
            elif ct[0] == 'RETURN_VAR':
                self.p(f'LOD R1, {VAR_OFFSET+self.vars[ct[1][0]]}')
                self.p('RET')
            elif ct[0] == 'ADD_IN_PLACE':
                if ct[1][1].isnumeric():
                    self.p(f'LOD R1, {VAR_OFFSET+self.vars[ct[1][0]]}')
                    self.p(f'ADD R1, R1, {ct[1][1]}')
                    self.p(f'STR {VAR_OFFSET+self.vars[ct[1][0]]}, R1')
                else:
                    self.p(f'LOD R1, {VAR_OFFSET+self.vars[ct[1][0]]}')
                    self.p(f'LOD R2, {VAR_OFFSET+self.vars[ct[1][1]]}')
                    self.p(f'ADD R1, R1, R2')
                    self.p(f'STR {VAR_OFFSET+self.vars[ct[1][0]]}, R1')
            elif ct[0] == 'SUB_IN_PLACE':
                if ct[1][1].isnumeric():
                    self.p(f'LOD R1, {VAR_OFFSET+self.vars[ct[1][0]]}')
                    self.p(f'SUB R1, R1, {ct[1][1]}')
                    self.p(f'STR {VAR_OFFSET+self.vars[ct[1][0]]}, R1')
                else:
                    self.p(f'LOD R1, {VAR_OFFSET+self.vars[ct[1][0]]}')
                    self.p(f'LOD R2, {VAR_OFFSET+self.vars[ct[1][1]]}')
                    self.p(f'SUB R1, R1, R2')
                    self.p(f'STR {VAR_OFFSET+self.vars[ct[1][0]]}, R1')
            elif ct[0] == 'INCREMENT':
                self.p(f'LOD R1, {VAR_OFFSET+self.vars[ct[1][0]]}')
                self.p(f'ADD R1, R1, 1')
                self.p(f'STR {VAR_OFFSET+self.vars[ct[1][0]]}, R1')
            elif ct[0] == 'DECREMENT':
                self.p(f'LOD R1, {VAR_OFFSET+self.vars[ct[1][0]]}')
                self.p(f'SUB R1, R1, 1')
                self.p(f'STR {VAR_OFFSET+self.vars[ct[1][0]]}, R1')
            elif ct[0] == 'CYCLE':
                self.p(f'CAL .prep_{ct[1][1]}_{ct[1][0]}')
                self.p2(f'.prep_{ct[1][1]}_{ct[1][0]}')
                self.p2(f'IMM R3, {ct[1][0]}')
                self.p2(f'._{ct[1][1]}_cycle')
                for i in ct[1][2]:
                    if i.isnumeric():
                        self.p2(f'PSH {i}')
                    else:
                        self.p2(f'LOD R1, {VAR_OFFSET+self.vars[i]}')
                        self.p2('PSH R1')
                self.p2(f'CAL .{ct[1][1]}')
                self.p2(f'DEC R3, R3')
                self.p2(f'CMP R3, 0')
                self.p2(f'BNZ ._{ct[1][1]}_cycle')
                self.p2(f'.end')
                self.p2('RET')
            try:
                ct = self.f()
            except IndexError:
                return self.output+self.after_out, self.vars
import sys
dat = open(sys.argv[1], 'r').read()
toks = tokenize(dat)
d = Lexer(toks).l()
print(d)
c = Compiler(d)
d2 = c.c()
print(d2[0])
print(d2[1])

with open(sys.argv[2], 'w') as f:
    f.write(d2[0])
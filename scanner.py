from pprint import pprint
import re
import collections

ID      = r'(?P<ID>[a-zA-Z][a-zA-Z0-9]*)'
NUM     = r'(?P<NUM>\d+)'
OP      = r'(?P<OP>[+\-*^])'
LPAREN  = r'(?P<LPAREN>\()'
RPAREN  = r'(?P<RPAREN>\))'
WS      = r'(?P<WS>\s+)'

master_pattern = re.compile('|'.join((ID, NUM, OP, LPAREN, RPAREN, WS)))
Token = collections.namedtuple('Token', ['type', 'value'])

def generate_tokens(text, pattern=master_pattern):
    scanner = pattern.scanner(text)
    tokens = [Token(m.lastgroup, m.group()) for m in iter(scanner.match, None)]
    return tokens

inputs = ["42", "(app   43 44)", "(lam hello (app hello hello))", "(lam x (app y (add1 (sub1 (iszero (+ 2 (- 3 (* hello (^ 33 44)))))))))", "(^ (-0 2) (-0 5))", "blah", "(app (+ 2 3) 4)", "(iszero 2)", "(iszero 0)", "(app (lam x x) 3)", "(app (app (app (app (lam x (app x x)) (lam f (lam n (lam a (lam b (app (app n (lam m (app (app (app (app f f) m) a) (app a b)))) b)))))) (lam s (lam z (app s (lam s (lam z z)))))) (lam x (+ x 1))) 5)", "(lam z (app (lam x (app x x)) (lam x (app x x))))"]

outputs = ["NUM(42)", "Lparen, ID(app), WS, NUM(43), WS, NUM(44), Rparen", "Lparen, ID(lam), WS, ID(hello), WS, Lparen, ID(app), WS, ID(hello), WS, ID(hello), Rparen, Rparen ", "Lparen, ID(lam), WS, ID(x), WS, Lparen, ID(app), WS, ID(y), WS, Lparen, ID(add1), WS, Lparen, ID(sub1), WS, Lparen, ID(iszero), WS, Lparen, OP(+), WS, NUM(2), WS, Lparen, OP(-), WS, NUM(3), WS, Lparen, OP(*), WS, ID(hello), WS, Lparen, OP(^), WS, NUM(33), WS, NUM(44), Rparen, Rparen, Rparen, Rparen, Rparen, Rparen, Rparen, Rparen, Rparen", "Lparen, OP(^), WS, Lparen, OP(-), NUM(0), WS, NUM(2), Rparen, WS, Lparen, OP(-), NUM(0), WS, NUM(5), Rparen, Rparen", "ID(blah)", "Lparen, ID(app), WS, Lparen, OP(+), WS, NUM(2), WS, NUM(3), Rparen, WS, NUM(4), Rparen", "Lparen, ID(iszero), WS, NUM(2), Rparen", "Lparen, ID(iszero), WS, NUM(0), Rparen", "Lparen, ID(app), WS, Lparen, ID(lam), WS, ID(x), WS, ID(x), Rparen, WS, NUM(3), Rparen", "Lparen, ID(app), WS, Lparen, ID(app), WS, Lparen, ID(app), WS, Lparen, ID(app), WS, Lparen, ID(lam), WS, ID(x), WS, Lparen, ID(app), WS, ID(x), WS, ID(x), Rparen, Rparen, WS, Lparen, ID(lam), WS, ID(f), WS, Lparen, ID(lam), WS, ID(n), WS, Lparen, ID(lam), WS, ID(a), WS, Lparen, ID(lam), WS, ID(b), WS, Lparen, ID(app), WS, Lparen, ID(app), WS, ID(n), WS, Lparen, ID(lam), WS, ID(m), WS, Lparen, ID(app), WS, Lparen, ID(app), WS, Lparen, ID(app), WS, Lparen, ID(app), WS, ID(f), WS, ID(f), Rparen, WS, ID(m), Rparen, WS, ID(a), Rparen, WS, Lparen, ID(app), WS, ID(a), WS, ID(b), Rparen, Rparen, Rparen, Rparen, WS, ID(b), Rparen, Rparen, Rparen, Rparen, Rparen, Rparen, WS, Lparen, ID(lam), WS, ID(s), WS, Lparen, ID(lam), WS, ID(z), WS, Lparen, ID(app), WS, ID(s), WS, Lparen, ID(lam), WS, ID(s), WS, Lparen, ID(lam), WS, ID(z), WS, ID(z), Rparen, Rparen, Rparen, Rparen, Rparen, Rparen, WS, Lparen, ID(lam), WS, ID(x), WS, Lparen, OP(+), WS, ID(x), WS, NUM(1), Rparen, Rparen, Rparen, WS, NUM(5), Rparen", "Lparen, ID(lam), WS, ID(z), WS, Lparen, ID(app), WS, Lparen, ID(lam), WS, ID(x), WS, Lparen, ID(app), WS, ID(x), WS, ID(x), Rparen, Rparen, WS, Lparen, ID(lam), WS, ID(x), WS, Lparen, ID(app), WS, ID(x), WS, ID(x), Rparen, Rparen, Rparen, Rparen"]

def pprint_scanner_output(tokens,i,per_line=False):
    buf = []
    for token in tokens:
        if token.type in ['LPAREN','RPAREN','WS'] : 
            buf.append(token.type)
        else: 
            buf.append(token.type+'('+token.value+')')
    if per_line:
        print(',\n'.join(buf))
    else:
        print("Our output:     ",', '.join(buf))
        print("Expected output:",outputs[i].upper())

for i,inp in enumerate(inputs):
    print("Input:   ",inp)
    output_tokens = generate_tokens(inp, master_pattern)
    pprint_scanner_output(output_tokens,i)
    print()


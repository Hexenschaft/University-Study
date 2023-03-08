# -----------------------------------------------------------
# performing operations over logical expressions
# -----------------------------------------------------------
#
# current implementation deals with logical expressions
# as computation graphs and performs some operations,
# such as computation of truth table, PCNF, PDNF and
# minimization of logical functions
#
# I admit that this implementation isn't perfect and may
# contain some issues, otherwise it can be helpful
# as example or even backbone for designing similar
# systems
#
# -----------------------------------------------------------
# Released under MIT License
# (C) Alexander Isaychikov, Minsk, Belarus
# email isaychikov.ai@yahoo.com
# -----------------------------------------------------------

from src.Variable import *
from src.operations import *

if __name__ == '__main__':
    A = Variable('A')
    B = Variable('B')
    C = Variable('C')
    D = Variable('D')
    E = Variable('E')

    # out = ((C | B & E) & (A | D) & E) & E
    out = ~((C | B) & (A & C))

    print('-' * 100)
    print_truth_table(out)
    print('-' * 100)
    print('PDNF', build_PDNF(out))
    print('-' * 100)
    print('PCNF', build_PCNF(out))
    print('-' * 100)
    print('PDNF minimization', minimize_PDNF(out))
    print('-' * 100)
    print('PCNF minimization', minimize_PCNF(out))
    print('-' * 100)

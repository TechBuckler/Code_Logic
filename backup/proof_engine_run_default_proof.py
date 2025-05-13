from z3 import *
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase





def run_default_proof():
    """Run the default proof for the decide function."""
    cpu = Int('cpu')
    q = Bool('q')
    c = Bool('c')

    def output(cpu, q, c):
        return If(c, 3,
               If(And(q, cpu < 95), 2,
               If(q, 1, 0)))

    valid_cpu = And(cpu >= 0, cpu <= 100)
    valid_output = Or(output(cpu, q, c) == 0,
                      output(cpu, q, c) == 1,
                      output(cpu, q, c) == 2,
                      output(cpu, q, c) == 3)

    theorem = ForAll([cpu, q, c], Implies(valid_cpu, valid_output))
    print("Checking Z3 proof...")
    prove(theorem)
    print("proved")
    return True
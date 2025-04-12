import sys
from NameValidator import is_valid_name

def load_vars(asm_prog, symbol_table):
    line_no = 0
    var_addr = 16

    for line in asm_prog:
        line_no += 1
        
        if not line.strip().startswith('@'):
            continue
        
        # A-instruction detected
        comment = line.find("//")
        if comment != -1:
            line = line[:comment]

        spacehunter = line.split()
        if len(spacehunter) > 1:
            print(f"[EXTERNAL ERROR] [LINE {line_no}] Variable names must not contain spaces.")
            sys.exit(1)
        
        var = spacehunter[0][1:]
        if var.isdigit(): # it means a number is being used to address a memory location; not a variable declaration/access
            continue
        
        if var[0].isdigit():
            print(f"[EXTERNAL ERROR] [LINE {line_no}] Variable names must not start with digits.");
            sys.exit(1)
        
        if not is_valid_name(var):
            print(f"[EXTERNAL ERROR] [LINE {line_no}] Invalid variable name: variable names must only contain alphanumeric characters and the following symbols: _ $ : .")
            sys.exit(1)

        if var not in symbol_table:
            symbol_table[var] = var_addr
            var_addr += 1

import sys
from NameValidator import is_valid_name

def load_labels(asm_prog, symbol_table):
    line_no = 0
    ram_no = 0;
    
    for line in asm_prog:
        line_no += 1
        
        if line.strip().startswith("//") or line.strip() == "":
            continue
        
        if not line.strip().startswith('('):
            ram_no += 1
            continue
        
        # line starts with (, start parsing label
        comment = line.find("//")
        if comment != -1:
            line = line[:comment]

        spacehunter = line.split()
        if len(spacehunter) > 1:
            print(f"[EXTERNAL ERROR] [LINE {line_no}] Labels must not contain spaces.")
            sys.exit(1)
        
        if not spacehunter[0].endswith(')'):
            print(f"[EXTERNAL ERROR] [LINE {line_no}] Unclosed bracket in label declaration.")
            sys.exit(1)
        
        label = spacehunter[0][1:-1]
        if label[0].isdigit():
            print(f"[EXTERNAL ERROR] [LINE {line_no}] Labels must not start with digits.")
            sys.exit(1)
        
        if not is_valid_name(label):
            print(f"[EXTERNAL ERROR] [LINE {line_no}] Invalid label: labels must only contain alphanumeric characters and the following symbols: _ $ : .")
            sys.exit(1)

        if label in symbol_table:
            print(f"[EXTERNAL ERROR] [LINE {line_no}] Redeclaration of label {label}.")
            sys.exit(1)

        symbol_table[label] = ram_no

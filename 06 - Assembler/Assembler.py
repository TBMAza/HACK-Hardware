import sys

from LoadLabels import load_labels
from LoadVars import load_vars
from AvengersAssemble import avengers_assemble

def main():
    if len(sys.argv) != 2:
        print("[USAGE] python script.py <filename.asm>")
        sys.exit(1)

    filename = sys.argv[1]

    if not filename.lower().endswith(".asm"):
        print("[EXTERNAL ERROR] File extension must be .asm")
        sys.exit(1)

    try:
        asm_prog = open(filename, 'r')
    except FileNotFoundError:
        print(f"[EXTERNAL ERROR] File '{filename}' not found.")
        sys.exit(1)
    except IOError as e:
        print(f"[INTERNAL ERROR] Could not open file '{filename}'. Reason: {e}")
        sys.exit(1)
    
    symbol_table = {
        "R0": 0,
        "R1": 1,
        "R2": 2,
        "R3": 3,
        "R4": 4,
        "R5": 5,
        "R6": 6,
        "R7": 7,
        "R8": 8,
        "R9": 9,
        "R10": 10,
        "R11": 11,
        "R12": 12,
        "R13": 13,
        "R14": 14,
        "R15": 15,
        
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,

        "SCREEN": 16384,
        "KBD": 24576
    }

    print("[PROGRESS] Loading labels in symbol table...")
    load_labels(asm_prog, symbol_table)
    asm_prog.seek(0)
    print("[PROGRESS] Done.")
    
    print("[PROGRESS] Loading variables in symbol table...")
    load_vars(asm_prog, symbol_table)
    asm_prog.seek(0)
    print("[PROGRESS] Done.")
    
    print("[PROGRESS] Assembling...")
    avengers_assemble(asm_prog, symbol_table, filename[:-4])
    print("[PROGRESS] Done. Executable was successfully created.")

    asm_prog.close()

if __name__ == "__main__":
    main()

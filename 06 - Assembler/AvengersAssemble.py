import sys
import re

def translate_a_ins(ins, symbol_table, binary):
    comment = ins.find("//")
    if comment != -1:
        ins = ins[:comment]

    spacehunter = ins.split()
    var = spacehunter[0][1:]
    
    if var.isdigit():
        ins_partial = format(int(var) % 32768, '015b')
    else:
        ins_partial = format(symbol_table[var], '015b')
    
    binary.write('0' + ins_partial + '\n')

def translate_c_ins(ins, symbol_table, binary, line_no):
    comment = ins.find("//")
    if comment != -1:
        ins = ins[:comment]

    spacehunter = ins.split()
    if len(spacehunter) > 1:
        print(f"[EXTERNAL ERROR] [LINE {line_no}] Instructions must not contain spaces.")
        sys.exit(1)

    cins = spacehunter[0]

    destcomp_tmp, jmp = cins.split(';') if ';' in cins else [cins, None]
    dest, comp = destcomp_tmp.split('=') if '=' in destcomp_tmp else [None, destcomp_tmp]
    operand1, operand2, operator = [None, None, None]
    if '+' in comp or '-' in comp or '&' in comp or '|' in comp:
        operand1, operand2 = re.split(r"[-+&|]", comp)
        if not operand1 or not operand2:
            if '-' not in comp:
                print(f"[EXTERNAL ERROR] [LINE {line_no}] Too few operands in computation: {comp}.")
                sys.exit()
            elif operand1:
                print(f"[EXTERNAL ERROR] [LINE {line_no}] Invalid computation: {comp}.")
                sys.exit()
            else:
                operand1 = '-' + operand2
                operand2 = None
                operator = None
        else:
            operator = '+' if '+' in comp else ('-' if '-' in comp else ('&' if '&' in comp else ('|' if '|' in comp else None)))
    else:
        operand1 = comp
        operand2 = None
        operator = None

    valid_conf1 = not dest and operand1 and not operand2 and not operator and not jmp
    valid_conf2 = not dest and operand1 and not operand2 and not operator and jmp
    valid_conf3 = not dest and operand1 and operand2 and operator and not jmp
    valid_conf4 = not dest and operand1 and operand2 and operator and jmp
    valid_conf5 = dest and operand1 and not operand2 and not operator and not jmp
    valid_conf6 = dest and operand1 and not operand2 and not operator and jmp
    valid_conf7 = dest and operand1 and operand2 and operator and not jmp
    valid_conf8 = dest and operand1 and operand2 and operator and jmp


    use_dest_as_comp = False # in absence of assignments

    # C-instruction error handling [START]
    
    # handle invalid instruction
    if not (valid_conf1 or valid_conf2 or valid_conf3 or valid_conf4 or valid_conf5 or valid_conf6 or valid_conf7 or valid_conf8):
        print(f"[EXTERNAL ERROR] [LINE {line_no}] Invalid instruction: {cins}.")
        sys.exit(1)

    # if destination is addressed, check if correct
    if (valid_conf3 or valid_conf4 or valid_conf5 or valid_conf6) and dest not in ['A', 'M', 'D', "AM", "AD", "MD", "AMD"]:
        print(f"[EXTERNAL ERROR] [LINE {line_no}] Destination can be only A, M, D, AM, AD, MD or AMD.")
        sys.exit(1)
    
    # if only one operand, check if operation is valid
    if (valid_conf1 or valid_conf2 or valid_conf5 or valid_conf6) and operand1 not in ['0', '1', "-1", 'A', 'M', 'D', "!A", "!M", "!D", "-A", "-M", "-D"]:
        print(f"[EXTERNAL ERROR] [LINE {line_no}] Computation can be only 0, 1, -1, a valid unary operation with A, M, D or a valid binary operation.")
        sys.exit(1)

    # if two operands, check if operation is valid
    if valid_conf3 or valid_conf4 or valid_conf7 or valid_conf8:
        if operator not in ['+', '-', '&', '|']:
            print(f"[EXTERNAL ERROR] [LINE {line_no}] Invalid binary operator: {operator}.")
            sys.exit(1)

        if operand1 == '1':
            print(f"[EXTERNAL ERROR] [LINE {line_no}] 1 is not a valid left operand in a Hack assembly binary operation.");
            sys.exit(1)

        if operand1 == operand2:
            print(f"[EXTERNAL ERROR] [LINE {line_no}] The two operands cannot be the same register.")
            sys.exit(1)

        if operand1 == 'A' and operand2 == 'M' or operand1 == 'M' and operand2 == 'A':
            print(f"[EXTERNAL ERROR] [LINE {line_no}] Binary operations are not possible between A and M registers.")
            sys.exit(1)

        if operator != '-' and operand2 != '1' and (operand1 == 'A' or operand1 == 'M'):
            print(f"[EXTERNAL ERROR] [LINE {line_no}] {operand1} cannot be the left operand unless you're subtracting or the second operand is 1.")
            sys.exit(1)

    # if jump instruction is addressed, check if correct
    if (valid_conf2 or valid_conf4 or valid_conf6 or valid_conf8) and jmp not in ["JMP", "JEQ", "JNE", "JLT", "JLE", "JGT", "JGE"]:
        print(f"[EXTERNAL ERROR] [LINE {line_no}] Invalid jump statement: {jmp}. Valid jump statements: JMP, JEQ, JNE, JLT, JLE, JGT, JGE.")
        sys.exit(1)
    
    # C-instruction error handling [END]

    # translation to machine instruction [START]
    
    # set destination bits
    if dest == 'A':
        dest_bits = "100"
    
    elif dest == 'M':
        dest_bits = "001"
    
    elif dest == 'D':
        dest_bits = "010"
    
    elif dest == "AM":
        dest_bits = "101"
    
    elif dest == "AD":
        dest_bits = "110"
    
    elif dest == "MD":
        dest_bits = "011"
    
    elif dest == "AMD":
        dest_bits = "111"
    
    else:
        dest_bits = "000"

    # set jump bits
    if jmp == "JMP":
        jmp_bits = "111"
    
    elif jmp == "JEQ":
        jmp_bits = "010"
    
    elif jmp == "JNE":
        jmp_bits = "101"
    
    elif jmp == "JLT":
        jmp_bits = "100"
    
    elif jmp == "JLE":
        jmp_bits = "110"
    
    elif jmp == "JGT":
        jmp_bits = "001"
    
    elif jmp == "JGE":
        jmp_bits = "011"
    
    else:
        jmp_bits = "000"

    # set computation bits
    if comp == '0':
        comp_bits = "0101010"

    elif comp == '1':
        comp_bits = "0111111"

    elif comp == "-1":
        comp_bits = "0111010"

    elif comp == 'A':
        comp_bits = "0110000"
    
    elif comp == 'M':
        comp_bits = "1110000"
    
    elif comp == 'D':
        comp_bits = "0001100"
    
    elif comp == "!A":
        comp_bits = "0110001"
    
    elif comp == "!M":
        comp_bits = "1110001"
    
    elif comp == "!D":
        comp_bits = "0001101"
    
    elif comp == "-A":
        comp_bits = "0110011"
    
    elif comp == "-M":
        comp_bits = "1110011"
    
    elif comp == "-D":
        comp_bits = "0001111"
    
    elif comp == "D+1":
        comp_bits = "0011111"
    
    elif comp == "D-1":
        comp_bits = "0001110"
    
    elif comp == "D+A":
        comp_bits = "0000010"
    
    elif comp == "D-A":
        comp_bits = "0010011"
    
    elif comp == "D&A":
        comp_bits = "0000000"
    
    elif comp == "D|A":
        comp_bits = "0010101"
    
    elif comp == "D+M":
        comp_bits = "1000010"
    
    elif comp == "D-M":
        comp_bits = "1010011"
    
    elif comp == "D&M":
        comp_bits = "1000000"
    
    elif comp == "D|M":
        comp_bits = "1010101"
    
    elif comp == "A+1":
        comp_bits = "0110111"
    
    elif comp == "A-1":
        comp_bits = "0110010"
    
    elif comp == "A-D":
        comp_bits = "0000111"
    
    elif comp == "M+1":
        comp_bits = "1110111"
    
    elif comp == "M-1":
        comp_bits = "1110010"
    
    else: # comp == M-D
        comp_bits = "1000111"

    # translation to machine instruction [END]

    binary.write("111" + comp_bits + dest_bits + jmp_bits + '\n')

def avengers_assemble(asm_prog, symbol_table, filename):
    try:
        binary = open(filename + ".hack", 'a')
    except IOError as e:
        print(f"[INTERNAL ERROR] Could not create binary file. Reason: {e}")
        sys.exit(1)
    
    line_no = 0
    for line in asm_prog:
        line_no += 1
        
        if line.strip().startswith("//") or line.strip().startswith('(') or line.strip() == "":
            continue
        if line.strip().startswith('@'):
            translate_a_ins(line, symbol_table, binary)
        else:
            translate_c_ins(line, symbol_table, binary, line_no)

    binary.close()

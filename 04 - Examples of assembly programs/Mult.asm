// if(a == 0 || b == 0) return 0;
    
// int abs_a = a >= 0 ? a : -a;
// int abs_b = b >= 0 ? b : -b;

// int g = abs_a > abs_b ? a : b;
// int l = a + b - g;

// if(l < 0) {
//     g = -g;
//     l = -l;
// }

// int ans = 0;
// while(l > 0) {
//     ans += g;
//     --l;
// }

// return ans;

// operands in RAM[0] (a), RAM[1] (b)
// result in RAM[2] (ans)

// if a == 0, ans = 0
@R0
D=M
@OUTZERO
D;JEQ

// if b == 0, ans = 0
@R1
D=M
@OUTZERO
D;JEQ

// if a >= 0, abs_a = a, else abs_a = -a
@R0
D=M
@abs_a
M=D // set abs_a to a
@CONTINUE_1
D;JGE // don't negate if positive by jumping to CONTINUE_1

M=-M // negate abs_a if negative to make it positive

(CONTINUE_1)

// if b >= 0, abs_b = b, else abs_b = -b
@R1
D=M
@abs_b
M=D // set abs_b to b
@CONTINUE_2
D;JGE // don't negate if positive by jumping to CONTINUE_2

M=-M // negate abs_b if negative to make it positive

(CONTINUE_2)

@R0
D=M
@greater
M=D // set greater to a

@abs_a
D=M
@abs_b
D=D-M
@CONTINUE_3
D;JGE // check if abs_a is greater or equal to abs_b, and if so, jump to CONTINUE_3

@R1
D=M
@greater
M=D // otherwise set greater to b

(CONTINUE_3)

// compute lesser = a + b - greater
@R0
D=M
@lesser
M=D
@R1
D=M
@lesser
M=D+M
@greater
D=M
@lesser
M=M-D
D=M

@CONTINUE_4
D;JGE // jump to CONTINUE_4 if lesser is non-negative

// otherwise negate lesser and greater
M=-M
@greater
M=-M

(CONTINUE_4)

@ans
M=0 // init ans to zero

(LOOP)
    @greater
    D=M
    @ans
    M=D+M // ans += greater

    @lesser
    M=M-1 // --lesser
    D=M

    @LOOP
    D;JGT // while lesser > 0

@ans
D=M
@R2
M=D // store ans in RAM[2]

(EXIT)
    @EXIT
    0;JMP

(OUTZERO)
    @R2
    M=0
    @EXIT
    0;JMP

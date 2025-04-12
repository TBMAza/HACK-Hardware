// screenmax = 8192
@8192
D=A
@screenmax
M=D

(FOREVER)

    @color
    M=0 // select white as screen color

    @KBD
    D=M
    @WHITE
    D;JEQ // if no keypress is detected, keep white as selected screen color

    @color
    M=-1 // otherwise change selection to black

    (WHITE)

    // i = 0
    @i
    M=0

    // screenptr = address to first 16 pixels
    @SCREEN
    D=A
    @screenptr
    M=D

    // blacken pixels
    (LOOP)
        @color
        D=M
        @screenptr
        A=M // point to content of screenptr's location
        M=D // set current 16 pixels to selected color
        
        // go to next 16 pixels
        @screenptr
        M=M+1
        
        // ++i
        @i
        M=M+1

        // loop if i < screenmax
        @screenmax
        D=M
        @i
        D=D-M
        @LOOP
        D;JGT

    @FOREVER
    0;JMP

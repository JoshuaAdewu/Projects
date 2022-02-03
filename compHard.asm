	;; Name: Joshua Adewunmi
        ;; user ID: NQ13895
        ;; Project: 4
        ;; Description: The hard game mode for the tic-tac-toe 4 row game


extern makeBoard
extern checkWinner
extern randomNum
	
	section         .data
location:       db      "Enter a location on the board 1-16", 10
len:            equ     $ - location
invalid:        db      "Input is invalid (1-16)", 10
len2:           equ     $ - invalid

taken:          db      "This is not an empty space. Try again!", 10
lenTaken:       equ     $ - taken

player:         db      "x", 10
playerlen:      equ     $ - player

copu:           db      "o", 10 ;cpu gave me problems for some reason
cpulen:         equ     $ - copu

	
boardRow1:      db      " | | | ", 10, 13
                db      "_______", 10, 13
boardRow2:      db      " | | | ", 10, 13
                db      "_______", 10, 13
boardRow3:      db      " | | | ", 10, 13
                db      "_______", 10, 13
boardRow4:      db      " | | | ", 10, 13
                db      "_______", 10, 13
lenBoard:       equ     $ - boardRow1

space:          db      " "    ;white space for characters

nums:           db      "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16", 10, 13
array1:         db      "[       ]", 10, 13
lenNum:         equ     $ - nums

;//board:          db      space,space,space,space,space,space,space,space,space,space,space,space,space,space,space,space
;//gamelen:        equ     $ - board
board:          db      0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20


min:            dw      1
max:            dw      16
new_line:       db      10

        section         .bss
pick:   resb            10

        section         .text
        global          compHard

valid:                          ;checks input
        mov     rax, pick       ;load user input
        cmp     rax, max       ;check if within range
        ja      nValid          ;if not valid go to nValid
        cmp     rax, min       ;checks if within range
        jb      nValid
        cmp     rax, 1
        je      box1            ;if valid put in first spot
        cmp     rax, 2
        je      box2
        cmp     rax, 3
        je      box3
        cmp     rax, 4
        je      box4
        cmp     rax, 5
        je      box5
        cmp     rax, 6
        je      box6
        cmp     rax, 7
        je      box7
        cmp     rax, 8
        je      box8
        cmp     rax, 9
        je      box9
        cmp     rax, 10
        je      box10
        cmp     rax, 11
        je      box11
        cmp     rax, 12
        je      box12
        cmp     rax, 13
        je      box13
        cmp     rax, 14
        je      box14
        cmp     rax, 15
        je      box15
        cmp     rax, 16
        je      box16
        jmp     end
	
	
nValid:
        mov     rax, 1
        mov     rdi, 1
        mov     rsi, invalid
        mov     rdx, len2

        mov     rax, 1
        mov     rdi, 1
        mov     rsi, location
        mov     rdx, len
        syscall

        mov     rax, 0
        mov     rdi, 0
        mov     rsi, pick
        mov     rdx, 17
        ret
	
	
compHard:

	xor     rdi, rdi
        xor     rax, rax
        mov     rax, gameBoard
        mov     rdi, rax
        call    makeBoard	;prints out the gameBoard
        syscall
        
        mov     rax, 1
        mov     rdi, 1
        mov     rsi, location	;prints out prompt for location
        mov     rdx, len
        syscall

        mov     rax, 0
        mov     rdi, 0
        mov     rsi, pick	;users choice of location on board
        mov     rdx, 17
        syscall

	mov     rax, player
        push    rax
        push    board
        call    checkWinner
        push    rbp             ;prepare stack
        mov     rbp, rsp
        push    rax
        call    valid
        call    gameBoard
        call    checkWinner

        mov     rax, copu
        push    rax
        push    board
        call    checkWinner
        push    rbp             ;prepare stack
        mov     rbp, rsp
        push    rax
        call    cpuValid
        call    gameBoard
        call    checkWinner

        ret

	
cpuValid:
        mov     rax, randomNum       ;load user input
        cmp     rax, max       ;check if within range
        ja      nValid          ;if not valid go to nValid
        cmp     rax, min       ;checks if within range
        jb      nValid
        cmp     rax, 1
        je      box1            ;if valid put in first spot
        cmp     rax, 2
        je      box2
        cmp     rax, 3
        je      box3
        cmp     rax, 4
        je      box4
        cmp     rax, 5
        je      box5
        cmp     rax, 6
        je      box6
        cmp     rax, 7
        je      box7
        cmp     rax, 8
        je      box8
        cmp     rax, 9
        je      box9
        cmp     rax, 10
        je      box10
        cmp     rax, 11
        je      box11
        cmp     rax, 12
        je      box12
        cmp     rax, 13
        je      box13
        cmp     rax, 14
        je      box14
        cmp     rax, 15
        je      box15
        cmp     rax, 16
        je      box16
        jmp     end




box1:
        mov     rsi, board
        add     rsi, 1          ;go to right spot
        mov     rax, space
        cmp     [rsi], rax      ;check if empty
        jne     nValid
        mov     rax, [rbp + 8]  ;move player into rax
        mov     [rsi], rax
        jmp     end

box2:

        mov     rsi, board
        add     rsi, 2
        mov     rax, space
        cmp     [rsi], rax      ;check if empty
        jne     nValid
        mov     rax, [rbp + 8]  ;move player into rax
        mov     [rsi], rax
        jmp     end

box3:

        mov     rsi, board
        add     rsi, 3
        mov     rax, space
        cmp     [rsi], rax      ;check if empty
        jne     nValid
        mov     rax, [rbp + 8]  ;move player into rax
        mov     [rsi], rax
        jmp     end

box4:

        mov     rsi, board
        add     rsi, 4
        mov     rax, space
        cmp     [rsi], rax      ;check if empty
        jne     nValid
        mov     rax, [rbp + 8]  ;move player into rax
        mov     [rsi], rax
        jmp     end

box5:

        mov     rsi, board
        add     rsi, 5
        mov     rax, space
        cmp     [rsi], rax      ;check if empty
        jne     nValid
        mov     rax, [rbp + 8]  ;move player into rax
        mov     [rsi], rax
        jmp     end

box6:

        mov     rsi, board
        add     rsi, 6
        mov     rax, space
        cmp     [rsi], rax      ;check if empty
        jne     nValid
        mov     rax, [rbp + 8]  ;move player into rax
        mov     [rsi], rax
        jmp     end

box7:

        mov     rsi, board
        add     rsi, 7
        mov     rax, space
        cmp     [rsi], rax      ;check if empty
        jne     nValid
        mov     rax, [rbp + 8]  ;move player into rax
        mov     [rsi], rax
        jmp     end

box8:

        mov     rsi, board
        add     rsi, 8
        mov     rax, space
        cmp     [rsi], rax      ;check if empty
        jne     nValid
        mov     rax, [rbp + 8]  ;move player into rax
        mov     [rsi], rax
        jmp     end
	
box9:

        mov     rsi, board
        add     rsi, 9
        mov     rax, space
        cmp     [rsi], rax      ;check if empty
        jne     nValid
        mov     rax, [rbp + 8]  ;move player into rax
        mov     [rsi], rax
        jmp     end

box10:

        mov     rsi, board
        add     rsi, 10
        mov     rax, space
        cmp     [rsi], rax      ;check if empty
        jne     nValid
        mov     rax, [rbp + 8]  ;move player into rax
        mov     [rsi], rax
        jmp     end

box11:

        mov     rsi, board
        add     rsi, 11
        mov     rax, space
        cmp     [rsi], rax      ;check if empty
        jne     nValid
        mov     rax, [rbp + 8]  ;move player into rax
        mov     [rsi], rax
        jmp     end

box12:

        mov     rsi, board
        add     rsi, 12
        mov     rax, space
        cmp     [rsi], rax      ;check if empty
        jne     nValid
        mov     rax, [rbp + 8]  ;move player into rax
        mov     [rsi], rax
        jmp     end

box13:

        mov     rsi, board
        add     rsi, 13
        mov     rax, space
        cmp     [rsi], rax      ;check if empty
        jne     nValid
        mov     rax, [rbp + 8]  ;move player into rax
        mov     [rsi], rax
        jmp     end

box14:

        mov     rsi, board
        add     rsi, 14
        mov     rax, space
        cmp     [rsi], rax      ;check if empty
        jne     nValid
        mov     rax, [rbp + 8]  ;move player into rax
        mov     [rsi], rax
        jmp     end

box15:

        mov     rsi, board
        add     rsi, 15
        mov     rax, space
        cmp     [rsi], rax      ;check if empty
        jne     nValid
        mov     rax, [rbp + 8]  ;move player into rax
        mov     [rsi], rax
        jmp     end

box16:

        mov     rsi, board
        add     rsi, 16
        mov     rax, space
        cmp     [rsi], rax      ;check if empty
        jne     nValid
        mov     rax, [rbp + 8]  ;move player into rax
        mov     [rsi], rax
        jmp     end

gameBoard:
        xor     rdi, rdi
        xor     rax, rax
        mov     rax, makeBoard
        mov     rdi, rax
        call    makeBoard       ;prints out the gameBoard
        syscall
        ret

end:
        pop     rax
        pop     rbp
        ret
	
	
exit:
        mov     rax, 60
        xor     rdi,rdi
        syscall

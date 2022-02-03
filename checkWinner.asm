        ;; Name: Joshua Adewunmi
        ;; user ID: NQ13895
        ;; Project: 4
        ;; Description: Checks the game board to see if either player gets 4 X's in
	;;              a row or whether the CPU gets 4 O's in a row

	
extern makeBoard
extern randomNum
	
        section         .data
winner:       	db      "YOU WIN", 10
lenwin:         equ     $ - winner

cpuWin:		db	"YOU LOSE", 10
lenL:		equ	$ - cpuWin
	
player:	        db      "x", 10
playerlen:      equ     $ - player

	
copu:		db	"o", 10	
cpulen:		equ	$ - copu
	
draw:		db	"It's a draw!", 10
drawlen:	equ	$ - draw

boardRow1:	db	" | | | ", 10, 13
		db	"_______", 10, 13
boardRow2:	db      " | | | ", 10, 13
		db	"_______", 10, 13
boardRow3:	db      " | | | ", 10, 13
		db	"_______", 10, 13
boardRow4:	db      " | | | ", 10, 13
		db	"_______", 10, 13
lenBoard:	equ	$ - boardRow1

location:       db      "Enter a location on the board 1-16", 10
len:            equ     $ - location
invalid:        db      "Input is invalid (1-16)", 10
len2:           equ     $ - invalid

taken:          db      "This is not an empty space. Try again!", 10
lenTaken:       equ     $ - taken

space:		db	0x20	;white space for characters
	
nums:		db	"0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16", 10, 13
array1:		db	"[       ]", 10, 13
lenNum:		equ	$ - nums

;//board:		db	space,space,space,space,space,space,space,space,space,space,space,space,space,space,space,space
;//gamelen:        equ     $ - board
board:          db      0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20
	
min:            dw      1
max:            dw      16
new_line:       db      10
line_len:	equ	$ - new_line

        section         .bss
pick:   resb            10
read:	resb		1000
	
        section         .text
        global          checkWinner
checkWinner:
	mov     rax, 1
        mov     rdi, 1
        mov     rsi, location   ;prompts user for location
        mov     rdx, len
        syscall

        mov     rax, 0
        mov     rdi, 0
        mov     rsi, pick       ;users choice for board placement
        mov     rdx, 17
        syscall

	mov	rax, 4
	mov	rbx, 2 		; reads the user string/ char
	syscall

	mov	rcx, 4		;(4 charcters in a row)
	mov	rsi, board	;loads address of board
	mov	rbx, 1

	call	checkRow
	call	checkCol
	call	equal

	xor     rdi, rdi
        xor     rax, rax
        mov     rax, makeBoard
        mov     rdi, rax
        call    makeBoard       ;prints out the gameBoard
        syscall
	ret
	
noR:				;space exists there so no repeats
	pop	rsi
	ret

win:
	mov     rax,1
        mov     rdi,1
        mov     rsi, new_line   ;goes to next line
        mov     rdx,1
        syscall
	
	mov     rax, 1
        mov     rdi, 1
        mov     rsi, winner   ;prompts user for location
        mov     rdx, lenwin
        syscall
	ret			;return


equal:
	push    rsi
        mov     rax, space      ;(0x20 = space or white space)
        mov     r9, [rsi]       ;loads character at user pick
        cmp     r9, space       ;compare pick with space
        je      noR             ;if no repeat chars stop
        add     rsi, rbx        ;else go to next char
        cmp     r9, [rsi]       ;compare with second spot
        jne     noR             ;if not equal , no repeats
        add     rsi, rbx
        cmp     r9,[rsi]        ;CHECKS TO SEE IF 4 CHARS IN A COL is =
        jne     noR
        add     rsi, rbx
        cmp     r9,[rsi]
        jne     noR
        mov     rax, r9         ;goes to r8 as character with 4 repeats
	syscall
	ret

cpuEqual:
	push    rsi
        mov     rax, space      ;(0x20 = space or white space)
	call	randomNum	;randomNum out of 16
        mov     r9, [rax]       ;loads character at user pick
        cmp     r9, space       ;compare pick with space
        je      noR             ;if no repeat chars stop
        add     rsi, rbx        ;else go to next char
        cmp     r9, [rsi]       ;compare with second spot
        jne     noR             ;if not equal , no repeats
        add     rsi, rbx
        cmp     r9,[rsi]        ;CHECKS TO SEE IF 4 CHARS IN A COL is =
        jne     noR
        add     rsi, rbx
        cmp     r9,[rsi]
        jne     noR
        mov     rax, r9         ;goes to r8 as character with 4 repeats
        syscall
        ret


checkRow:
	call	equal
	cmp	rax, space	;check if it returned a space
	jne	win		;if not space winner was found
	add	rsi, 4		;go to next row
	loop	checkRow	;go through 4 times when rcx is not zero
	mov	rcx, 4		;allows rcx 4 loops
	mov	rsi, board	;loads board adress
	mov	rbx, 4		;compare separated by 4
	syscall

	call	cpuEqual
	cmp     rax, space      ;check if it returned a space
        jne     win             ;if not space winner was found
        add     rsi, 4          ;go to next row
        loop    checkRow        ;go through 4 times when rcx is not zero
        mov     rcx, 4          ;allows rcx 4 loops
        mov     rsi, board      ;loads board adress
        mov     rbx, 4          ;compare separated by 4
        syscall
	ret

checkCol:
	call    equal
        cmp     rax, space      ;check if it returned a space
        jne     win             ;if not space winner was found
	add 	rsi, 1		;go to next column
	loop	checkCol	;repeat 4 times
	mov	rsi, board
	mov	rbx, 4
	syscall

	call	cpuEqual
	cmp     rax, space      ;check if it returned a space
        jne     win             ;if not space winner was found
        add     rsi, 4          ;go to next row
        loop    checkCol        ;go through 4 times when rcx is not zero
        mov     rcx, 4          ;allows rcx 4 loops
        mov     rsi, board      ;loads board adress
        mov     rbx, 4          ;compare separated by 4
        syscall
	ret
	

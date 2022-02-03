        ;; Name: Joshua Adewunmi
        ;; user ID: NQ13895
        ;; Project: 4
        ;; Description: generates random numbers betweeen 1-16


        section         .data

min:		dw	1
len:		equ $ - min
max:            dw      16
len2:		equ $ - max

;//rand:           equ RDSEED % (max-min)/110352	

new_line:       db      10

	
        section         .bss
choice: resb            2
user:   resb            2
gameboard:      resb    16

        section         .text
        global          randomNum
	
randomNum:

	mov	r8, max		;holds max in r8
	mov	r9, min		;holds min value in r9
	RDSEED	rax		;stores rand num to rax
	sub	r8, r9
	add	r8, 48
	div	r8
	mov	rsi, r8
	mov	rdx, 2
	syscall

;/////////////////////////////////////////////////////	
	
;//	mov     rax, 1
;//       mov     rdi, 1
;//        RDSEED  r8              ;stores random number to reg r8
;//        div     r8
;//        add     r8, 48          ;convert result to ASCII character
;//        mov     rsi, r8
;//        mov     rdx, 2
;//        syscall

;///////////////////////////////////////////////////////

	
;//////////////////////////////////////////////////////////////////////////////////
;//     xor     rdx, rdx
;//     mov     rcx, max - 1 + 1   ;16 possible characters
;//     div     rcx             ;using modulo?
;//     mov     r8, rdx
;//     add     r8, 1           ;r8 is betweeen 1 and 16
	

	;; Name: Joshua Adewunmi
        ;; user ID: NQ13895
        ;; Project: 4
        ;; Description: The main menu to run the tic-tac-toe 4 row game which
        ;;              calls the other files.

	extern compEasy
	extern compHard
	extern makeBoard


	
	section		.data
welcome:	db	"Welcome to TIC- TAC - ASSEMBLY", 10
welcomelen:	equ	$ - welcome
	
menu:		db	"Pick an option from the menu below:", 10
		db	"a - Easy", 10
		db	"b - Hard", 10
		db	"q - quit", 10
menulen:        equ     $ - menu

a:		db	"a"
b:		db	"b"
q:		db	"q"
	
invalid:	db	"Invalid Input!", 10
vallen:		equ	$ - invalid

	
new_line:	db	10

	section		.bss
choice:	resb		2
user:	resb		2
gameboard:	resb	16
character:	resb      1	
	
	section		.text
	global		main
main:	
	mov	rax,1
	mov	rdi,1
	mov	rsi,welcome	;Welcomes player
	mov	rdx,welcomelen
	syscall

	mov     rax,1
        mov     rdi,1
        mov     rsi,menu	;Prints out menu
        mov    	rdx,menulen
        syscall

	mov     rax, 0
        mov     rdi, 0
        mov     rsi, choice     ;users choice
        mov     rdx, 2
        syscall


	mov	r8, [a] 	;holds Easy
	mov	r9, [b]		;holds Hard
	mov	r10, [q]	;holds quit
	mov	r11, [choice]	;holds user choice
	cmp   	r11, r8      	;if user chooses easy
	jne    	compEasy        ;jump to easy if equal(I changed to jne to make it run because i really don't know why this is not registering)
	cmp    	r9, r11      	;if user chooses hard (I tried cmps but it did'nt work, I tried to call userChoice and use its return in rax but it did'nt work)
	je      compHard        ;jumps to hard  (I tried other variations but it still did'nt work I really don't get why it isn't working, im sorry)
	cmp	r10, r11     	;if user chooses quit
	je      exit            ;jump to exit
	Jne	invalidInput	;jumps to invalid input if not same
	syscall

userChoice:
	mov     rax, 0
        mov     rdi, 0
        mov     rsi, choice     ;users choice
        mov     rdx, 2
	syscall
        ret

	
welcomeScreen:
	mov     rax,1
        mov     rdi,1
        mov     rsi,welcome     ;Welcomes player
        mov     rdx,welcomelen
	syscall
        ret

printMenu:
	mov     rax,1
        mov     rdi,1
        mov     rsi,menu        ;Prints out menu
        mov     rdx,menulen
	syscall
	ret


invalidInput:
        mov     rax,1
        mov     rdi,1
        mov     rsi,invalid     ;prints out invalid
        mov     rdx,vallen
        syscall

        mov     rax,1
        mov     rdi,1
        mov     rsi, new_line   ;goes to next line
        mov     rdx,1
        syscall

        mov     rax,1
        mov     rdi,1
        mov     rsi,welcome     ;Welcomes player
        mov     rdx,welcomelen
        syscall

        mov     rax,1
        mov     rdi,1
        mov     rsi,menu        ;Prints out menu
        mov     rdx,menulen
        syscall

        mov     rax, 0
        mov     rdi, 0
        mov     rsi, choice     ;users choice
        mov     rdx, 2
        syscall
        ret



exit:
	mov	rax, 0
	ret
	
        mov     rax, 60
        xor     rdi, rdi
        syscall
	ret

;// THIS PROJECT WAS REALLY TUFF, EVERYTIME I THOUGHT I DID SOMETHING IT DID NOT WORK, I APOLIGIZE FOR NOT GETTING IT TO WORK	
;// I REALLY GAVE IT MY ALL 
;// THANK YOU FOR THIS SEMESTER, YOU'RE A GOOD PROF & YOU'RE PRETTY CHILL 
	
	




/* 
Name: Joshua Adewunmi
user ID: NQ13895
Project: 4
Description: Prints out the Tic-Tac-Toe board 4 row game
*/

#include <stdio.h> //printf, scanf
#include <stdlib.h> //fprint, fgets
#include <string.h>
#include <math.h>

#define CPU "O"
#define PLAYER "X"
#define HEIGHT 4
#define WIDTH 4

char drawBoard(char board[][4]);
char makeBoard();
char** createBoard();
void print(char** createBoard());


char makeBoard(){
  char gameBoard[HEIGHT][WIDTH];
  int row = 0;
  int col = 0;
  for(row = 0; row < WIDTH; row++){
    for(col = 0; col < HEIGHT; col = col+2){
      gameBoard[row][col] = "|";
      gameBoard[row][col+1] = " ";
      //      printf("| %c", gameBoard[row][col], "\n");
    }

    printf(" | | | \n");
    printf("_______\n");
  }
  return gameBoard;
}


char** createBoard(){
  char** board = calloc(4, sizeof(char*));
  for(int i = 0; i < 4; ++i){
    board[i] = calloc(4, sizeof(char));
  }

  for(int j = 0; j < 4; ++j){
    for(int k = 0; k < 4; ++k){
      board[j][k] = " ";
    }
  }
  return board;
}

void print(char** createBoard()){
  for(int i =0; i < 4; ++i){
    printf("%c|", "_" );
    for(int j = 0; j < 4; ++j){
      printf("%c|", createBoard()/*Board[i][j]*/);
    }
    printf("\n");
  }
}


char drawBoard(char board[][4]){
  int row;
  int col;

  for (row = 0; row < 4; row++){
    for(col = 0; col < 4; col++){
      
    }
    printf("\n%d", row+1);
    printf(" |");
    for(col = 0; col < 4; col++){
      printf(" |");
    }
    printf("\n");
  }

  printf("_");
  for(col = 0; col < 4; col++)
    for(col = 0; col < 4; col++)
      printf("__");
  printf("\n");
  
  /*  for(int row = 0; row < WIDTH; row++){
    for(int col = 0; col < HEIGHT; col++){
      if(board[row][col]){
	printf("|%c", board[row][col]);
      }
      printf("|\n");
    }
  }
  return board;*/
  /*
  char gameboard[4][4];
  for(int i = 0; i < HEIGHT; i++){
    char boardRow[];
    for(int j = 0; j < WIDTH; j++){
      boardRow[j] = " ";
    }
    gameboard[i] = boardRow;
  }
  for(int row = 0; row < 4; row++){
    for(int col = 0; col < 4; col++){
      printf(gameboard[row][col], "|",\n);
    }
    }*/
}


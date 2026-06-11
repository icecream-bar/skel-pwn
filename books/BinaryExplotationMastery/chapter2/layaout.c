#include<stdio.h>
#include<stdlib.h>

int global_init = 42; //.data
int global_uninit; //.bss

int main(){
	int local = 10; //stack
	
	char *heap_buf = malloc(16); //heap
	sprintf(heap_buf, "Hi");

	printf("Address of code (main): %p\n", main);
	printf("Address of .bss (global_uninit): %p\n", &)global_uninit;
	printf("Address of stack (local): %p\n", &)local;
	printf("Address of heap (heap_buf):%p\n", &)heap_buf;
	free(heap_buf);

	return 0;
}

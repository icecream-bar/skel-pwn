#include<stdio.h>
#include<stdlib.h>
#include<string.h>

int main(){
	char *buffer = malloc(32); //allocated on heap
	strcpy(buffer, "Hello from heap!");
	printf("%s\n", buffer);
	free(buffer);
	return 0;
}


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int initialized_global = 42;       // .data — initialized at compile time
int uninitialized_global;          // .bss  — zeroed by OS at load time

int main() {
    int local = 7;                 // stack — lives in this stack frame
    char *heap = malloc(32);       // heap  — lives until free()
    strcpy(heap, "heap buffer");

    printf("initialized global (.data): %d  @ %p\n", initialized_global, (void *)&initialized_global);
    printf("uninitialized global (.bss): %d  @ %p\n", uninitialized_global, (void *)&uninitialized_global);
    printf("local variable (stack):      %d  @ %p\n", local, (void *)&local);
    printf("heap buffer (heap):          %s  @ %p\n", heap, (void *)heap);

    free(heap);
    return 0;
}

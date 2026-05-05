#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdio.h>

int main(void) {
for (int i = 0; i < 8; i++) {
    pid_t pid = fork();
    if (pid == 0) { 
        printf("Child %d created. ", i + 1);
        execl("./task1a", "./task1a", NULL);
        exit(0);
    }
}

for (int i = 0; i < 8; i++) wait(NULL);
return 0;
}
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <signal.h>

void handle_signal(int sig) {
    printf("Child %d", getpid(), "\n");
}

int main() {
signal(SIGUSR1, handle_signal);
for (int i = 0; i < 6; i++) {
if (fork() == 0) {
    pause();
    printf("Child %d received signal. Current time: %ld\n", getpid(), time(NULL));

    kill(getppid(), SIGUSR1);
    exit(0);
}
}
sleep(3); 
kill(0, SIGUSR1); // Send signal to all children
for (int i = 0; i < 6; i++) wait(NULL);
return 0;
}
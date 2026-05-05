#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdio.h>




int main() {
pid_t pid = fork();
if (pid > 0) {
printf("Parent process. Child is PID: %d. Sleeping for 20s...\n", pid);
// Parent sleeps without calling wait(), creating a zombie
sleep(100);
} else {
    sleep(100);
printf("Child process exiting immediately...\n");
exit(0);
}
return 0;
}
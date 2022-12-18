#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/inotify.h>
#include <limits.h>
#include <unistd.h>

 // function prototype to display information from inotify_event structure
static void displayInotifyEvent(struct inotify_event *ptr);

#define BUF_LEN (10 * (sizeof(struct inotify_event) + NAME_MAX + 1))

int main(int argc, char *argv[]) {
    int fd = 0, wd = 0;
    char buf[BUF_LEN];
    ssize_t nRead;
    char *p = NULL;
    struct inotify_event *event = NULL;

    if (argc < 2 || strcmp(argv[1], "--help") == 0) {
        fprintf(stderr, "Usage: %s filepath \n", argv[0]);
        return EXIT_FAILURE;
    }

    // create inotify instance
    fd = inotify_init1(0); 

    if (fd < 0) {
        perror("inotify_init1");
        exit(EXIT_FAILURE);
    }

    // add a watch for file modification event
    wd = inotify_add_watch(fd, argv[1], IN_MODIFY);

    if (wd < 0) {
        perror("inotify_add_watch");
        exit(EXIT_FAILURE);
    }
    else {
        fprintf(stdout, "Watching %s using wd %d\n", argv[1], wd);
    }

    while(1) { // read events indefinitely
        nRead = read(fd, buf, BUF_LEN);
        if (nRead < 0) {
            perror ("read");
            exit(EXIT_FAILURE);
        }
        if (nRead == 0){
            perror("read() from inotify fd returned 0!");
        }
        fprintf(stdout, "Read %zd bytes from inotify fd\n", nRead);

        p = buf;
        while ( p < buf + nRead ) {
            event = (struct inotify_event *) p;
            displayInotifyEvent(event);
            p += sizeof(struct inotify_event);
        }
    }
    exit(EXIT_SUCCESS);
}

static void displayInotifyEvent(struct inotify_event *ptr) {
    printf("wd = %d; ", ptr->wd);
    printf("mask = ");
    if (ptr->mask & IN_MODIFY) {
        fprintf(stdout, "IN_MODIFY \n");
        fprintf(stdout, "File was written to!\n");
    }
}

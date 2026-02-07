#include "MT25066_Part_A_Common.h"

#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <pthread.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

typedef struct {
    int client_fd;
    size_t msg_size;
} mt25066_client_ctx_t;

static volatile sig_atomic_t mt25066_stop = 0;

static void mt25066_on_sigint(int sig) {
    (void)sig;
    mt25066_stop = 1;
}

static void *mt25066_client_thread(void *arg) {
    mt25066_client_ctx_t *ctx = (mt25066_client_ctx_t *)arg;
    int fd = ctx->client_fd;
    size_t msg_size = ctx->msg_size;

    mt25066_set_nodelay(fd);

    mt25066_message_t *msg = mt25066_message_create(msg_size);
    if (!msg) {
        close(fd);
        free(ctx);
        return NULL;
    }
    mt25066_message_fill(msg, 0x2A);

    char *send_buf = (char *)malloc(msg_size);
    char *recv_buf = (char *)malloc(msg_size);
    if (!send_buf || !recv_buf) {
        free(send_buf);
        free(recv_buf);
        mt25066_message_destroy(msg);
        close(fd);
        free(ctx);
        return NULL;
    }

    while (!mt25066_stop) {
        ssize_t recvd = mt25066_recv_all(fd, recv_buf, msg_size);
        if (recvd <= 0) {
            break;
        }

        mt25066_message_flatten(msg, send_buf);
        if (mt25066_send_all(fd, send_buf, msg_size) < 0) {
            break;
        }
    }

    free(send_buf);
    free(recv_buf);
    mt25066_message_destroy(msg);
    close(fd);
    free(ctx);
    return NULL;
}

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <port> <message_size>\n", argv[0]);
        return 1;
    }

    int port = atoi(argv[1]);
    size_t msg_size = (size_t)strtoul(argv[2], NULL, 10);
    if (port <= 0 || msg_size == 0) {
        fprintf(stderr, "Invalid port or message size.\n");
        return 1;
    }

    signal(SIGINT, mt25066_on_sigint);

    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        perror("socket");
        return 1;
    }

    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons((uint16_t)port);

    if (bind(server_fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("bind");
        close(server_fd);
        return 1;
    }

    if (listen(server_fd, 128) < 0) {
        perror("listen");
        close(server_fd);
        return 1;
    }

    fprintf(stdout, "A1 Server listening on port %d (msg_size=%zu)\n", port, msg_size);

    while (!mt25066_stop) {
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        int client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);
        if (client_fd < 0) {
            if (errno == EINTR) {
                continue;
            }
            perror("accept");
            break;
        }

        mt25066_client_ctx_t *ctx = (mt25066_client_ctx_t *)calloc(1, sizeof(mt25066_client_ctx_t));
        if (!ctx) {
            close(client_fd);
            continue;
        }
        ctx->client_fd = client_fd;
        ctx->msg_size = msg_size;

        pthread_t tid;
        if (pthread_create(&tid, NULL, mt25066_client_thread, ctx) != 0) {
            close(client_fd);
            free(ctx);
            continue;
        }
        pthread_detach(tid);
    }

    close(server_fd);
    return 0;
}

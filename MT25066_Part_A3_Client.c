#include "MT25066_Part_A_Common.h"

#include <arpa/inet.h>
#include <netinet/in.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

typedef struct {
    const char *server_ip;
    int port;
    size_t msg_size;
    uint64_t duration_ns;
    mt25066_stats_t stats;
} mt25066_thread_arg_t;

static int mt25066_connect_to_server(const char *ip, int port) {
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    if (fd < 0) {
        return -1;
    }

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons((uint16_t)port);
    if (inet_pton(AF_INET, ip, &addr.sin_addr) != 1) {
        close(fd);
        return -1;
    }

    if (connect(fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        close(fd);
        return -1;
    }

    mt25066_set_nodelay(fd);
    return fd;
}

static void *mt25066_client_thread(void *arg) {
    mt25066_thread_arg_t *targ = (mt25066_thread_arg_t *)arg;
    int fd = mt25066_connect_to_server(targ->server_ip, targ->port);
    if (fd < 0) {
        return NULL;
    }

    char *send_buf = (char *)malloc(targ->msg_size);
    char *recv_buf = (char *)malloc(targ->msg_size);
    if (!send_buf || !recv_buf) {
        free(send_buf);
        free(recv_buf);
        close(fd);
        return NULL;
    }
    memset(send_buf, 0x5A, targ->msg_size);

    uint64_t start = mt25066_now_ns();
    uint64_t end = start + targ->duration_ns;

    while (mt25066_now_ns() < end) {
        uint64_t t0 = mt25066_now_ns();
        if (mt25066_send_all(fd, send_buf, targ->msg_size) < 0) {
            break;
        }
        if (mt25066_recv_all(fd, recv_buf, targ->msg_size) <= 0) {
            break;
        }
        uint64_t t1 = mt25066_now_ns();
        targ->stats.total_latency_ns += (t1 - t0);
        targ->stats.messages += 1;
        targ->stats.bytes += targ->msg_size;
    }

    free(send_buf);
    free(recv_buf);
    close(fd);
    return NULL;
}

int main(int argc, char **argv) {
    if (argc != 6) {
        fprintf(stderr, "Usage: %s <server_ip> <port> <message_size> <threads> <duration_sec>\n", argv[0]);
        return 1;
    }

    const char *server_ip = argv[1];
    int port = atoi(argv[2]);
    size_t msg_size = (size_t)strtoul(argv[3], NULL, 10);
    int threads = atoi(argv[4]);
    int duration_sec = atoi(argv[5]);

    if (port <= 0 || msg_size == 0 || threads <= 0 || duration_sec <= 0) {
        fprintf(stderr, "Invalid arguments.\n");
        return 1;
    }

    pthread_t *tids = (pthread_t *)calloc((size_t)threads, sizeof(pthread_t));
    mt25066_thread_arg_t *args = (mt25066_thread_arg_t *)calloc((size_t)threads, sizeof(mt25066_thread_arg_t));
    if (!tids || !args) {
        free(tids);
        free(args);
        return 1;
    }

    for (int i = 0; i < threads; ++i) {
        args[i].server_ip = server_ip;
        args[i].port = port;
        args[i].msg_size = msg_size;
        args[i].duration_ns = (uint64_t)duration_sec * 1000000000ull;
        args[i].stats.bytes = 0;
        args[i].stats.messages = 0;
        args[i].stats.total_latency_ns = 0;
        pthread_create(&tids[i], NULL, mt25066_client_thread, &args[i]);
    }

    uint64_t total_bytes = 0;
    uint64_t total_messages = 0;
    uint64_t total_latency_ns = 0;

    for (int i = 0; i < threads; ++i) {
        pthread_join(tids[i], NULL);
        total_bytes += args[i].stats.bytes;
        total_messages += args[i].stats.messages;
        total_latency_ns += args[i].stats.total_latency_ns;
    }

    double duration = (double)duration_sec;
    double throughput_gbps = (total_bytes * 8.0) / (duration * 1e9);
    double avg_latency_us = total_messages ? (double)total_latency_ns / (double)total_messages / 1000.0 : 0.0;

    printf("TOTAL_BYTES=%lu TOTAL_MESSAGES=%lu AVG_LATENCY_US=%.3f THROUGHPUT_GBPS=%.6f\n",
           (unsigned long)total_bytes,
           (unsigned long)total_messages,
           avg_latency_us,
           throughput_gbps);

    free(tids);
    free(args);
    return 0;
}

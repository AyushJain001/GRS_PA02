#include "MT25066_Part_A_Common.h"

#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <time.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>

mt25066_message_t *mt25066_message_create(size_t total_size) {
    mt25066_message_t *msg = (mt25066_message_t *)calloc(1, sizeof(mt25066_message_t));
    if (!msg) {
        return NULL;
    }

    msg->total_size = total_size;
    size_t base = total_size / MT25066_FIELDS;
    size_t rem = total_size % MT25066_FIELDS;

    for (int i = 0; i < MT25066_FIELDS; ++i) {
        size_t sz = base + (i == MT25066_FIELDS - 1 ? rem : 0);
        msg->field_sizes[i] = sz;
        msg->fields[i] = (char *)malloc(sz);
        if (!msg->fields[i]) {
            mt25066_message_destroy(msg);
            return NULL;
        }
    }

    return msg;
}

void mt25066_message_fill(mt25066_message_t *msg, uint8_t seed) {
    if (!msg) {
        return;
    }
    for (int i = 0; i < MT25066_FIELDS; ++i) {
        memset(msg->fields[i], (int)(seed + i), msg->field_sizes[i]);
    }
}

void mt25066_message_flatten(const mt25066_message_t *msg, char *buffer) {
    size_t offset = 0;
    for (int i = 0; i < MT25066_FIELDS; ++i) {
        memcpy(buffer + offset, msg->fields[i], msg->field_sizes[i]);
        offset += msg->field_sizes[i];
    }
}

struct iovec *mt25066_message_iov(const mt25066_message_t *msg) {
    struct iovec *iov = (struct iovec *)calloc(MT25066_FIELDS, sizeof(struct iovec));
    if (!iov) {
        return NULL;
    }
    for (int i = 0; i < MT25066_FIELDS; ++i) {
        iov[i].iov_base = msg->fields[i];
        iov[i].iov_len = msg->field_sizes[i];
    }
    return iov;
}

void mt25066_message_destroy(mt25066_message_t *msg) {
    if (!msg) {
        return;
    }
    for (int i = 0; i < MT25066_FIELDS; ++i) {
        free(msg->fields[i]);
        msg->fields[i] = NULL;
    }
    free(msg);
}

ssize_t mt25066_send_all(int fd, const void *buf, size_t len) {
    const char *ptr = (const char *)buf;
    size_t remaining = len;
    while (remaining > 0) {
        ssize_t sent = send(fd, ptr, remaining, 0);
        if (sent < 0) {
            if (errno == EINTR) {
                continue;
            }
            return -1;
        }
        if (sent == 0) {
            break;
        }
        remaining -= (size_t)sent;
        ptr += sent;
    }
    return (ssize_t)(len - remaining);
}

ssize_t mt25066_recv_all(int fd, void *buf, size_t len) {
    char *ptr = (char *)buf;
    size_t remaining = len;
    while (remaining > 0) {
        ssize_t recvd = recv(fd, ptr, remaining, 0);
        if (recvd < 0) {
            if (errno == EINTR) {
                continue;
            }
            return -1;
        }
        if (recvd == 0) {
            break;
        }
        remaining -= (size_t)recvd;
        ptr += recvd;
    }
    return (ssize_t)(len - remaining);
}

uint64_t mt25066_now_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ull + (uint64_t)ts.tv_nsec;
}

int mt25066_set_nodelay(int fd) {
    int flag = 1;
    return setsockopt(fd, IPPROTO_TCP, TCP_NODELAY, &flag, sizeof(flag));
}

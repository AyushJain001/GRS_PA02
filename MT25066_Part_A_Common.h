#ifndef MT25066_PART_A_COMMON_H
#define MT25066_PART_A_COMMON_H

#include <stdint.h>
#include <stddef.h>
#include <sys/uio.h>

#define MT25066_FIELDS 8

typedef struct {
    char *fields[MT25066_FIELDS];
    size_t field_sizes[MT25066_FIELDS];
    size_t total_size;
} mt25066_message_t;

typedef struct {
    uint64_t bytes;
    uint64_t messages;
    uint64_t total_latency_ns;
} mt25066_stats_t;

mt25066_message_t *mt25066_message_create(size_t total_size);
void mt25066_message_fill(mt25066_message_t *msg, uint8_t seed);
void mt25066_message_flatten(const mt25066_message_t *msg, char *buffer);
struct iovec *mt25066_message_iov(const mt25066_message_t *msg);
void mt25066_message_destroy(mt25066_message_t *msg);

ssize_t mt25066_send_all(int fd, const void *buf, size_t len);
ssize_t mt25066_recv_all(int fd, void *buf, size_t len);

uint64_t mt25066_now_ns(void);
int mt25066_set_nodelay(int fd);

#endif

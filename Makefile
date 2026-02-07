# MT25066
#ayush jain
CC=gcc
CFLAGS=-O2 -Wall -Wextra -pthread
LDFLAGS=-pthread

COMMON=MT25066_Part_A_Common.c

all: MT25066_Part_A1_Server MT25066_Part_A1_Client \
     MT25066_Part_A2_Server MT25066_Part_A2_Client \
     MT25066_Part_A3_Server MT25066_Part_A3_Client

MT25066_Part_A1_Server: MT25066_Part_A1_Server.c $(COMMON)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

MT25066_Part_A1_Client: MT25066_Part_A1_Client.c $(COMMON)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

MT25066_Part_A2_Server: MT25066_Part_A2_Server.c $(COMMON)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

MT25066_Part_A2_Client: MT25066_Part_A2_Client.c $(COMMON)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

MT25066_Part_A3_Server: MT25066_Part_A3_Server.c $(COMMON)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

MT25066_Part_A3_Client: MT25066_Part_A3_Client.c $(COMMON)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

clean:
	rm -f MT25066_Part_A1_Server MT25066_Part_A1_Client \
	      MT25066_Part_A2_Server MT25066_Part_A2_Client \
	      MT25066_Part_A3_Server MT25066_Part_A3_Client \
	      *.o *.perf

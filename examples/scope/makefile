BINS=static nested undeclared

all: $(BINS)

%: %.c
	gcc -Wall -Wextra -o $@ $<

clean:
	rm -f $(BINS)

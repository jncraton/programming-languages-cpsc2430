all:

%: %.c
	gcc -Wall -Wextra $< -o $@

%: %.cc
	g++ -Wall -Wextra $< -o $@

%: %.rs
	rustc $<

clean:
	rm -f error crash poly

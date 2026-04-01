all:

%: %.c
	gcc -Wall -Wextra $< -o $@

%: %.cc
	g++ -Wall -Wextra $< -o $@

%: %.rs
	# apt install rustc cargo
	rustc $<

clean:
	rm -f error crash poly option eq void

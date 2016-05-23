import sys

s = set()
for line in sys.stdin:
	word = line.strip()
	s.add(word)

print s
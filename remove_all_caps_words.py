import re
import fileinput

caps = re.compile('^[A-Z\[]+[\']?[A-Z.?!,;\]]$|^[A-Z]$')
for line in fileinput.input():
	words = line.split()
	for w in words:
		if not caps.match(w): print w,

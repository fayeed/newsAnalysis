import csv
import sys

filename = sys.argv[1]
outputfilename = sys.argv[2]

output = [['content', 'emotion']]

with open('{}'.format(filename)) as file:
  content = [line.rstrip('\n') for line in file]
  for row in content:
    s = row.split(". ")
    output.append(s)

with open('{}'.format(outputfilename)) as file:
  writer = csv.writer(file)
  writer.writerows(output)


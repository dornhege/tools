#!/usr/bin/env python
from __future__ import with_statement

import sys

filter_cmd = "echo"

def parse_top(file):
    lines = []
    with open(file) as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            lines.append(line)
    return lines

def parseHeader(lines):
    assert(lines[0].startswith("top"))
    lines = lines[1:]
    assert(lines[0].startswith("Tasks"))
    lines = lines[1:]
    assert(lines[0].startswith("Cpu"))
    lines = lines[1:]
    assert(lines[0].startswith("Mem"))
    lines = lines[1:]
    assert(lines[0].startswith("Swap"))
    lines = lines[1:]
    return lines

def parseData(lines):
    headers = lines[0].split()
    lines = lines[1:]
    ret = []
    count = 0
    while len(lines) > count and not lines[count].startswith("top"):
        if lines[count].find(filter_cmd) == -1:     # prefilter lines that cannot contain filter_cmd
           count += 1
           continue
        entries = lines[count].split()
        assert(len(entries) == len(headers))
        tupels = zip(headers, entries)
        ret.append(dict(tupels))
        count += 1
        #lines = lines[1:]
    return (lines[count:], ret)

def evalEntry(entry):
    def filter_fn(e):
        return e["COMMAND"] == filter_cmd
    hit = filter(filter_fn, entry)
    if len(hit) == 0:
        return (False, 0, 0, 0)
    assert(len(hit) == 1)
    #print hit[0]
    ok = True
    if len(hit[0]["%CPU"]) == 0:
      ok = False
    if len(hit[0]["%MEM"]) == 0:
      ok = False
    if len(hit[0]["DATA"]) == 0:
      ok = False
    if hit[0]["DATA"] == "0":
      ok = False
    return (ok, hit[0]["%CPU"], hit[0]["%MEM"], hit[0]["DATA"])
        

if len(sys.argv) < 3:
    print "Usage: parse_top <top_output_file> <process>"
    sys.exit(1)

top_file = sys.argv[1]
filter_cmd = sys.argv[2]
print "Reading Top output from: " + top_file
lines = parse_top(top_file)
print "Read " + str(len(lines)) + " lines"
result = []
count = 0
while len(lines) > 0:
    lines = parseHeader(lines)
    #print "parsed hdr"
    (lines, res) = parseData(lines)
    #print "parsed data"
    result.append(res)
    count += 1
    if count % 20 == 0:
      print "Parsed " + str(count) + " entries"

print "Read " + str(len(result)) + " entries"

cpus = []
mem_percs = []
mem_abss = []  
for i in result:
    (ok, cpu, mem_perc, mem_abs) = evalEntry(i)
    if not ok:
      continue
    cpus.append(float(cpu))
    mem_percs.append(float(mem_perc))
    mem_abss.append(float(mem_abs[0:-1]))   # remove 'm' from 156m
max_cpu = reduce(max, cpus)
max_mem_perc = reduce(max, mem_percs)
max_mem_abs = reduce(max, mem_abss)
print "CPU avg: " + str(sum(cpus)/len(cpus)) + " max: " + str(max_cpu)
print "mem_perc avg: " + str(sum(mem_percs)/len(mem_percs)) + " max: " + str(max_mem_perc)
print "mem abs avg: " + str(sum(mem_abss)/len(mem_abss)) + " max: " + str(max_mem_abs)

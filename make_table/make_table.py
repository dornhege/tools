#!/usr/bin/env python
import sys
from functools import partial

use_columns = range(1000)
column_process = {}


def make_float(entry, precision):
    conv_str = "%." + precision + "f"
    return conv_str % float(entry)

def load_data(filename):
    rows = []
    with open(filename) as f:
        for line in f:
            row = line.split()
            rows.append(row)
    return rows

def process_data(data):
    processed_data = []
    for row in data:
        processed_row = []
        for (i, entry) in enumerate(row):
            if not i in use_columns:
                continue
            processed = entry
            if i in column_process:
                processed = column_process[i](entry)
            processed_row.append(processed)
        processed_data.append(processed_row)
    return processed_data

def write_data(data):
    for row in data:
        first = True
        for col in row:
            if not first:
                print " & ",
            print col,
            first = False
        print "\\\\"

def make_eval(x, proc):
    data = float(x)
    return eval(proc)

def load_process(proc_desc):
    global use_columns
    global column_process

    procs = proc_desc.split(":")
    for (i, proc) in enumerate(procs):
        if not proc:
            use_columns.remove(i)
            continue
        if proc == "id":
            if i in column_process:
                del column_process[i]
            continue
        if proc.startswith("make_float"):
            prec = proc[len("make_float"):]
            column_process[i] = partial(make_float, precision=prec)
        else:
            column_process[i] = partial(make_eval, proc=proc)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        load_process(sys.argv[2])

    #print column_process

    data = load_data(sys.argv[1])
    #print data
    proc = process_data(data)
    #print proc
    write_data(proc)

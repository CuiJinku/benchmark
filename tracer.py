#!/usr/bin/env python3
import os
import io
import sys
import trace

NUMPY = "numpy"

# create a Trace object, telling it what to ignore, and whether to
# do tracing or line-counting or both.
tracer = trace.Trace(
    count=-1,
    trace=-1,
    countfuncs=0,
    countcallers=-1,
    ignoredirs=[sys.prefix, sys.exec_prefix],
)

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('progname', nargs='?',
        help='file to run as main program')
parser.add_argument('arguments', nargs=argparse.REMAINDER,
        help='arguments to the program')

opts = parser.parse_args()
print(opts.progname)
print(opts.arguments)

try:
    sys.argv = [opts.progname, *opts.arguments]
    sys.path[-1] = os.path.dirname(opts.progname)

    with io.open_code(opts.progname) as fp:
        code = compile(fp.read(), opts.progname, 'exec')
    # try to emulate __main__ namespace as much as possible
    globs = {
        '__file__': opts.progname,
        '__name__': '__main__',
        '__package__': None,
        '__cached__': None,
    }
    tracer.runctx(code, globs, globs)
except OSError as err:
    sys.exit("Cannot run file %r because: %s" % (sys.argv[-1], err))
except SystemExit:
    pass


# make a report, placing output in the current directory
r = tracer.results()
# r.write_results(show_missing=True, coverdir=".")
if r.calledfuncs:
    print()
    print("functions called:")
    calls = r.calledfuncs
    for filename, modulename, funcname in sorted(calls):
        if NUMPY in filename or NUMPY in modulename or NUMPY in funcname:
            print(("filename: %s, modulename: %s, funcname: %s"
               % (filename, modulename, funcname)))

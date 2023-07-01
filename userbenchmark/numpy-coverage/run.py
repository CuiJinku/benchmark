#!/usr/bin/env python2
import os
import io
import sys
import trace
from datetime import datetime
from typing import List
import sys



# `list`: This is a built-in Python type and, starting from Python 3.9, 
# you can use it in type annotations to indicate a list of a specific type, 
# like list[str] for a list of strings.
def run(args: list[str]):
    progname = os.path.dirname(os.path.abspath(__file__)) + '/_run.py'

    # create a Trace object, telling it what to ignore, and whether to
    # do tracing or line-counting or both.
    tracer = trace.Trace(
        count=-1,
        trace=-1,
        countfuncs=0,
        countcallers=-1,
        ignoredirs=[sys.prefix, sys.exec_prefix],
    )
    
    try:
        sys.argv = [progname, *args]
        # sys.path[-1] = os.path.dirname(progname)

        with io.open_code(progname) as fp:
            code = compile(fp.read(), progname, 'exec')
        # try to emulate __main__ namespace as much as possible
        globs = {
            '__file__': progname,
            '__name__': '__main__',
            '__package__': None,
            '__cached__': None,
        }

        tracer.runctx(code, globs, globs)

    except OSError as err:
        sys.exit("Cannot run file %r because: %s" % (sys.argv[-1], err))
    except SystemExit:
        print("SystemExit")
        pass

    NUMPY = "numpy"

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



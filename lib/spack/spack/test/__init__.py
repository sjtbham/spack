import sys
import unittest

import spack
from spack.colify import colify
import spack.tty as tty

test_names = ['versions',
              'url_parse',
              'stage',
              'spec_syntax',
              'spec_dag',
              'concretize']


def list_tests():
    return test_names


def run(names, verbose=False):
    verbosity = 1 if not verbose else 2

    if not names:
        names = test_names
    else:
        for test in names:
            if test not in test_names:
                tty.error("%s is not a valid spack test name." % test,
                          "Valid names are:")
                colify(test_names, indent=4)
                sys.exit(1)

    runner = unittest.TextTestRunner(verbosity=verbosity)

    testsRun = errors = failures = skipped = 0
    for test in names:
        module = 'spack.test.' + test
        suite = unittest.defaultTestLoader.loadTestsFromName(module)

        tty.msg("Running test: %s" % test)
        result = runner.run(suite)
        testsRun += result.testsRun
        errors   += len(result.errors)
        failures += len(result.failures)
        skipped  += len(result.skipped)

    succeeded = not errors and not failures
    tty.msg("Tests Complete.",
            "%5d tests run" % testsRun,
            "%5d skipped" % skipped,
            "%5d failures" % failures,
            "%5d errors" % errors)

    if not errors and not failures:
        tty.info("OK", format='g')
    else:
        tty.info("FAIL", format='r')
        sys.exit(1)
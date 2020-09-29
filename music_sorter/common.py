#!/usr/bin/env python3

import argparse
import sys

def practise_or_debug_message(message):
    if True:#practise
        sys.stdout.write('practise: %s\n' % message)
        return True
    elif True:#debug
        sys.stdout.write('practise: %s\n' % message)

    return False


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)
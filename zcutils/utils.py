###########################################################################
# author: JanKalin
#
# General utilities
###########################################################################

import sys

###########################################################################
# Progress indicator
###########################################################################

class Progress:
    """Progress indicator"""

    def __init__(self, value=0, fmt="{}", max_value=0):
        """Sets max value and prints out first line. The format should be without the \\r"""
        self.max_value = max_value
        self.value = value
        self.prev = 0
        self.fmt = "\r" + fmt
        print self.fmt.format(self.value),
        sys.stdout.flush()

    def step(self):
        self.value += 1
        if not self.max_value:
            print self.fmt.format(self.value),
            sys.stdout.flush()
        else:
            self.now = int(round(100*self.value/self.max_value))
            if not self.now == self.prev:
                print self.fmt.format(self.now),
                sys.stdout.flush()
                self.prev = self.now
            if self.value == self.max_value:
                self.done()

    def done(self):
        print
            


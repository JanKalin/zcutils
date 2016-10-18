###########################################################################
# author: JanKalin
#
# Simple python interface to zcash-cli
###########################################################################

import json
import subprocess

###########################################################################

class zcli:
    """Interface

    This object defines the interface
    """
    def __init__(self, zcli):
        """Constructor

        Args:
            zcli: path to zcash-cli
        """
        self.zcli = zcli


    def _call(self, args):
        """Calls zcash-cli and returns result

        Not intended to be called directly
        """
        cmd = "{} {}".format(self.zcli, args)
        buf = subprocess.check_output(cmd,
                                      universal_newlines=True, shell=True,
                                      stderr=subprocess.STDOUT)
        return json.loads(buf, strict=False) if buf[0] in ['[', '{'] else buf.strip()


    def listtransactions(self, count):
        """Calls listtransactions to get last `count` transactions"""
        return self._call('listtransactions "" {}'.format(count))
                         
    def getblock(self, blockhash):
        """Calls listtransactions to get last `count` transactions"""
        return self._call('getblock {}'.format(blockhash))
                         

#!/usr/bin/python3.5
# EASY-INSTALL-ENTRY-SCRIPT: 'b2share','console_scripts','b2share'
__requires__ = 'b2share'
import re
import sys
sys.path.insert(0, "/build/b2share")
sys.path.insert(0, "/build/b2share/demo")
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('b2share', 'console_scripts', 'b2share')()
    )

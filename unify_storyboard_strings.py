#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# MIT Licence
#
# Copyright (C) 2012 Pierre Dulac
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and 
# associated documentation files (the "Software"), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial 
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Unify Storyboard strings and Localizable.strings

Steps for unification:

    1. Convert Storyboard Strings file into a Localizable strings format 
        which means go from something like

            /* Class = "IBUINavigationItem"; title = "New event"; ObjectID = "166"; */
            "166.title" = "Neues Ereignis";

        to something like

            /* No comment provided by engineer. */
            "New Event" = "Neues Ereignis";

    2. Merge the original Loclizable.strings file with the converted storyboad one
        Thanks to the pygenstrings module

    3. Cleanup useless files
"""

from sys import argv
from codecs import open
from re import compile, sub
from copy import copy
import os
import shutil
import optparse
import logging

FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('unify')
logger.level = logging.INFO

from pygenstrings.genstring import LocalizedString, LocalizedFile

__version__ = "0.1"
__license__ = "MIT"

USAGE = "%prog [options] <storyboard string file>"
VERSION = "%prog v" + __version__

STRINGS_FILE = 'Localizable.strings'

re_translation = compile(r'^"((?:[^"]|\\")+)" = "((?:[^"]|\\")+)";(?:\n)?$')
re_comment_single = compile(r'^/\* Class = "[^"]+"; [a-z]+ = "([^"]+)"; ObjectID = "[^"]+"; \*/$')
re_comment_start = compile(r'^/\*.*$')
re_comment_end = compile(r'^.*\*/$')

class StoryboardStringFile(LocalizedFile):
     
    def read_from_file(self, fname=None):
        self.reset()

        fname = self.fname if fname == None else fname
        try:
            f = open(fname, encoding='utf_8', mode='r')
        except:
            print 'File %s does not exist.' % fname
            exit(-1)
        
        try:
            line = f.readline()

            # to avoid the empty lines at the beginning of the file
            while not line.strip():
                line = f.readline()

            logger.debug(line)
        except:
            logger.error("Can't read line for file: %s" % fname)
            raise

        i = 1
        while line:
            comments = ["/* No comment provided by engineer. */\n"]
            original_text = "<No Text>"

            if not re_comment_single.match(line):
                while line and not re_comment_end.match(line):
                    line = f.readline()
                    comments.append(line)
                    logger.warning(" ! \tStrange comment on multiple line... not supposed to happen")
            else:
                m = re_comment_single.match(line)
                original_text = m.group(1)
        
            line = f.readline()
            i += 1

            # handle multi lines
            while len(line) > 1 and line[-1] != u';' and line[-2] != u';':
                line += f.readline()
                i += 1

            logger.debug("%d %s" % (i, line.rstrip('\n')))
            if line and re_translation.match(line):
                translation = line
            else:
                logger.error("Line %d raising the exception: %s" % (i, line))
                raise Exception('invalid file')
 
            # convert the format of the translation
            translation = '"%s" = "%s";\n' % (original_text, re_translation.match(line).group(2))

            line = f.readline()
            i += 1
            while line and line == u'\n':
                line = f.readline()
                i += 1

            string = LocalizedString(comments, translation)
            self.strings.append(string)
            self.strings_d[string.key] = string
 
        f.close()

def _puts_header(message):
    logger.info("\t%s" % message)

def _puts(message):
    logger.info("\t\t------> %s" % message)

def unify(storyboard_strings_file, localizable_strings_file):
    """
    Handle the unification steps
    """
    new_filename = localizable_strings_file + '.new'
    old_filename = localizable_strings_file
    merged_filename = localizable_strings_file + '.merged'

    # step 1
    _puts_header("Conversion")
    new_file = StoryboardStringFile(storyboard_strings_file, auto_read=True)
    _puts("done")
    new_file.save_to_file(new_filename)
    _puts("new file saved")
    new_file.read_from_file()
    _puts("read again the file to update strings lookup tables")

    # step 2
    _puts_header("Merge")
    old_file = LocalizedFile(localizable_strings_file, auto_read=True)
    _puts("old file read")
    merged_file = LocalizedFile()
    merged_file.update_with(old_file)
    merged_file.update_with(new_file)
    _puts("merged file updated with new file")
    merged_file.save_to_file(merged_filename)
    _puts("merged file saved")

    # do some cleanup
    _puts_header("Cleanup")
    os.rename(merged_filename, old_filename)
    os.remove(new_filename)
    _puts("done")

def parse_options():
    """parse_options() -> opts, args

    Parse any command-line options given returning both
    the parsed options and arguments.
    """
    parser = optparse.OptionParser(usage=USAGE, version=VERSION)

    parser.add_option("-d", "--debug",
            action="store_true", default=False, dest="debug",
            help="Set to DEBUG the logging level (default to INFO)")

    parser.add_option("-l", "--localizable-strings-file",
            action="store", default=False, dest="localizable_strings_file",
            help="If no file is specified then the script search for a file called '%s' \
                in the same directory of the <storyboard strings file>" % STRINGS_FILE)

    opts, args = parser.parse_args()
    return opts, args

if __name__ == '__main__':
    opts, args = parse_options()
    if opts.debug:
        logger.level = logging.DEBUG
    if len(args) == 0:
        logger.error("You need to specify the storyboard string file path")
        exit(1)
    else:
        storyboard_strings_file = args[0]
        if not opts.localizable_strings_file:
            opts.localizable_strings_file = os.path.join(os.path.dirname(storyboard_strings_file), STRINGS_FILE)
        if not os.path.exists(opts.localizable_strings_file):
            logger.error("The localizable strings file does not exists at path \n\t'%s'" % opts.localizable_strings_file)
            exit(1)

    logging.info("\n\tRunning the script for storyboard string file \n\t\t------> %s \n\tand localizable strings file \n\t\t------> %s" % (storyboard_strings_file, opts.localizable_strings_file))
    unify(storyboard_strings_file, opts.localizable_strings_file)

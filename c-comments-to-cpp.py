#!/usr/bin/python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
"""
  Copyright (C) 2017 Marcus Geelnard

  This software is provided 'as-is', without any express or implied
  warranty.  In no event will the authors be held liable for any damages
  arising from the use of this software.

  Permission is granted to anyone to use this software for any purpose,
  including commercial applications, and to alter it and redistribute it
  freely, subject to the following restrictions:

  1. The origin of this software must not be misrepresented; you must not
     claim that you wrote the original software. If you use this software
     in a product, an acknowledgment in the product documentation would be
     appreciated but is not required.
  2. Altered source versions must be plainly marked as such, and must not be
     misrepresented as being the original software.
  3. This notice may not be removed or altered from any source distribution.
"""

import argparse, fileinput

# Handle the program arguments.
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description='Convert C-style comments to C++-style.')
args = parser.parse_args()

inside_c_comment = False
comment_style = '//'

for line in fileinput.input():
    out_line = ''
    inside_string = False
    inside_indentation = True
    k = 0
    while k < len(line):
        if inside_indentation and not (line[k] in [' ', '\t']):
            inside_indentation = False
            if inside_c_comment:
                if line[k] == '*' and ((k + 1) == len(line) or line[k + 1] != '/'):
                    k += 1
                out_line += comment_style

        if inside_string:
            assert(k > 0)
            if line[k] == '"' and line[k - 1] != '\\':
                inside_string = False
            out_line += line[k]
            k += 1
        else:
            if inside_c_comment:
                if line[k] == '*' and (k + 1) < len(line) and line[k + 1] == '/':
                    inside_c_comment = False
                    out_line += '\n'
                    k += 2
                else:
                    out_line += line[k]
                    k += 1
            else:
                if line[k] == '/' and (k + 1) < len(line) and line[k + 1] == '*':
                    # Start of C style comment.
                    inside_c_comment = True
                    comment_style = '//'
                    k += 2
                    if k < len(line) and (line[k] == '*' or line[k] == '!'):
                        # Start of Doxygen comment.
                        comment_style = '///'
                        k += 1
                    out_line += comment_style
                elif line[k] == '/' and (k + 1) < len(line) and line[k + 1] == '/':
                    # Start of C++ style comment.
                    out_line += line[k:]
                    k = len(line)
                else:
                    if line[k] == '"':
                        inside_string = True
                    out_line += line[k]
                    k += 1

    # Strip trailing whitespace (including newline chars).
    out_line = out_line.rstrip()

    print '%s\n' % (out_line),


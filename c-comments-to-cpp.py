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
comment_indent = 0

for line in fileinput.input():
    # Start by dropping trailing whitespace from the input.
    line = line.rstrip()

    out_line = ''
    inside_string = False
    inside_indentation = True
    start_or_end_line = False
    k = 0
    while k < len(line):
        if inside_string:
            assert(k > 0)
            if line[k] == '"' and line[k - 1] != '\\':
                inside_string = False
            out_line += line[k]
            k += 1
        else:
            if inside_c_comment:
                if inside_indentation:
                    if (k >= comment_indent) or not (line[k] in [' ', '\t']):
                        inside_indentation = False
                        out_line += comment_style
                        # Consume up to len(comment_style) chars from the line.
                        for m in xrange(k, min(k + len(comment_style), len(line))):
                            if line[m] in [' ', '\t']:
                                k += 1
                            elif line[m] == '*' and ((m + 1) == len(line) or line[m + 1] != '/'):
                                k += 1
                            else:
                                break
                        if k < len(line) and not (line[k] in [' ', '\t', '*']):
                            out_line += ' '
                if k < len(line):
                    if line[k] == '*' and (k + 1) < len(line) and line[k + 1] == '/':
                        inside_c_comment = False
                        start_or_end_line = True
                        if k > 0 and line[k - 1] == '*':
                            # Replace '*/' with '**' in case this is a '...*****/'-style line.
                            out_line += '**'
                        out_line += '\n'
                        k += 2
                    else:
                        out_line += line[k]
                        k += 1
            else:
                if line[k] == '/' and (k + 1) < len(line) and line[k + 1] == '*':
                    # Start of C style comment.
                    comment_indent = k
                    inside_c_comment = True
                    start_or_end_line = True
                    comment_style = '//'
                    k += 2
                    if k < len(line) and (line[k] == '*' or line[k] == '!'):
                        if (k + 1) >= len(line) or line[k + 1] != '*':
                            # Start of Doxygen comment.
                            comment_style = '///'
                            k += 1
                            if k < len(line) and line[k] == '<':
                                # Start of Doxygen after-member comment.
                                comment_style = '///<'
                                k += 1
                    out_line += comment_style
                    inside_indentation = False
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

    # Empty start/stop line?
    if (not start_or_end_line) or len(out_line.lstrip()) != len(comment_style):
        print '%s\n' % (out_line),


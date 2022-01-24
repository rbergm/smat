#!/usr/bin/env python3

import argparse
import re
import textwrap
import sys
from typing import List


def read_stdin() -> List[str]:
    return [line.rstrip("\n") for line in sys.stdin.readlines()]


def read_file(src: str) -> List[str]:
    contents = []
    with open(src, "r") as file:
        contents = file.readlines()
    return [line.rstrip("\n") for line in contents]


def write_stdout(output: List[str]) -> None:
    for line in output:
        print(line)


def write_file(output: List[str], target: str) -> None:
    with open(target, "w") as file:
        file.writelines(output)


def shrink(text: List[str], *, prefix: str, suffix: str) -> List[str]:
    result = text
    if prefix:
        prefix_re = re.compile("^" + prefix)
        result = [re.sub(prefix_re, "", line) for line in result]
    if suffix:
        suffix_re = re.compile(suffix + "$")
        result = [re.sub(suffix_re, "", line) for line in result]
    return result


def expand(text: List[str], *, prefix: str, suffix: str) -> List[str]:
    return [prefix + line + suffix for line in text]


def smat(text: List[str], *, add_prefix="", drop_prefix="", add_suffix="", drop_suffix="") -> List[str]:
    shrinked = shrink(text, prefix=drop_prefix, suffix=drop_suffix)
    expanded = expand(shrinked, prefix=add_prefix, suffix=add_suffix)
    return expanded


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent("""\
        Utility to add and remove prefixes as well as suffixes from strings.

        By default, this tool will read from stdin and write to stdout, but can read/write from files as well.
        Processing takes place on a per-line basis, dropping prefixes/suffixes first and then adding the new ones.
        Smat uses Python regular expressions and will apply them as part of drop statements."""))
    parser.add_argument("--drop-prefix", "-dp", action="store", help="Prefix to remove from all matching strings", default="", metavar="drop_prefix")
    parser.add_argument("--add-prefix", "-ap", action="store", help="Prefix to add to all strings", default="", metavar="add_prefix")
    parser.add_argument("--drop-suffix", "-ds", action="store", help="Suffix to remove from all matching strings", default="", metavar="drop_suffix")
    parser.add_argument("--add-suffix", "-as", action="store", help="Suffix to add to all strings", default="", metavar="add_suffix")
    parser.add_argument("--input", "-i", action="store", help="Read from given file instead of stdin")
    parser.add_argument("--output", "-o", action="store", help="Write to given file instead of stdout")

    args = parser.parse_args()

    if not (args.drop_prefix or args.drop_suffix or args.add_prefix or args.add_suffix):
        parser.error("No action given, add at least one of -dp, -ap, -ds or -as")

    text = read_file(args.input) if args.input else read_stdin()

    result = smat(text, add_prefix=args.add_prefix, drop_prefix=args.drop_prefix, add_suffix=args.add_suffix, drop_suffix=args.drop_suffix)

    if args.output:
        write_file(result, args.output)
    else:
        write_stdout(result)


if __name__ == "__main__":
    main()

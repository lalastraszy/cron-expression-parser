#!/usr/bin/env python3
import re
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


class Parser:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def run(self, exr):
        self._validate_numbers(exr)

        joker_match = re.match('^\*$', exr)
        if joker_match:
            return self._generate_range()

        separate_match = re.match('^(\d+,?)+$', exr)
        if separate_match:
            return separate_match.group(0).replace(',', ' ')

        rage_match = re.match('^(\d+)-(\d+)$', exr)
        if rage_match:
            return self._generate_range(int(rage_match.group(1)), int(rage_match.group(2)))

        step_match = re.match('^(\*|\d+)/(\d+)$', exr)
        if step_match:
            return self._generate_range(
                self.min if step_match.group(1) == '*' else int(step_match.group(1)),
                step=int(step_match.group(2)))

        raise Exception('Invalid cron expression: {}'.format(exr))

    def _generate_range(self, start=None, end=None, step=1):
        start = self.min if not start else start
        end = self.max if not end else end
        return ' '.join([str(i) for i in range(start, end + 1, step)])

    def _validate_numbers(self, exr):
        for number in re.findall('(\d+)', exr):
            if self.min <= int(number) <= self.max:
                continue
            raise Exception('Invalid value {} for field {}'.format(number, self.name))


class Formatter:
    def __init__(self, field_name_size):
        self.field_name_size = field_name_size

    def print(self, name, value):
        print('{}{}{}'.format(name, ' ' * (self.field_name_size - len(name)), value))


def parse(args):
    f = Formatter(14)
    f.print('minute', Parser(0, 59).run(args.min))
    f.print('hour', Parser(0, 24).run(args.hour))
    f.print('day of month', Parser(1, 31).run(args.dom))
    f.print('month', Parser(1, 12).run(args.month))
    f.print('day of week', Parser(1, 7).run(args.dow))
    f.print('command', args.cmd)


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Cron expression parser",
        formatter_class=ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('min', help='minute (allowed values: 0-59, allowed special characters: , - * /)')
    parser.add_argument('hour', help='hour (allowed values: 0-24, allowed special characters: , - * /)')
    parser.add_argument('dom', help='day of month (allowed values: 1-31, allowed special characters: , - * /)')
    parser.add_argument('month', help='month (allowed values: 1-12, allowed special characters: , - * /)')
    parser.add_argument('dow', help='day of week (allowed values: 1-7, allowed special characters: , - * /)')
    parser.add_argument('cmd', help='command')
    parse(parser.parse_args())

"""Main file."""
import sys
import time
import argparse

import data_input
import data_output
import network
import utils


def main(args: argparse.Namespace):
    """Main function.

    Big and maybe scary, but simple: bring all logic together and do the job.
    It's big only because of prints in fact :)
    """

    data = data_input.Reader.read(args.connection_string)
    invalid = list(filter(lambda value: not value.get('valid'), data.values()))
    valid = list(filter(lambda value: value.get('valid'), data.values()))
    if len(invalid) and not args.force:
        print('Program input contains invalid values, that unable to parse.')
        print('Use --skip_invalid parameter to skip it, or fix your input file')
        print('invalid values (first index = 1): ')
        for val in invalid:
            print(f'element #{val.get("idx") + 1} ', end='')
            print(f'host={val.get("host") or "``"} | ', end='')
            print(f'ports={",".join(val.get("ports"))}')
        exit(0)
    writer = data_output.StdPrintWriter()
    plug = '???'
    while True:
        writer.write('Check results' +
                     (' for new iteration:' if args.infinite else ':'))
        for host_settings in valid:
            network.check(**host_settings)
            for result in network.check(**host_settings):
                if ip := result.get('ip'):
                    host = result.get('host')
                    host = host if not utils.is_ip(host) else plug
                    status = result.get('status')
                    match status:
                        case 1:
                            status = 'opened'
                        case 0:
                            status = 'Closed'
                        case None:
                            status = 'Address pingable.'
                    writer.write(
                        f"{result.get('time')} |"
                        f" {host} |"
                        f" {ip} | {result.get('rtt')} ms "
                        f"| {result.get('port') or plug} | "
                        f"{status}"
                    )
                else:
                    writer.write(
                        f"{result.get('time')} |"
                        f" {result.get('host')} |"
                        f" {plug}  | 0 ms | {result.get('port') or plug} | "
                        f"Hostname not resolved."
                    )
        if not args.infinite:
            break
        time.sleep(int(args.period))


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        prog='avasite',
        description='Site availability checker'
    )
    arg_parser.add_argument(
        '--inp',
        dest='connection_string',
        default='csv:input.csv',
        help='Input string. looks like "con_type:path."'
             '\nCurrently available protocols are: ' +
             ', '.join(data_input.Reader.get_all_protocols()) +
             '\n E.G csv:input.csv or json:files/inp.json '
             '(DEFAULT: csv::input.csv)'
    )
    arg_parser.add_argument(
        '--inf',
        dest='infinite',
        action='store_true',
        help='Run program infinitely, till someone stop it.'
    )
    arg_parser.add_argument(
        '--period',
        dest='period',
        default=180,
        action='store',
        help='Period of availability check in seconds. Is used only with --inf.'
    )
    arg_parser.add_argument(
        '--skip_invalid',
        dest='force',
        action='store_true',
        help='Skip invalid input. If provided, invalid values in input'
             ' will be ignored'
    )
    parsed_args = arg_parser.parse_args()
    try:
        if int(parsed_args.period) <= 0:
            raise ValueError
    except ValueError:
        print('Provided `--period` parameter is not valid. please pass valid'
              'positive integer value')
    try:
        main(parsed_args)
    except KeyboardInterrupt:
        print('Program stopped by user')
        sys.exit(1)

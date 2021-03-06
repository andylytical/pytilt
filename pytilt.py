#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Read data from a tilt hydrometer and save it in a CSV file

    Environment variables:
        Values for cmdline parameters can be specified in environment variables.
"""

import argparse
import collections
import csv
import os
import pathlib
import tiltscanner

import pprint


#module level paramter settings
_params = {}


### Getter methods for program parameters.
def _get_param( pname, ptype=str ):
    if pname not in _params:
        try:
            rawval = _params[ 'args' ][ pname ]
        except ( KeyError ) as e:
            msg = ( f"\nMissing parameter '{pname}'.\n" )
            raise SystemExit( msg )
        _params[ pname ] = ptype( rawval )
    return _params[ pname ]


def _get_tiltcolor():
    raw_color = _get_param( 'PYTILT_COLOR' )
    return raw_color.upper()


def _get_period():
    return _get_param( 'PYTILT_SAMPLE_PERIOD', int )


def _get_rate():
    return _get_param( 'PYTILT_SAMPLE_RATE', int )


def _get_csvfile():
    rawpath = _get_param( 'PYTILT_CSVOUTFILE', pathlib.Path )
    tgtpath = rawpath
    if not rawpath.is_absolute():
        tgtpath = pathlib.Path( '/data' ) / rawpath
    return tgtpath


def _parse_cmdline():
    arg_defaults = {
        'PYTILT_COLOR': '',
        'PYTILT_CSVOUTFILE': 'pytilt_output.csv',
        'PYTILT_SAMPLE_PERIOD': 900,
        'PYTILT_SAMPLE_RATE': 5,
    }
    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            argument_default=argparse.SUPPRESS)
    parser.add_argument(
        '-c', '--color',
        dest = 'PYTILT_COLOR',
        help = ( 'Tilt color; which tilt to collect data from '
                 f'[default={arg_defaults["PYTILT_COLOR"]}] ' )
        )
    parser.add_argument(
        '-f', '--file',
        dest = 'PYTILT_CSVOUTFILE',
        help = ( 'CSV output file '
                 f'[default={arg_defaults["PYTILT_CSVOUTFILE"]}] ' )
        )
    parser.add_argument(
        '-p', '--period', type=int,
        dest = 'PYTILT_SAMPLE_PERIOD',
        help = ( 'Tilt sample period, in seconds '
                 f'[default={arg_defaults["PYTILT_SAMPLE_PERIOD"]}]' )
        )
    parser.add_argument(
        '-r', '--rate', type=int,
        dest = 'PYTILT_SAMPLE_RATE',
        help = ( 'Tilt sample rate; number of secs between individual samples '
                 'in the sampling period'
                 f'[default={arg_defaults["PYTILT_SAMPLE_RATE"]}]' )
        )
    namespace = parser.parse_args()
    cmdline_args = { k:v for k,v in vars(namespace).items() if v }
    combined = collections.ChainMap( cmdline_args, os.environ, arg_defaults )
    _params[ 'args' ] = combined


def csv_get_headers():
    fn = _get_csvfile()
    with fn.open( newline='' ) as fh:
        csv_handle = csv.DictReader( fh )
        return list( csv_handle.fieldnames )


def csv_write_sample( data ):
    ''' Data is a Hash of Hashes, where
        Key = color
        Value = hash of data (suitable to write out as csv)
    '''
    outfile = _get_csvfile()
    headers = []
    needs_header = True
    if outfile.exists():
        headers = csv_get_headers()
        needs_header = False
    else:
        first_color = next( iter( data ) )
        headers = data[ first_color ].keys()
    with outfile.open( mode='a', newline='' ) as fh:
        csv_handle = csv.DictWriter( fh, headers )
        if needs_header:
            csv_handle.writeheader()
        for color in data:
            csv_handle.writerow( data[ color ] )


def main():
    ts = tiltscanner.TiltScanner( sample_period=_get_period(),
                                  sample_frequency=_get_rate()
                                )
    color = _get_tiltcolor()
    outfile = _get_csvfile()
    pprint.pprint( [ ts, f'Color={color}', outfile ] )
    while( True ):
        raw_sample = ts.get_data_point()
        if raw_sample:
            filtered_sample = raw_sample
            if color:
                filtered_sample = { color: raw_sample[ color ] }
            pprint.pprint( filtered_sample )
            csv_write_sample( filtered_sample )

if __name__ == '__main__':
    _parse_cmdline()
    main()

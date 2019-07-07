import lescanner
import statistics
import time

import pprint


class TiltScanner( object ):

    # Class attributes (and defaults)
    attr_names=[
        'bluetooth_device_id',
        'sample_period',
        'sample_frequency',
    ]
    bluetooth_device_id = 0
    sample_period = 900      #900 seconds = 15 mins
    sample_frequency = 5

    def __init__( self, *a, **k ):
        # set any attribute values
        namesfound = []
        for key in k:
            if key in self.attr_names:
                setattr( self, key, k[key] )
        # check for sane values
        if self.sample_frequency > self.sample_period:
            msg = ( f"Bad sample parameters: "
                    f"Frequency:'{sample_frequency}' "
                    f"must be less than Period:'{sample_period}'"
                  )
            raise UserWarning( msg )
        # create tilt scanner object
        self.ts = lescanner.LEScanner( bluetooth_dev_id=self.bluetooth_device_id )

    def __str__( self ):
        return f"<TiltScanner [period={self.sample_period} freq={self.sample_frequency}]>"
    __repr__ = __str__


    def get_data_point( self ):
        '''
            Scan all tilts, take multiple samples during a sample_period,
            save the median of each data type.
            Return a dict of dicts of the form:
                { TiltColor: { 'Color': TiltColor,
                               'SG': float,
                               'Temp': float,
                               'datetime': datetime.datetime object }
                             },
                  ...
                }
        '''
#        samples_by_color looks like (before median is applied)
#        {'RED': {'Color': ['RED', 'RED', 'RED', 'RED'],
#                 'SG': [1.061, 1.061, 1.061, 1.061],
#                 'Temp': [81.0, 81.0, 81.0, 81.0],
#                 'datetime': [datetime.datetime(2019, 7, 6, 22, 43, 21, 375638),
#                              datetime.datetime(2019, 7, 6, 22, 43, 24, 319871),
#                              datetime.datetime(2019, 7, 6, 22, 43, 29, 728097),
#                              datetime.datetime(2019, 7, 6, 22, 43, 32, 895652)]}}
        samples_by_color = {}
        num_samples = self.sample_period // self.sample_frequency
        # collect multiple samples
        for i in range( num_samples ):
            # ts.scan will return a list of data points, one per tilt color
            for data in self.ts.scan():
                color = data[ 'Color' ]
                if color not in samples_by_color:
                    samples_by_color[ color ] = { k:[] for k in data }
                for k in data:
                    samples_by_color[ color ][ k ].append( data[k] )
            time.sleep( self.sample_frequency )
        #pprint.pprint( samples_by_color )

        # For each color tilt, get median of samples
        new_s_by_c = {}
        for color,data in samples_by_color.items() :
            new_data = { k:statistics.median_high( data[k] ) for k in data }
            new_s_by_c[ color ] = new_data
        return new_s_by_c


if __name__ == '__main__':
    tilt = TiltScanner( sample_period=10, sample_frequency=2 )
    pprint.pprint( tilt )
    data = tilt.get_data_point()
    pprint.pprint( data )

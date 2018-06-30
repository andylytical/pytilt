import blescan
import bluetooth._bluetooth as bluez
import datetime
import pprint

class LEScanner( object ):
    # uuid's of various colour tilt hydrometers
    uuidmap = {
        'A495BB10-C5B1-4B44-B512-1370F02D74DE' : 'RED',
        'A495BB20-C5B1-4B44-B512-1370F02D74DE' : 'GREEN',
        'A495BB30-C5B1-4B44-B512-1370F02D74DE' : 'BLACK',
        'A495BB40-C5B1-4B44-B512-1370F02D74DE' : 'PURPLE',
        'A495BB50-C5B1-4B44-B512-1370F02D74DE' : 'ORANGE',
        'A495BB60-C5B1-4B44-B512-1370F02D74DE' : 'BLUE',
        'A495BB70-C5B1-4B44-B512-1370F02D74DE' : 'YELLOW',
        'A495BB80-C5B1-4B44-B512-1370F02D74DE' : 'PINK',
    }
#    colormap = {
#        'red'    : 'a495bb10c5b14b44b5121370f02d74de',
#        'green'  : 'a495bb20c5b14b44b5121370f02d74de',
#        'black'  : 'a495bb30c5b14b44b5121370f02d74de',
#        'purple' : 'a495bb40c5b14b44b5121370f02d74de',
#        'orange' : 'a495bb50c5b14b44b5121370f02d74de',
#        'blue'   : 'a495bb60c5b14b44b5121370f02d74de',
#        'yellow' : 'a495bb70c5b14b44b5121370f02d74de',
#        'pink'   : 'a495bb80c5b14b44b5121370f02d74de',
#    }

    def __init__( self, bluetooth_dev_id, *a, **k ):
        self.devid=bluetooth_dev_id
#        self.super( *a, **k )


    def scan( self ):
        #TODO - make this a "with" style context manager

        # Setup
        sock = bluez.hci_open_dev( self.devid )
        blescan.hci_le_set_scan_parameters( sock )
        blescan.hci_enable_le_scan( sock )

        #returns a list of Beacons
        scan_results = blescan.parse_events( sock, 10 )
        #pprint.pprint( scan_results )
        for beacon in scan_results:
            try:
                color = self.uuidmap[ beacon.uuid ]
            except (KeyError) as e:
                continue
            print( 'Found Tilt color: {}'.format( color ) )
            data = { 
                'datetime': datetime.datetime.now(),
                'SG':       float( beacon.minor ) / 1000,
                'Temp':     float( beacon.major ),
                'Color':    color,
            }
            pprint.pprint( data )

        # Teardown
        blescan.hci_disable_le_scan( sock )

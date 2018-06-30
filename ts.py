import lescanner

bt_dev = 0

ts = lescanner.LEScanner( bluetooth_dev_id=bt_dev )
ts.scan()

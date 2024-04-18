from glob import glob

def fp(rp):
    return sorted(glob(f"data/processed/{rp}/*.gz"))

return_periods = ['rp0001', 'rp0002', 'rp0005', 'rp0010', 'rp0050', 'rp0100', 'rp0250', 'rp0500', 'rp1000']

rps = dict([(rp, fp(rp)) for rp in return_periods])

print(rps['rp0001'][1])
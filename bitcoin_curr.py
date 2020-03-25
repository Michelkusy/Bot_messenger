import requests

def bitcoin(value, invert=False):
    site = 'https://blockchain.info/tobtc?currency=USD&value=' + value
    r = requests.get(site)
    p = r.json()

    if invert:
        text = value + " bitcoin te permette d'avoir " + str(1/p) + " euros"
    else:
        text = value + " euros te permette d'avoir " + str(p) + " bitcoins"
    return (text)
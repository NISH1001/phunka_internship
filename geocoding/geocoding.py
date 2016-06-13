#!/usr/bin/env python3

import xlrd
import xlwt
import geocoder
import json

# read json dump into dict for cleaned data
def read_clean_latlng(filename):
    datastr = open(filename).read()
    data = json.loads(datastr)
    d = {}
    for org in data:
        try:
            lat = data[org]['properties']['lat']
            lng = data[org]['properties']['lng']
            latstr = "{0:.2f}".format(lat)
            lngstr = "{0:.2f}".format(lng)
            #d[org] = [ lat, lng ]
            d[latstr+lngstr] = org
        except KeyError:
            continue
    return d

# read dirty json dump
def read_dirty_latlng(filename):
    datastr = open(filename).read()
    return json.loads(datastr)


# read sheet 1 and json dump the lat long as hashes
def read_sheet1(filename, row_start, row_end):
    workbook = xlrd.open_workbook(filename)
    sheet1 = workbook.sheet_by_index(0)
    sheet2 = workbook.sheet_by_index(1)
    nrows, ncols = sheet1.nrows, sheet1.ncols
    data = {}
    for i in range(row_start, row_end):
        #row = sheet1.row_slice(rowx=i, start_colx=1, end_colx=ncols)
        addrs = sheet1.cell(i, 1).value.split(';')
        for addr in addrs:
            #g = geocoder.mapbox(addr, access_token="pk.eyJ1IjoibmlzaHBhcmFkb3giLCJhIjoiY2lwZTliZWQ1MDA0M3NybWFndnh3ZjN5OCJ9.WkBPk_KcXEEu7vxmOjDydw")
            g = geocoder.google(addr)
            latlng = g.latlng
            try:
                lat = latlng[0]
                lng = latlng[1]
                latstr = "{0:.2f}".format(lat)
                lngstr = "{0:.2f}".format(lng)
                data[latstr+lngstr] = addr
                print(latstr+lngstr, addr)
                print('-'*30)
                with open("dirty.json", "w") as f:
                    json.dump(data, f)
            except IndexError:
                continue

# search for common hashes
def search(dirty, cleaned):
    sc = set(cleaned)
    sd = set(dirty)
    print(len(sc.intersection(sd)))
    for key in sc.intersection(sd):
        print(key)
        print(dirty[key])
        print(cleaned[key])
        print('-'*30)

def main():
    #read_sheet1("test.xlsx", 1, 1500)
    cleaned = read_clean_latlng("../data/geocoding/org_latlng.json")
    dirty = read_dirty_latlng("../data/geocoding/dirty.json")
    search(dirty, cleaned)


if __name__ == "__main__":
    main()


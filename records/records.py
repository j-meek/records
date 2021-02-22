#!/usr/bin/env python

"""
A program to query GBIF for all records of a specific species for a given
year range.
"""

import requests
import pandas as pd


class Records:

    """
    Class object for retrieving occurrenece records from GBIF
    """

    def __init__(self, genusname=None, genuskey=None, year=None):

        # store input params
        self.genusname = genusname
        self.genuskey = genuskey
        self.year = year

        # will be used to store output results
        self.df = None
        self.json = None

    def get_single_batch(self, offset=0, limit=20):
        "returns JSON result for a small batch query"

        params = {
                "year": self.year,
                "offset": offset,
                "limit": limit,
                "hasCoordinate": "true",
                "country": "US",
                }
        if self.genuskey:
            params["genuskey"] = self.genuskey
        elif self.genusname:
            params["q"] = self.genusname
            params["rank"] = "GENUS"

        # query GBIF for genus and year
        res = requests.get(
            url="https://api.gbif.org/v1/occurrence/search/",
            params=params
        )
        return res.json()

    def get_all_records(self):
        "stores result for all records to self.json and self.df"

        # for storing results
        alldata = []

        # continue until we call 'break'
        offset = 0
        while 1:

            # get JSON data for a batch
            jdata = self.get_single_batch(offset, 300)

            # increment counter by 300 (the max limit)
            offset += 300

            # add this batch of data to the growing list
            alldata.extend(jdata["results"])

            # stop when end of record is reached
            if jdata["endOfRecords"]:
                print(f'Done. Found {len(alldata)} records')
                break

            # print a dot on each rep to show progress
            print('.', end='')

        return alldata
        self.json = alldata
        self.df = pd.json_normalize(alldata)


if __name__ == "__main__":
    Records(genusname="Bombus", genuskey=1340278, year="1980,1985")

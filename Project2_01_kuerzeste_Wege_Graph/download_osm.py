#!/usr/bin/env python

# Copyright (c) 2018 Frank Fischer <frank-fischer@shadow-soft.de>
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see  <http://www.gnu.org/licenses/>

import csv
from urllib.request import urlopen
import xml.sax
import sys

highway_cat = ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'road', 'residential', 'service', 'motorway_link', 'trunk_link', 'primary_link', 'secondary_link', 'teriary_link']

#box = (-122.330,47.600,-122.301,47.601)
box = (8.1611, 49.9468, 8.3781, 50.1082)
# read coordinates from command line
box = tuple(float(sys.argv[i+1]) if i+1 < len(sys.argv) else box[i] for i in range(4))

def download_osm(left,bottom,right,top,highway_cat):
    """
    Downloads OSM street (only highway-tagged) Data using a BBOX,
    plus a specification of highway tag values to use

    Parameters
    ----------
    left,bottom,right,top : BBOX of left,bottom,right,top coordinates in WGS84
    highway_cat : a list of highway tag strings

    Returns
    ----------
    stream object with osm xml data

    """

    hw_cat_string = "|".join(highway_cat)

    print("trying to download osm data from {},{},{},{} with highways of categories {}".format(left,bottom,right,top, hw_cat_string))
    try:
        fp = urlopen( "http://www.overpass-api.de/api/xapi?way[highway=%s][bbox=%f,%f,%f,%f]"%(hw_cat_string,left,bottom,right,top) )
        return fp
    except Exception as ex:
        print("osm data download unsuccessful: ", ex)

def read_osm(filename_or_stream, highway_cat = None,only_roads = True):
    """Read graph in OSM format from file specified by name or by stream object.
    Filter by highway tags

    Parameters
    ----------
    filename_or_stream : filename or stream object

    highway_cat : list of highway tag strings

    only_roads : restriction to roads highways only

    Returns
    -------
    G : Graph

    Examples
    --------
    >>> (nodes, edges)=read_osm(nx.download_osm(-122.33,47.60,-122.31,47.61))

    """

    nodes = {}
    ways = {}

    class Node:
        def __init__(self, id, lon, lat):
            self.id = id
            self.lon = lon
            self.lat = lat
            self.tags = {}

    class Way:
        def __init__(self, id):
            self.id = id
            self.nds = []
            self.tags = {}

    class OSMHandler(xml.sax.ContentHandler):
        @classmethod
        def setDocumentLocator(self,loc):
            pass

        @classmethod
        def startDocument(self):
            pass

        @classmethod
        def endDocument(self):
            pass

        @classmethod
        def startElement(self, name, attrs):
            if name=='node':
                self.currElem = Node(attrs['id'], (attrs['lon']), (attrs['lat']))
            elif name=='way':
                self.currElem = Way(attrs['id'])
            elif name=='tag':
                self.currElem.tags[attrs['k']] = attrs['v']
            elif name=='nd':
                self.currElem.nds.append( attrs['ref'] )

        @classmethod
        def endElement(self,name):
            if name=='node':
                nodes[self.currElem.id] = self.currElem
            elif name=='way':
                ways[self.currElem.id] = self.currElem

        @classmethod
        def characters(self, chars):
            pass

    xml.sax.parse(filename_or_stream, OSMHandler)

    nds = {}
    edges = {}
    for way in list(ways.values()):
        if len(way.nds) >= 2:
            for u in way.nds:
                nds[u] = nodes[u]
            for i in range(1,len(way.nds)):
                edges[(way.nds[i-1], way.nds[i])] = True
            #if ('oneway' not in way.tags) or (way.tags['oneway'] != 'yes'):
            for i in range(1,len(way.nds)):
                edges[(way.nds[i], way.nds[i-1])] = True
    return (list(nds.values()), list(edges.keys()))

osm_xml = download_osm(*box, highway_cat)
(nodes, edges) = read_osm(osm_xml)

with open('nodes.csv', 'w', newline='') as f:
    w = csv.writer(f)
    for n in nodes:
        w.writerow([n.id, n.lon, n.lat])

with open('edges.csv', 'w', newline='') as f:
    w = csv.writer(f)
    for (u,v) in edges:
        w.writerow([u,v])

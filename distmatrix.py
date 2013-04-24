#! /usr/bin/env python
from googlemaps import GoogleMaps
import csv
import creds

gmaps = GoogleMaps(creds.api_key)


def calc(start, end):
	data = gmaps.directions(start, end)
	time = data['Directions']['Duration']['html']
	distance = data['Directions']['Distance']['meters'] // 1000 * 0.62137119
	resp = {}
	resp['start'] = start
	resp['end'] = end
	resp['time'] = time
	resp['distance'] = distance
	return resp

def setup():
	global postcodes
	global lookup
	csvfile = open('locations.csv', 'r') 
	data = csv.reader(csvfile)
	postcodes = []
	for row in data:
		postcodes.append(row[1])
	csvfile = open('locations.csv', 'r') 
	data = csv.reader(csvfile)
	lookup = {}
	for row in data:
		lookup[row[1]] = row[0] 
		lookup[row[0]] = row[1]

def process():
	data =[]
	for start in postcodes:
		for end in postcodes:
			if start != end:
				d = calc(start, end)
				d['start'] = lookup[d['start']]
				d['end'] = lookup[d['end']]
				data.append(d)
	return data
	

def output(data):
	output = open('distances.csv', 'a')
	for d in data:
		dist = "%.2f" % d['distance'] 
		distance = str(dist)+ ' mi'
		string =  d['start'] + "," + d['end'] + "," + distance + "," + d['time'] + "," +"\n"
		output.write(string)
	output.close()
	print "Done"

		
if __name__ == '__main__':
	setup()
	data = process()
	output(data)		
	




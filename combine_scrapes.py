# -*- coding: utf-8 -*-
# this script takes all the scraped*.csv files and combines them into one, getting rid of duplicates

import os
import sys
import glob

os.chdir('.')
csvs = [i for i in glob.glob('scraped*.csv')]
#print(csvs)

data = dict()
for datafile in csvs:
	for line in open(datafile):
		linel = line.rstrip().split(',')
		img = linel[0]
		caption = linel[1]
		if caption not in data:
			data[caption] = img

# write to new csv
# csv header
with open('all_scrapes.csv', 'w+') as f:
	f.write("img_url,img_caption,img_desc\n")
	for caption in data:
		line = "{},{},\n".format(data[caption], caption)
		f.write(line)

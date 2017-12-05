# -*- coding: utf-8 -*-

import sys
from captionbot import CaptionBot
import emoji

# create instance of CaptionBot
c = CaptionBot()

for line in open('all_scrapes.csv', encoding="utf8"):
	line = line.rstrip()
	cols = line.split(',')
	img_url = cols[0]
	# if line is the header
	if img_url == 'img_url':
		print(line)
		continue
		
	#------------- Clean Image URL -------------#
	# remove quotes from img_url
	img_url = img_url[1:-1]
	
	caption = cols[1]
	#--------- Clean Instagram Caption ---------#
	# if there is no caption skip it
	if len(caption) < 1: continue
	# currently emojis look like (apparently called mojibake): ðŸ˜˜
	# should turn emojis into actual emojis
	caption.encode('cp1252').decode('utf-8')
	# now try converting emojis to aliases
	try:
		caption = emoji.demojize(caption)
	except e:
		print >> sys.stderr, 'Error converting caption to alias for image {}'.format(img_url)
		# if you can't do it, it's not a big deal, leave the funny looking characters in there
	
	# try getting description from captionbot
	try:
		desc = c.url_caption(img_url)
	except e:
		print >> sys.stderr, 'Error getting captionbot desc for image {}: {}'.format(img_url, e)
		continue
	# try converting emojis to aliases
	try:
		desc = emoji.demojize(desc)
	except e:
		print >> sys.stderr, 'Error converting desc to alias for image {}'.format(img_url)
		continue
	#------------ Clean Description ------------#
	# insert spaces between emoji aliases 
	desc = desc.replace('::', ': :')
	# remove commas from captionbot description
	desc = desc.replace(',', '')
	# remove newlines and return chars
	desc = desc.replace('\n', ' ')
	desc = desc.replace('\r', '')
	desc = desc.replace('\r\n', '')
	# get rid of period at the end
	desc = desc.replace('.', '')
	
	# write out data
	data = "{},{},{}".format(img_url, caption, desc)
	print(data)
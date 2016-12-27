#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'CYX'

import aiohttp, asyncio
import json, time
import xlrd


COLUM_FAMILY = ['title', 'sort_id', 'content', 'url', 'keywords']
DB_HOST = '1.85.37.132'
#DB_HOST = 'localhost'

async def vod_data(client, data, headers):
	r = await client.post('http://'+DB_HOST+'/api/vod/items', data=json.dumps(data), headers = headers)
	await r.release()

workbook = xlrd.open_workbook(r'vod/vod.xlsx')

sheet1_name = workbook.sheet_names()[0]
print(sheet1_name)

sheet1 = workbook.sheet_by_name(sheet1_name)
print(sheet1.name, sheet1.nrows, sheet1.ncols)

items = []
for i in range(sheet1.nrows):
#	if i == 0:
#		continue
	rows = sheet1.row_values(i)
	item = {}
	for j in range(len(COLUM_FAMILY)):
		column_name = COLUM_FAMILY[j]
		item[column_name] = sheet1.cell(i,j).value

	items.append(item)

data = {'items':items}
headers = {'content-type': 'application/json'}

with aiohttp.ClientSession() as client:
	tasks = [vod_data(client, data, headers)]

	asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))

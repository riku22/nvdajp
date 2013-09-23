# jtalkPredicTest.py 
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
import os
import sys
sys.path.append(r'..\source\synthDrivers\jtalk')
from _jtalk_core import *
import _nvdajp_predic

tests = [
	['0123345', ' ゼロ イチ ニー サン サン ヨン ゴー '],
	['人々', '人人'],
	['昔々', '昔昔'],
	['家々', '家家'],
	['山々', '山山'],
	['は', 'ハ'],
	[' は', 'ハ'],
	['Ａ', 'a'],
	['59 名', '59名'],
	['4行', '4ギョー'],
	['2 分前更新', '2分マエコーシン'],
	['1MB', '1メガバイト'],
	['10MB', '10メガバイト'],
	['1.2MB', '1.2メガバイト'],
	['0.5MB', '0.5メガバイト'],
	['321.1MB', '321.1メガバイト'],
	['123.45MB', '123.45メガバイト'],
	['2.7GB', '2.7ギガバイト'],
	['10KB', '10キロバイト'],
	['1 MB', '1メガバイト'],
	['10 MB', '10メガバイト'],
	['1.2 MB', '1.2メガバイト'],
	['0.5 MB', '0.5メガバイト'],
	['321.0 MB', '321.0メガバイト'],
	['123.45 MB', '123.45メガバイト'],
	['2.7 GB', '2.7ギガバイト'],
	['10 KB', '10キロバイト'],
	['12.01 KB', '12. ゼロ イチ キロバイト'],
	['12.01', '12. ゼロ イチ '],
	['12.35', '12.35'],
	['01234', ' ゼロ イチ ニー サン ヨン '],
	['1.01', '1. ゼロ イチ '],
	['1.10', '1.10'],
	['２０１１．０３．１１', '2011. ゼロ サン .11'],
	['１，２３４円', '1234円'],
	['0,1', '0カンマ1'],
	['134,554', '134554'],
]

def _print(s):
	print(s.encode('utf-8', 'ignore'))

if __name__ == '__main__':
	_nvdajp_predic.setup()
	for item in tests:
		s = _nvdajp_predic.convert(item[0])
		if item[1] != s:
			_print('expected:%s result:%s' % (item[1], s))

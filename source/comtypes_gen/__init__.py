
def setAsComtypesGenModule():
	import sys
	import comtypes
	import comtypes.gen
	import comtypes_gen
	sys.modules['comtypes.gen']=comtypes.gen=comtypes_gen

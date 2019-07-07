import platform
sys_name = platform.system().lower()
filename = ''
if sys_name.startswith('darwin'):  # mac
    filename = '/Applications/QGIS3.app/Contents/Resources/resources/data/world_map.shp'
elif sys_name.startswith('win'):  # windows
    filename = 'C:/Program Files/QGIS 3.6/apps/qgis/resources/data'
else:
    raise 'unknown system'

import fiona
shape = fiona.open(filename)
print (shape.schema)
#first feature of the shapefile
first = shape.next()
print (first) # (GeoJSON format)

# other method for open shapefile https://gis.stackexchange.com/questions/113799/how-to-read-a-shapefile-in-pythonk
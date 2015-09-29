from osgeo import gdal, gdalconst
import sys, struct, matplotlib.pyplot as plt

#Read DEM file
dataset = gdal.Open('/home/zia/Documents/Test/geospatial-py/l10g')

#Following code is to convert lat long values into pixel values
t = dataset.GetGeoTransform()
success, tInverse = gdal.InvGeoTransform(t)
if not success:
    print "failed"
    sys.exit(1)
x1, y1 = gdal.ApplyGeoTransform(tInverse, 165, -48)
x2, y2 = gdal.ApplyGeoTransform(tInverse, 179, -33)
minX = int(min(x1,x2))
maxX = int(max(x1,x2))
minY = int(min(y1,y2))
maxY = int(max(y1,y2))

band = dataset.GetRasterBand(1)
width = (maxX - minX) + 1

#Dictionary to map height to # pixels with that height
histogram = {}

#Read raster band, line-by-line
for y in range(minY, maxY+1):
    #Following line is interesting about the passed in parameters
    scanline = band.ReadRaster(minX, y, width, 1, width, 1, gdalconst.GDT_Int16)
    values = struct.unpack("<"+("h"*width), scanline)
    
    for value in values:
        if value != band.GetNoDataValue():
            try:
                histogram[value] += 1
            #Following KeyError is to handle NoDataValues. You have to use this code. Dunno why "if value !=" and "except" have been used together?!
            except KeyError:
                histogram[value] = 1

#Plot the graph        
plt.plot(histogram.keys(), histogram.values(), 'ro')
plt.xlim(0,3300)
plt.ylim(0,3000)
plt.show()
    

from osgeo import ogr
from osgeo.ogr import CreateGeometryFromWkt

shapefile = ogr.Open("/home/zia/Documents/Data/TM_WORLD_BORDERS-0.3/TM_WORLD_BORDERS.shp")
layer = shapefile.GetLayer(0)

for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    geometry = feature.GetGeometryRef()
    minlong, maxlong, minlat, maxlat = geometry.GetEnvelope()
    poly_Wkt= "POLYGON((%s %s, %s %s, %s %s, %s %s))"% (minlong, minlat, minlong, maxlat, maxlong, minlat, maxlong, maxlat)
    geom_poly = ogr.CreateGeometryFromWkt(poly_Wkt)
    print geom_poly

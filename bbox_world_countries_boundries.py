from osgeo import ogr, osr
import shutil, os, os.path, math

def calculateLength(minlong, minlat, maxlong, maxlat):
    rminlat = math.radians(minlat)
    rminlong = math.radians(minlong)
    rmaxlat = math.radians(maxlat)
    rmaxlong = math.radians(maxlong)
    dLat = rmaxlat - rminlat
    dLong = rmaxlong - rminlong
    a = math.sin(dLat/2)**2 + math.cos(rminlat) * math.cos(rmaxlat) \
    * math.sin(dLong/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = 6371 * c
    return distance

def calculateArea(minlong, minlat, maxlong, maxlat):
    area = calculateLength(minlong, minlat, maxlong, minlat) * calculateLength(maxlong, minlat, maxlong, maxlat)
    return area

#World countries boundries shapefile
srcFile = ogr.Open("/home/zia/Documents/Data/TM_WORLD_BORDERS-0.3/TM_WORLD_BORDERS.shp")
#Taking the very first, and in this case the only, layer
layer = srcFile.GetLayer(0)

#Below 3 lines. Creating bounding-box dir
if os.path.exists("/home/zia/bounding-box"):
    shutil.rmtree("/home/zia/bounding-box")
os.mkdir("/home/zia/bounding-box")

#Setting spatial reference for our future shapefile which will hold the bbox
spatialRef = osr.SpatialReference()
spatialRef.SetWellKnownGeogCS('WGS84')

#Setting the driver and all. Necessary stuff
driver = ogr.GetDriverByName('ESRI Shapefile')
dstPath = os.path.join('/home/zia/bounding-box', 'bounding-boxes.shp')
dstFile = driver.CreateDataSource(dstPath)
dstLayer = dstFile.CreateLayer('layer', spatialRef)

#Make a Name field for the new shapefile
fieldDef = ogr.FieldDefn('Country', ogr.OFTString)
fieldDef.SetWidth(50)
dstLayer.CreateField(fieldDef)

#Make an area field
fieldDef = ogr.FieldDefn('Area', ogr.OFTReal)
dstLayer.CreateField(fieldDef)

#Read the world countries boundries shapefile
for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    countryName = feature.GetField('NAME')
    geometry = feature.GetGeometryRef()
    minlong, maxlong, minlat, maxlat = geometry.GetEnvelope()
    
    #Create a linearRing geometry which will hold the countires boundries rectangles' ring
    linearRing = ogr.Geometry(ogr.wkbLinearRing)
    linearRing.AddPoint(minlong, minlat)
    linearRing.AddPoint(maxlong, minlat)
    linearRing.AddPoint(maxlong, maxlat)
    linearRing.AddPoint(minlong, maxlat)
    linearRing.AddPoint(minlong, minlat)
    
    #Make the polygon from the above generated ring
    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(linearRing)
    
    #Calculate area using Haversine Formula
    area = calculateArea(minlong, minlat, maxlong, maxlat)
    
    #Feed to the new shapefile both polygon and country name attribute
    feature = ogr.Feature(dstLayer.GetLayerDefn())
    feature.SetGeometry(polygon)
    feature.SetField('Country', countryName)
    feature.SetField('Area', area)
    dstLayer.CreateFeature(feature)
    
    #Destroy the feature for subsequents loop
    feature.Destroy()
 
#Destroy both the source and destination shapefiles. Destinations' destruction is necessary for saving ensurement    
srcFile.Destroy()
dstFile.Destroy()

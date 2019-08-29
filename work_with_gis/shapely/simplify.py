# https://gist.github.com/robinkraft/c6de2f988c9d3f01af3c
# https://shapely.readthedocs.io/en/stable/manual.html#polygons
# https://shapely.readthedocs.io/en/stable/manual.html#object.simplify
# https://shapely.readthedocs.io/en/stable/manual.html#coordinate-systems
# https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
# https://shapely.readthedocs.io/en/stable/manual.html#python-geo-interface

import pyproj
import utm
from functools import partial
from shapely.geometry import shape
from shapely.ops import transform
from shapely.geometry import Polygon


# list of points for Polygon
listPoints = [ (113.40457095200009, 34.66669761300005), (113.40450188800003, 34.666838461000054), (113.40429731400002, 34.667026358000044), (113.40410619400006, 34.66710937700003), (113.40395538100006, 34.66707783900006), (113.40386091900007, 34.66708171100004), (113.40377173500008, 34.667081274000054), (113.40373535300012, 34.66703341500005), (113.40363570600005, 34.667028592000065), (113.4035200080001, 34.66706703600005), (113.4033729890001, 34.667083654000066), (113.40322044400011, 34.66713925600004), (113.40303605000008, 34.66724671700007), (113.4030300600001, 34.66735071900007), (113.40299265300007, 34.66744589700005), (113.40286568600004, 34.66759265400003), (113.40279642500002, 34.667739693000044), (113.40258530800008, 34.66797401500003), (113.40258401900007, 34.66815352100008), (113.40257383400001, 34.66836170500005), (113.40258997500007, 34.66853411500006), (113.40262329100005, 34.66873533100005), (113.40263398400009, 34.66881939500007), (113.40292263800006, 34.66883713400006), (113.402996314, 34.66891636200006), (113.40311285500002, 34.66893446000006), (113.4032722610001, 34.66889142700006), (113.40352724700006, 34.66883133600004), (113.40362339400008, 34.668735414000025), (113.40362446400002, 34.66858644700005), (113.40358443100001, 34.668253253000046), (113.40355487900001, 34.66793763800007), (113.40352457200004, 34.66772717500004), (113.40371579300006, 34.66768429700005), (113.40400522000004, 34.66766982900003), (113.40402565000011, 34.66777494400003), (113.4040848620001, 34.66798405000003), (113.4040947950001, 34.66799791300008), (113.40453040500006, 34.66802228100005), (113.40454060400009, 34.66803009700004), (113.40458139500004, 34.668258137000066), (113.40461044800008, 34.66864385400004), (113.40461960900006, 34.66884545000005), (113.40468268200004, 34.668924624000056), (113.4047782020001, 34.668916325000055), (113.40483211100002, 34.66879390400004), (113.40484378400004, 34.66864498800004), (113.40483512200001, 34.66837329100008), (113.4048366290001, 34.66816298400005), (113.40482022800006, 34.66809595500007), (113.40482791000011, 34.66742400500004), (113.4050725080001, 34.667423787000075), (113.40510611000002, 34.667559641000025), (113.40515573700009, 34.66793709800004), (113.40517263700008, 34.66863782300004), (113.40522460500006, 34.66878704700002), (113.40533035500005, 34.66883137600007), (113.40550722600005, 34.668844421000074), (113.40553633800005, 34.66922410400008), (113.40575813600003, 34.66923893300003), (113.40587417900008, 34.66924484300006), (113.40586907300008, 34.66889729400003), (113.40736676900008, 34.66889527300003), (113.40765143300007, 34.668672438000044), (113.4076462920001, 34.668673296000065), (113.40749474400002, 34.666869381000026), (113.40748047400007, 34.66669954500003), (113.4074803090001, 34.666697586000055), (113.40739014700011, 34.66562504900003), (113.40738350600009, 34.665545989000066), (113.40739183900007, 34.66527564100005), (113.40709305400003, 34.665340764000064), (113.40697358400007, 34.66532000800004), (113.40692137300005, 34.665235309000025), (113.40653873300005, 34.66530724200004), (113.40651742200009, 34.66538425400006), (113.40632427500009, 34.66543414300003), (113.40622804100008, 34.66542441100006), (113.40625827400004, 34.665449686000045), (113.40629460800005, 34.66566903300003), (113.40648081600011, 34.66588797400004), (113.4064398160001, 34.66591439100006), (113.40615271900003, 34.66590621100005), (113.40594761200009, 34.66590521000006), (113.40592290300003, 34.66591864700007), (113.4057666860001, 34.66596533500007), (113.40565950300004, 34.66603937600007), (113.40558552100003, 34.66605935100006), (113.40542181900003, 34.66600432200005), (113.40534798200008, 34.666003964000026), (113.40524118600001, 34.666023781000035), (113.40521604700007, 34.66609822500004), (113.4052319760001, 34.66616608900006), (113.4052478100001, 34.66624751000006), (113.40521456300007, 34.66630835700005), (113.40508296300004, 34.66635516800005), (113.40498413000012, 34.66640891800006), (113.40472240800011, 34.666516999000066) ]

# list of points for Python Geo Interface
listP2 = [[[[113.40457095200009, 34.66669761300005], [113.40450188800003, 34.666838461000054], [113.40429731400002, 34.667026358000044], [113.40410619400006, 34.66710937700003], [113.40395538100006, 34.66707783900006], [113.40386091900007, 34.66708171100004], [113.40377173500008, 34.667081274000054], [113.40373535300012, 34.66703341500005], [113.40363570600005, 34.667028592000065], [113.4035200080001, 34.66706703600005], [113.4033729890001, 34.667083654000066], [113.40322044400011, 34.66713925600004], [113.40303605000008, 34.66724671700007], [113.4030300600001, 34.66735071900007], [113.40299265300007, 34.66744589700005], [113.40286568600004, 34.66759265400003], [113.40279642500002, 34.667739693000044], [113.40258530800008, 34.66797401500003], [113.40258401900007, 34.66815352100008], [113.40257383400001, 34.66836170500005], [113.40258997500007, 34.66853411500006], [113.40262329100005, 34.66873533100005], [113.40263398400009, 34.66881939500007], [113.40292263800006, 34.66883713400006], [113.402996314, 34.66891636200006], [113.40311285500002, 34.66893446000006], [113.4032722610001, 34.66889142700006], [113.40352724700006, 34.66883133600004], [113.40362339400008, 34.668735414000025], [113.40362446400002, 34.66858644700005], [113.40358443100001, 34.668253253000046], [113.40355487900001, 34.66793763800007], [113.40352457200004, 34.66772717500004], [113.40371579300006, 34.66768429700005], [113.40400522000004, 34.66766982900003], [113.40402565000011, 34.66777494400003], [113.4040848620001, 34.66798405000003], [113.4040947950001, 34.66799791300008], [113.40453040500006, 34.66802228100005], [113.40454060400009, 34.66803009700004], [113.40458139500004, 34.668258137000066], [113.40461044800008, 34.66864385400004], [113.40461960900006, 34.66884545000005], [113.40468268200004, 34.668924624000056], [113.4047782020001, 34.668916325000055], [113.40483211100002, 34.66879390400004], [113.40484378400004, 34.66864498800004], [113.40483512200001, 34.66837329100008], [113.4048366290001, 34.66816298400005], [113.40482022800006, 34.66809595500007], [113.40482791000011, 34.66742400500004], [113.4050725080001, 34.667423787000075], [113.40510611000002, 34.667559641000025], [113.40515573700009, 34.66793709800004], [113.40517263700008, 34.66863782300004], [113.40522460500006, 34.66878704700002], [113.40533035500005, 34.66883137600007], [113.40550722600005, 34.668844421000074], [113.40553633800005, 34.66922410400008], [113.40575813600003, 34.66923893300003], [113.40587417900008, 34.66924484300006], [113.40586907300008, 34.66889729400003], [113.40736676900008, 34.66889527300003], [113.40765143300007, 34.668672438000044], [113.4076462920001, 34.668673296000065], [113.40749474400002, 34.666869381000026], [113.40748047400007, 34.66669954500003], [113.4074803090001, 34.666697586000055], [113.40739014700011, 34.66562504900003], [113.40738350600009, 34.665545989000066], [113.40739183900007, 34.66527564100005], [113.40709305400003, 34.665340764000064], [113.40697358400007, 34.66532000800004], [113.40692137300005, 34.665235309000025], [113.40653873300005, 34.66530724200004], [113.40651742200009, 34.66538425400006], [113.40632427500009, 34.66543414300003], [113.40622804100008, 34.66542441100006], [113.40625827400004, 34.665449686000045], [113.40629460800005, 34.66566903300003], [113.40648081600011, 34.66588797400004], [113.4064398160001, 34.66591439100006], [113.40615271900003, 34.66590621100005], [113.40594761200009, 34.66590521000006], [113.40592290300003, 34.66591864700007], [113.4057666860001, 34.66596533500007], [113.40565950300004, 34.66603937600007], [113.40558552100003, 34.66605935100006], [113.40542181900003, 34.66600432200005], [113.40534798200008, 34.666003964000026], [113.40524118600001, 34.666023781000035], [113.40521604700007, 34.66609822500004], [113.4052319760001, 34.66616608900006], [113.4052478100001, 34.66624751000006], [113.40521456300007, 34.66630835700005], [113.40508296300004, 34.66635516800005], [113.40498413000012, 34.66640891800006], [113.40472240800011, 34.666516999000066]]]]

# print out for gis test
# for p in listPoints:
    # print(p[0],",", p[1])

# Polygon method to create polygon
gon1 = Polygon(listPoints)
# print(len(listPoints))

# Python Geo Interface method to create polygon
listP2 = [l for sublist in listP2 for l in sublist]
geom = {'type': 'Polygon', 'coordinates': listP2}
gon2 = shape(geom)

# choose polygon
gon = gon1

# get one sample coordinates
lat = listP2[0][0][1]
lon = listP2[0][0][0]

# calculate epsg according to utm zone
x, y, z, l  = utm.from_latlon(lat,lon)
if(lat > 0):
    epsg_tgt = 'epsg:' + str(32600 + z)
else:
    epsg_tgt = 'epsg:' + str(32700 + z)
# print(epsg_tgt)
# epsg:32649

epsg_src = 'epsg:4326'

# transform project: source to target; target to source
proj = partial(pyproj.transform, pyproj.Proj(init=epsg_src),
               pyproj.Proj(init=epsg_tgt))
proj_rev = partial(pyproj.transform, pyproj.Proj(init=epsg_tgt),
               pyproj.Proj(init=epsg_src))

# transform latlon coordinates to Cartesian coordinates
gon_utm = transform(proj, gon)
# print area and numnber of coordinates
# print(gon_utm.area, len(gon_utm.exterior.coords))

# simplify the polygon
gon_utm_simplify = gon_utm.simplify(0.5, True)
# print(gon_utm_simplify.area, len(gon_utm_simplify.exterior.coords))

# transform Cartesian coordinates to latlon coordinates
gon_simplify = transform(proj_rev, gon_utm_simplify)
# print(gon_simplify.wkt)
pts = list(gon_simplify.exterior.coords)
# print(x, ",", y)
# print out for gis test
for p in pts:
    print(p[0],",", p[1])

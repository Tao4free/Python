#!/usr/local/bin/python3
# refer: https://stackoverflow.com/questions/46261002/print-multiple-lines-without-space-between-lines

import csv, codecs, time
import latlon2dis as ll2dis

start_time = time.time()

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    f.close()
    return i + 1


ffac = codecs.open("factory.csv", 'r',encoding='utf-8')
ffac_a = open("factory_addFloodDis.csv", 'w')
fc = open("count.csv",'w')
w = csv.writer(fc)

fflood = open("flood_centroid.txt", 'r')

#for i, line in enumerate(fflood,1):
#    if(i == 15):
#        break
#    line = line.splitlines()[0]
#    
#    line = line.split(',')
#    line = list(map(float,line))
#    print(line[0])
    

reader = csv.reader(ffac)
header = next(reader)
#print(header)

for n, row in enumerate(reader,1):
    thold = 20 # km radius 
    lv = [0.1,1.0,3.0,5.0]
    count = [0,0,0,0,0]
    nallow = 0

    #if(n == 26):
    #    break

    number = [row[0]]
    id     = [row[1]]
    lat1_d = float(row[2])
    lon1_d = float(row[3])
    #print(lat1_d,lon1_d)

    shift = 1.0
    lat1_d_plus  = lat1_d + shift
    lat1_d_minus = lat1_d - shift
    lon1_d_plus  = lon1_d + shift
    lon1_d_minus = lon1_d - shift

    # Initialize distance and depth value
    dis_min = 9999
    v_dismin = 0

    dis_vmax = 0
    vmax = 0


    fflood.seek(0)
    next(fflood)
    for i, line in enumerate(fflood,1):
        #if(i == 30):
        #    break
        line = line.splitlines()[0]
        
        line = line.split(',')
        line = list(map(float,line))
        lat2_d = line[1]
        lon2_d = line[0]
        value = line[2]

        if(lat2_d < lat1_d_minus or lat2_d > lat1_d_plus or \
           lon2_d < lon1_d_minus or lon2_d > lon1_d_plus):
            continue
   
        dis = ll2dis.dis(lat1_d,lon1_d,lat2_d,lon2_d)

        if(dis <= thold):
            if(dis_min > dis):
                dis_min = dis
                v_dismin = value
            if(vmax < value):
                dis_vmax = dis
                vmax = value
            nallow = nallow + 1
            for nlv in range(len(lv)):
                if(value < lv[nlv] ):
                    count[nlv] = count[nlv] + 1

        #print("facter %2d %15.10f %15.10f flood %10d %10.3f" % (n, lat1_d, lon1_d, i, dis)) if (dis<= 40)


    # Recalculate counts in each range
    count[len(count)-1] = nallow - count[len(count)-2]
    for nc in range(len(count)-2,0,-1):
        count[nc] = count[nc] - count[nc-1]

    csvrow = number + id + count + ["%.3f" % dis_min] + ["%.3f" % v_dismin] + ["%.3f" % dis_vmax] + ["%.3f" % vmax]
    w.writerow(csvrow)
    print(csvrow)

ffac.close()
ffac_a.close()
fc.close()

print("--- %s seconds ---" % (time.time() - start_time))

#lat1_d = 52.2296756
#lon1_d = 21.0122287
#lat2_d = 52.406374
#lon2_d = 16.9251681

#dis = ll2dis.dis(lat1_d,lon1_d,lat2_d,lon2_d)

#print("Calculate distance from (%f,%f) to (%f,%f)" % (lat1_d,lon1_d,lat2_d,lon2_d))
#print("Result:", dis)
#print("Should be: %10.3f km" % dis)

import requests
import time
import json
import geopy.distance
import haversine as hs
from haversine import Unit

def get_sboxname():
    sandboxname=requests.get("http://131.114.54.25/platform-ctrl/v1/sandboxes").json()['sandboxes'][0]['name']
    print("Sandbox name is: %s" % sandboxname)
    urlbase="http://131.114.54.25"
    urlrni_base=urlbase + "/" + sandboxname +"/"+ "rni" + "/" + "v2"
    urlgis_base=urlbase + "/" + sandboxname + "/" + "gis" + "/" + "v1" + "/" + "geodata"
    return urlgis_base

def p_choose():
    urlgis_base=get_sboxname()
    gis=requests.get(urlgis_base)
    gisjson=gis.json()
    gis_dumped=json.dumps(gisjson,indent=4)
    i=0
    p_wifi1=0
    p_wifi2=0
    p_4g1=0
    p_4g2=0
    p_5g1=0
    p_5g2=0
   
    while True:
        try:
            uename=gisjson['geoDataAssets'][i]['assetName']
            if uename=='ue1':
                uepos=gisjson['geoDataAssets'][i]['location']['coordinates']
                break
            else:
                i+=1
        except:
            print("No ue1 found")
            break

    i=0

    while True:
        try:
            bs1=gisjson['geoDataAssets'][i]['assetName']
            if bs1=='wifi1':
                bs1pos=gisjson['geoDataAssets'][i]['location']['coordinates']
                break
            else:
                i+=1
        except:
            print("No bs1 found")
            break
    i=0
    while True:
        try:
            bs2=gisjson['geoDataAssets'][i]['assetName']
            if bs2=='wifi2':
                bs2pos=gisjson['geoDataAssets'][i]['location']['coordinates']
                break
            else:
                i+=1
        except:
            print("No bs2 found")
            break


    bs1touem=hs.haversine(bs1pos,uepos,unit=Unit.METERS)
    bs2touem=hs.haversine(bs2pos,uepos,unit=Unit.METERS)
    bs1tobs2=hs.haversine(bs1pos,bs2pos,unit=Unit.METERS)

  
    print("bs1 to ue=",bs1touem)
    print("bs2 to ue=",bs2touem)

    if bs1touem < 200:
        p_wifi1=1
        p_5g1=1
        p_4g1=1
    if bs1touem < 500 and bs1touem > 200:
        p_wifi1=0
        p_5g1=1
        p_4g1=1
    if bs1touem < 1000 and bs1touem > 500:
        p_wifi1=0
        p_5g1=0
        p_4g1=1

    if bs2touem < 200:
        p_wifi2=1
        p_5g2=1
        p_4g2=1
    if bs2touem < 500 and bs2touem > 200:
        p_wifi2=0
        p_5g2=1
        p_4g2=1
    if bs2touem < 1000 and bs2touem > 500:
        p_wifi2=0
        p_5g2=0
        p_4g2=1

    p=[[p_wifi1,p_4g1,p_5g1],[p_wifi2,p_4g2,p_5g2]]
    p_description=[["wifi1","4g1","5g1"],["wifi2","4g2","5g2"]]
    return p, uename, p_description

def p_choose_noMEC():
    urlgis_base=get_sboxname()
    gis=requests.get(urlgis_base)
    gisjson=gis.json()
    gis_dumped=json.dumps(gisjson,indent=4)
    i=0
    p_wifi1=0
    p_wifi2=0
    p_4g1=0
    p_4g2=0
    p_5g1=0
    p_5g2=0

    while True:
        try:
            uename=gisjson['geoDataAssets'][i]['assetName']
            if uename=='ue1':
                uepos=gisjson['geoDataAssets'][i]['location']['coordinates']
                break
            else:
                i+=1
        except:
            print("No ue1 found")
            break

    i=0

    while True:
        try:
            bs1=gisjson['geoDataAssets'][i]['assetName']
            if bs1=='wifi1':
                bs1pos=gisjson['geoDataAssets'][i]['location']['coordinates']
                break
            else:
                i+=1
        except:
            print("No bs1 found")
            break
    i=0
    while True:
        try:
            bs2=gisjson['geoDataAssets'][i]['assetName']
            if bs2=='wifi2':
                bs2pos=gisjson['geoDataAssets'][i]['location']['coordinates']
                break
            else:
                i+=1
        except:
            print("No bs2 found")
            break


    bs1touem=hs.haversine(bs1pos,uepos,unit=Unit.METERS)
    bs2touem=hs.haversine(bs2pos,uepos,unit=Unit.METERS)
    bs1tobs2=hs.haversine(bs1pos,bs2pos,unit=Unit.METERS)

    print("bs1 to ue=",bs1touem)
    print("bs2 to ue=",bs2touem)




    if bs1touem < bs2touem:
        p_wifi1=0
        p_5g1=1
        p_4g1=0
        p_wifi2=0
        p_5g2=0
        p_4g2=0
    if bs1touem > bs2touem:
        p_wifi1=0
        p_5g1=0
        p_4g1=0
        p_wifi2=0
        p_5g2=0
        p_4g2=1
    p=[[p_wifi1,p_4g1,p_5g1],[p_wifi2,p_4g2,p_5g2]]
    p_description=[["wifi1","4g1","5g1"],["wifi2","4g2","5g2"]]
    return p, uename, p_description



if __name__ == "__main__":
    while True:
        time.sleep(1)
        p, uename, p_description=p_choose()



        for i in range(len(p[0])):
            if p[0][i] == 1:
                print("ue1 under coverage of: ",p_description[0][i])
            if p[1][i] == 1:
                print("ue1 under coverage of: ",p_description[1][i])

import requests
import json

#change the IP address to where the AdvantEDGE platform is running  
def post_mobility(element,dest):

    sandboxname=requests.get("http://152.94.64.68/platform-ctrl/v1/sandboxes").json()['sandboxes'][0]['name']
    urlbase="http://152.94.64.68"#"http://192.168.178.145"


#urlrni_base=urlbase + "/" + sandboxname +"/"+ "rni" + "/" + "v2"
#urlgis_base=urlbase + "/" + sandboxname + "/" + "gis" + "/" + "v1" + "/" + "geodata"

    mobility_url=urlbase + "/" + sandboxname + "/" + "sandbox-ctrl/v1/events/MOBILITY"
    headers = {'accept': 'application/json', 'content-type': 'application/json'}
    body='{"name": "name","type": "MOBILITY","eventMobility": {"elementName":'   +'"'+str(element)+'"' +  ',"dest":' + '"'+str(dest)+'"'+ '}}'
    response = requests.post(mobility_url, data=(body), headers=headers)
    print(response)



if __name__ == "__main__":
    element="term1"
    dest="w3"
    post_mobility(element,dest)

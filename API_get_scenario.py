import requests
import time
import json

def format_time():
    adesso=time.time()
    timestruct=time.localtime(adesso)
    ore=timestruct.tm_hour
    ore=str(ore)
    if len(ore)<2:
        ore="0" + ore

    minuti=timestruct.tm_min
    minuti=str(minuti)
    if len(minuti)<2:
        minuti="0" + minuti

    secondi=timestruct.tm_sec
    secondi=str(secondi)
    if len(secondi)<2:
        secondi="0" + secondi

    nanosecondi=int((adesso-int(adesso))*1000000)
    nanosecondi=str(nanosecondi)

    if len(nanosecondi)==5:
        nanosecondi="0"+nanosecondi
    elif len(nanosecondi)==4:
        nanosecondi="00"+nanosecondi
    elif len(nanosecondi)==3:
        nanosecondi="000"+nanosecondi
    elif len(nanosecondi)==2:
        nanosecondi="0000"+nanosecondi
    elif len(nanosecondi)==1:
        nanosecondi="00000"+nanosecondi
    elif len(nanosecondi)==0:
        nanosecondi="000000"

    orarioattuale=ore + ":" + minuti + ":" + secondi + "." + nanosecondi
    return orarioattuale

#change the IP address to where the AdvantEDGE platform is running  
def get_scenario_API():
    sandboxname=requests.get("http://152.94.64.68/platform-ctrl/v1/sandboxes").json()['sandboxes'][0]['name']
    urlbase="http://152.94.64.68"
    sdbx_basev1=urlbase + "/" + sandboxname + "/" + "sandbox-ctrl/v1"
    tof="false"
    scenario_url=sdbx_basev1 + "/" + "active?minimize="+ tof
    headers = {'accept': 'application/json', 'content-type': 'application/json'}
    response = requests.get(scenario_url)
    json_resp=response.json()
    json_resp_dumped=json.dumps(json_resp,indent=4)
    return response
    



if __name__ == "__main__":
    r=get_scenario_API()
    json_resp=r.json()
    json_resp_dumped=json.dumps(json_resp,indent=4)
    print(json_resp["deployment"]["domains"][1]["zones"][3]["netChar"])#["zones"]["zone3"])#["netChar"])

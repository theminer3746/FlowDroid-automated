import argparse
import os
import subprocess
import sys
import time
from subprocess import Popen, PIPE
from dotenv import load_dotenv, find_dotenv
import requests as req
import json
import re

try:
    load_dotenv(find_dotenv())

    parser = argparse.ArgumentParser()
    parser.add_argument('app_id', metavar='app_id', type=str,
                        help='Application identifier')

    parser.add_argument('--endpoint', metavar='endpoint',
                    type=str, help='Endpoint at which the result will be sent (Example: http://127.0.0.1:80/sendResult)', default=None)


    if __name__ == '__main__':
        args = parser.parse_args()


    # Pipeline
    apk_path = os.environ.get("APK_PATH", "../automated-gui-tester/apk")
    log_path = "final_log"

    def flowDroid(apk):
        start_time = time.time()
        p = Popen(["java", "-jar", "soot-infoflow-cmd-jar-with-dependencies.jar", "-a", os.path.join(apk_path, f"{apk}.apk"), "-p", "/home/theminer3746/Android/Sdk/platforms", "-s", "mergeSuSi.txt", "-ct", "120"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate() 
        rc = p.returncode
        finish_time = time.time()
        time_lapsed = finish_time - start_time
        fp = open(os.path.join(log_path, apk + ".log"), "w")
        fp.write("Time lapsed: " + str(time_lapsed) + (" s\n\n"))
        fp.write(str(err,"utf-8"))
        fp.close()

        return err.decode().split('\n')[:-1]

    flowDroid_log = flowDroid(args.app_id)


    # Log transformation
    log_path = "final_log"
    new_log_path = "final_pro_log"
    cat_log_path = "final_cat_log"

    method = {}
    fp = open("final_piiSu.txt","r")
    for line in fp:
        k = line.split(",")[0]
        v = line.split(",")[1].split("\n")[0]
        method[k] = v
    fp.close()

    cat_method = {}
    fp = open("final_pii_cat.txt","r")
    for line in fp:
        k = line.split(",")[0]
        v = line.split(",")[1].split("\n")[0]
        cat_method[k] = v
    fp.close()


    def getNewLogFileContent(flowDroid_log):
        new_log_file_content = []
        
        for line in flowDroid_log:
            if len(line.split("- -")) > 1:
                new_log_file_content.append(line.split("- - ")[1].split(" in method")[0])

        return new_log_file_content


    def getFinalCatLogContent(new_log_file_content):
        final_cat_log_content = []
        for line in new_log_file_content:
            for k,v in method.items():
                if k in line:
                    if cat_method[k] == "Account":
                        final_cat_log_content.append("Username")
                        final_cat_log_content.append("Email")
                        final_cat_log_content.append("Password")
                    else:
                        final_cat_log_content.append(cat_method[k])


        return final_cat_log_content


    new_log_file_content = getNewLogFileContent(flowDroid_log)
    final_cat_log_content = getFinalCatLogContent(new_log_file_content)
    # print(final_cat_log_content)


    # Export result
    log_path = "final_cat_log"

    pii_list = [
        "static-Advertiser ID",
        "static-Android ID",
        "static-Device SN",
        "static-GSF ID",
        "static-IMEI",
        "static-MAC Address",
        "static-GSM Cell ID",
        "static-ICCID",
        "static-IMSI",
        "static-Location Area Code",
        "static-Phone Number",
        "static-Age",
        "static-Audio",
        "static-Calendar",
        "static-Contract Book",
        "static-Country",
        "static-Credit Card",
        "static-Date Of Birth",
        "static-Email",
        "static-Gender",
        "static-Name",
        "static-Password",
        "static-Photo",
        "static-Physical Address",
        "static-Relationship",
        "static-SMS",
        "static-SSN",
        "static-Time Zone",
        "static-Username",
        "static-Video",
        "static-Web Log",
        "static-GPS"
    ]

    def getLeaks(final_cat_log_content):
        ans = ["0" for a in pii_list]
        for line in final_cat_log_content:
            pii = line.strip()
            ans[pii_list.index("static-"+pii)] = "1"

        return ans

    result = getLeaks(final_cat_log_content)
    result = dict(zip(pii_list, result))


    def getVersionName(package_name):
        cmd = ["aapt", "dump", "badging", os.path.join(apk_path, f"{package_name}.apk")]

        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        out = output.decode("utf-8").strip()

        versionName = None

        for line in out.split('\n'):
            line = line.strip()
            if 'versionName=' in line:
                version_search = re.search("versionName=\'(.*?)\'", line)
                if version_search:
                    return version_search.group(1)

    version_name = getVersionName(args.app_id)

    # print(result)
    payload = dict()
    payload['status'] = 'success'
    payload['appInfo'] = {
        'applicationId' : args.app_id,
        'version' : version_name,
    }
    payload['result'] = result
    payload['testingMethods'] = 'STATIC_ONLY'
    print(payload)


    if args.endpoint:
        res = req.post(args.endpoint, json=payload)
    else:
        print('-----BEGIN JSON OUTPUT-----')
        print(json.dumps(payload))
        print('-----END JSON OUTPUT-----')

    exit(0)

except Exception as e:
    print("An exception occurred")
    print(e)
    exit(1)

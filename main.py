import argparse
import os
import subprocess
import time
from subprocess import Popen, PIPE
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

parser = argparse.ArgumentParser()
parser.add_argument('app_id', metavar='app_id', type=str,
                    help='Application identifier')

if __name__ == '__main__':
    args = parser.parse_args()


# Pipeline
apk_path = os.environ.get("APK_PATH", "../vulpix-runner/automated-gui-tester/apk")
log_path = "final_log"

def flowDroid(apk):
    start_time = time.time()
    p = Popen(["java", "-jar", "soot-infoflow-cmd-jar-with-dependencies.jar", "-a", os.path.join(apk_path, apk), "-p", "/home/theminer3746/Android/Sdk/platforms", "-s", "mergeSuSi.txt", "-ct", "120"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
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
    
    # in_fp = open(os.path.join(log_path, log_file), "r", encoding = "utf-8")
    # out_fp = open(os.path.join(new_log_path, log_file), "w", encoding = "utf-8")
    for line in flowDroid_log:
        if len(line.split("- -")) > 1:
            # out_fp.write(line.split("- - ")[1].split(" in method")[0]+"\n")
            new_log_file_content.append(line.split("- - ")[1].split(" in method")[0])
    # in_fp.close()
    # out_fp.close()

    return new_log_file_content


def getFinalCatLogContent(new_log_file_content):
    # ans = {}
    # ans["DEVICE"] = "0"
    # ans["SIM"] = "0"
    # ans["USER"] = "0"
    # ans["LOCATION"] = "0"
    # ans["LEAK"] = "0"
    final_cat_log_content = []
    # out_fp = open(os.path.join(cat_log_path, log_file), "w", encoding = "utf-8")
    for line in new_log_file_content:
        for k,v in method.items():
            if k in line:
                # ans["LEAK"] = "1"
                # ans[v] = "1"
                if cat_method[k] == "Account":
                    final_cat_log_content.append("Username")
                    final_cat_log_content.append("Email")
                    final_cat_log_content.append("Password")
                else:
                    final_cat_log_content.append(cat_method[k])
    # in_fp.close()
    # out_fp.close()

    return final_cat_log_content




# def classifyMethod(log_file):
#     in_fp = open(os.path.join(new_log_path, log_file), "r", encoding = "utf-8")
#     # ans = {}
#     # ans["DEVICE"] = "0"
#     # ans["SIM"] = "0"
#     # ans["USER"] = "0"
#     # ans["LOCATION"] = "0"
#     # ans["LEAK"] = "0"
#     out_fp = open(os.path.join(cat_log_path, log_file), "w", encoding = "utf-8")
#     for line in in_fp:
#         for k,v in method.items():
#             if k in line:
#                 # ans["LEAK"] = "1"
#                 # ans[v] = "1"
#                 if cat_method[k] == "Account":
#                     out_fp.write("Username\nEmail\nPassword\n")
#                 else:
#                     out_fp.write(cat_method[k]+"\n")
#     in_fp.close()
#     out_fp.close()
#     # fp.write(log_file[:len(log_file)-4]+","+ans["DEVICE"]+","+ans["SIM"]+","+ans["USER"]+","+ans["LOCATION"]+","+ans["LEAK"]+"\n")


# def getNewLog(log_file):
#     in_fp = open(os.path.join(log_path, log_file), "r", encoding = "utf-8")
#     out_fp = open(os.path.join(new_log_path, log_file), "w", encoding = "utf-8")
#     for line in in_fp:
#         if len(line.split("- -")) > 1:
#             out_fp.write(line.split("- - ")[1].split(" in method")[0]+"\n")
#     in_fp.close()
#     out_fp.close()

# for apk in os.listdir(log_path):
#     print(apk)
#     getNewLog(apk)
# fp.close()

# fp = open("cat_flowdroid_final.csv","w")
# fp.write("apk,DEVICE,SIM,USER,LOCATION,LEAK\n")
# for apk in os.listdir(new_log_path):
#     print(apk)
#     classifyMethod(apk)
# fp.close()

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
    # in_fp = open(os.path.join(log_path,log_file),"r",encoding = "utf-8")
    ans = ["0" for a in pii_list]
    for line in final_cat_log_content:
        pii = line.strip()
        ans[pii_list.index("static-"+pii)] = "1"
    # in_fp.close()
    # fp.write(log_file[:len(log_file)-4]+","+",".join(ans)+"\n")

    return ans

result = getLeaks(final_cat_log_content)
print(result)
print(dict(zip(pii_list, result)))

# fp = open("detail_static.csv","w")
# fp.write("apk,"+",".join(pii_list)+"\n")
# for file in os.listdir(log_path):
#     classifyMethod(file)
# fp.close()


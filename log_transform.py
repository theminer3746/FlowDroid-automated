import os

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


def classifyMethod(log_file):
    in_fp = open(os.path.join(new_log_path, log_file), "r", encoding = "utf-8")
    ans = {}
    ans["DEVICE"] = "0"
    ans["SIM"] = "0"
    ans["USER"] = "0"
    ans["LOCATION"] = "0"
    ans["LEAK"] = "0"
    out_fp = open(os.path.join(cat_log_path, log_file), "w", encoding = "utf-8")
    for line in in_fp:
        for k,v in method.items():
            if k in line:
                ans["LEAK"] = "1"
                ans[v] = "1"
                if cat_method[k] == "Account":
                    out_fp.write("Username\nEmail\nPassword\n")
                else:
                    out_fp.write(cat_method[k]+"\n")
    in_fp.close()
    out_fp.close()
    fp.write(log_file[:len(log_file)-4]+","+ans["DEVICE"]+","+ans["SIM"]+","+ans["USER"]+","+ans["LOCATION"]+","+ans["LEAK"]+"\n")


def getNewLog(log_file):
    in_fp = open(os.path.join(log_path, log_file), "r", encoding = "utf-8")
    out_fp = open(os.path.join(new_log_path, log_file), "w", encoding = "utf-8")
    for line in in_fp:
        if len(line.split("- -")) > 1:
            out_fp.write(line.split("- - ")[1].split(" in method")[0]+"\n")
    in_fp.close()
    out_fp.close()


for apk in os.listdir(log_path):
    print(apk)
    getNewLog(apk)
fp.close()

fp = open("cat_flowdroid_final.csv","w")
fp.write("apk,DEVICE,SIM,USER,LOCATION,LEAK\n")
for apk in os.listdir(new_log_path):
    print(apk)
    classifyMethod(apk)
fp.close()

pii_list = set()
for apk in os.listdir(cat_log_path):
    print(apk)
    fp = open(cat_log_path+apk,"r")
    for line in fp:
        pii_list.add(line.strip())
    fp.close()

for v in pii_list:
    print(v.strip())

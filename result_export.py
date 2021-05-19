import os

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

def classifyMethod(log_file):
    in_fp = open(os.path.join(log_path,log_file),"r",encoding = "utf-8")
    ans = ["0" for a in pii_list]
    for line in in_fp:
        pii = line.strip()
        ans[pii_list.index("static-"+pii)] = "1"
    in_fp.close()
    fp.write(log_file[:len(log_file)-4]+","+",".join(ans)+"\n")

fp = open("detail_static.csv","w")
fp.write("apk,"+",".join(pii_list)+"\n")
for file in os.listdir(log_path):
    classifyMethod(file)
fp.close()

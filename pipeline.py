import os
import subprocess
import time
from subprocess import Popen, PIPE 

apk_path = "../vulpix-runner/automated-gui-tester/apk"
log_path = "final_log"

def flowDroid(apk):
    start_time = time.time()
    p = Popen(["java", "-jar", "soot-infoflow-cmd-jar-with-dependencies.jar", "-a", os.path.join(apk_path, apk),"-p","/home/theminer3746/Android/Sdk/platforms","-s","mergeSuSi.txt","-ct","120"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate() 
    rc = p.returncode
    finish_time = time.time()
    time_lapsed = finish_time - start_time
    fp = open(os.path.join(log_path, apk + ".log"), "w")
    fp.write("Time lapsed: " + str(time_lapsed) + (" s\n\n"))
    fp.write(str(err,"utf-8"))
    fp.close()


flowDroid("com.ookbee.ookbeecomics.android.apk")

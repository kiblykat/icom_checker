import os
import subprocess
import shutil
import time

FPKX = 0
WHUD = 1

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# = = = = = = = = = = FUNCTION DEFINITIONS = = = = = = = = = =
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

# Function to prompt user for folder selection
def select_entry(prompt_message):
    while True:
        folder_path = input(prompt_message)
        if os.path.exists(os.path.join(os.getcwd(), folder_path)) or os.path.exists(os.path.join(os.getcwd(), folder_path)+".bat") :
            return folder_path
        else:
            print(f"🔴 {time.strftime('%X')} File/Folder not found. Please check spelling.")



# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# = = = = = = = = = = = = CODE FLOW = = = = = = = = = = = = = = =
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#define main directory
main_directory = os.getcwd()

# Prompt user for AC and GC folders
build_folder_AC = select_entry(f"❩ {time.strftime('%X')} Choose build folder for AC: ").upper()
build_folder_GC = select_entry(f"❩ {time.strftime('%X')} Choose build folder for GC: ").upper()

while True:
    project = input("is project 0: FPKX or 1: WHUD \n") 
    if(project == "0" or project == "1"):
        project = int(project)
        break

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# = = = = = = = = = GENERATE FLASH FILES (AC) = = = = = = = = = =
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
if(project == WHUD):
    #open prv/tool/_GEN (AC)
    os.chdir(main_directory+"/" + build_folder_AC + "/prv/tool/_GEN")

    # run __changeRSA_PubKey.bat
    # run __Gen_ALL.bat (concurrently as above as they are independent)
    subprocess.run([ "__changeRSA_PubKey" + ".bat"], stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True) #note: do not run in background using Popen, will cause issue
    subprocess.run([ "__Gen_ALL" + ".bat"], stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True) #use run to ensure process is done before next (since this takes longer)

if(project == FPKX):
    #open prv/tool/_GEN (AC)
    os.chdir(main_directory+"/" + build_folder_AC + "/tool/integration/tool/deliver/core")

    # run __changeRSA_PubKey.bat
    # run __Gen_ALL.bat (concurrently as above as they are independent)
    subprocess.Popen([ "get_sym" + ".bat"], stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True) #run in background
    process = subprocess.Popen([ "get_prg" + ".bat"], stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True) #use run to ensure process is done before next (since this takes longer)
    process.communicate(input="ALL\n ")
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# = = = = = = = = = GENERATE FLASH FILES (GC) + OPEN FLASH TOOL = = = = = = = = = =
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
if(project == WHUD):
    #open prv/tool/_GEN (GC)
    os.chdir(main_directory+"/" + build_folder_GC + "/prv/tool/_GEN")

    # run __changeRSA_PubKey.bat
    # run __Gen_ALL.bat (concurrently as above as they are independent)
    subprocess.run([ "__changeRSA_PubKey" + ".bat"], stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True) #note: do not run in background using Popen, will cause issue
    subprocess.run([ "__Gen_ALL" + ".bat"], stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True) #use run to ensure process is done before next (since this takes longer)


    # go to pkg\fls\tool\mapscrpt\out
    os.chdir(main_directory + "/" + build_folder_AC + "/pkg/fls/tool/mapscrpt/out")


    # open in this order:
    # 	1. GCLoader (GC) 
    os.chdir(main_directory + "/" + build_folder_GC + "/pkg/fls/tool/mapscrpt/out")
    if os.path.exists("HUDW_MQB2020_Q3_GC_Loader.prg"):
        subprocess.Popen(["cmd", "/c", "HUDW_MQB2020_Q3_GC_Loader.prg"])
        time.sleep(0.5)
    else:
        subprocess.Popen(["cmd", "/c", "HUDW_MQB2020_Q3_GC_Loader_ETH.prg"])
        time.sleep(0.5)

    # 	2. ACLoader (AC)
    os.chdir(main_directory + "/" + build_folder_AC + "/pkg/fls/tool/mapscrpt/out") 
    if os.path.exists("HUDW_MQB2020_Q3_AC_Loader.prg"):
        subprocess.Popen(["cmd", "/c", "HUDW_MQB2020_Q3_AC_Loader.prg"])
        time.sleep(0.5)
    else:
        subprocess.Popen(["cmd", "/c", "HUDW_MQB2020_Q3_AC_Loader_ETH.prg"])
        time.sleep(0.5)

    # 	3. BackupIDL (AC)  
    subprocess.Popen(["cmd", "/c", "BACKUP_IDL.prg"])
    time.sleep(0.5)

    # 	4. Format_EEProm (AC) 
    subprocess.Popen(["cmd", "/c", "FormatEEProm.prg"])
    time.sleep(0.5)

    # 	5. GC_APP (GC) (use GC_ALL) 
    os.chdir(main_directory + "/" + build_folder_GC + "/pkg/fls/tool/mapscrpt/out")
    subprocess.Popen(["cmd", "/c", "HUDW_MQB2020_Q3_GC_All.prg"])
    time.sleep(0.5)

    # 	6. AC_APP (AC) (use AC_ALL) 
    os.chdir(main_directory + "/" + build_folder_AC + "/pkg/fls/tool/mapscrpt/out")
    subprocess.Popen(["cmd", "/c", "HUDW_MQB2020_Q3_AC_All.prg"])
    time.sleep(0.5)

    #   7. DataSet, eg. <xxx>_ds.prg (AC) 
    os.chdir(main_directory + "/" + build_folder_AC + "/pkg/fls/tool/mapscrpt/out")
    subprocess.Popen(["cmd", "/c", "HUDW_MQB2020_AU380PA_C5_LL_ds.prg"])

if(project == FPKX):
    #open prv/tool/_GEN (GC)
    os.chdir(main_directory+"/" + build_folder_GC + "/tool/integration/tool/deliver/core")

    # run __changeRSA_PubKey.bat
    # run __Gen_ALL.bat (concurrently as above as they are independent)
    subprocess.Popen([ "get_sym" + ".bat"], stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True) #run in background
    process = subprocess.Popen([ "get_prg" + ".bat"], stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True) #use run to ensure process is done before next (since this takes longer)
    process.communicate(input="ALL\n ")


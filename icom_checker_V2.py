# = = = = = = = = = = = = = = = = = = = = ICOM CHECKER & SYNC = = = = = = = = = = = = = = = = = = = = = =
# visit https://confluence.auto.continental.cloud/display/VNIHMIAEICSW/ICOM+Sync+Tool for details on usage  

import os
import subprocess
import shutil
import time

#defining constants
FPKM = 0
FPKE = 1 
WHUD = 2

#global variables
fpkmBrand = ""

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
# = = = = = = = = = = = = = = DEFINING FUNCTIONS  = = = = = = = = = = = = = = = = 
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 

main_directory = os.getcwd() 
log_file = "logFile.txt"
os.chdir(main_directory)
with open(log_file, "a") as f:
    f.write("\n = = = = NEW BUILD STARTED = = = = \n")

def getProjectType():
    while True:
        projectType = input("{} Which project are you building:\nFPKM: 0\nFPKE: 1 \nWHUD: 2\n".format(time.strftime('%X')))
        if(projectType.isdigit):
            if(int(projectType) >= 0 and int(projectType) < 3):
                return int(projectType)
        print("Enter a valid option")
# Function to prompt user for folder selection
def select_entry(prompt_message):
    while True:
        folder_path = input(prompt_message)
        if os.path.exists(os.path.join(os.getcwd(), folder_path)) or os.path.exists(os.path.join(os.getcwd(), folder_path)+".bat") :
            return folder_path
        else:
            log("{} File/Folder not found. Please check spelling.".format(time.strftime('%X')))

# Function to find line containing search word
def find_line(file_path):
    if(os.path.exists(file_path)):
        with open(file_path, "r") as file:
            for line in file:
                if search_word in line:
                    return line.strip()
    return None

def continueSync():
        while True:
            continue_sync = input("{} Do you still want to proceed with sync? (y/n): ".format(time.strftime('%X'))).upper()
            if continue_sync == "Y":
                break
            elif continue_sync == "N":
                log("{} Script finished".format(time.strftime('%x %X')))
                input("Press Enter to continue...")
                exit()

# Function to compare lines between AC and GC folder
def compare_lines(line1,line2,line3,line4):
    if line1 is None:
        log("{} INTERFACEID not found in {}".format(time.strftime('%X'), file_AC))
    if line2 is None:
        log("{} INTERFACEID not found in {}".format(time.strftime('%X'), file_GC))
    if line3 is None:
        log("{} INTERFACEID not found in {}".format(time.strftime('%X'), file_AC_2))
    if line4 is None:
        log("{} INTERFACEID not found in {}".format(time.strftime('%X'), file_GC_2))
    if line1 != line2:
        log("{} Your folders are not synced \n".format(time.strftime('%X')))
        log("{}: {}".format(file_AC, line1))
        log("{}: {} \n".format(file_GC, line2))
        time.sleep(2)
        continueSync()
        log("{} Proceeding with ICOM build syncing...".format(time.strftime('%X')))
        time.sleep(5)
        return
    elif line3 != line4:
        log("{} Your folders are not synced \n".format(time.strftime('%X')))
        log("{}: {}".format(file_AC_2, line3))
        log("{}: {} \n".format(file_GC_2, line4))
        time.sleep(2)
        continueSync()
        log("{} Proceeding with ICOM build syncing...".format(time.strftime('%X')))
        time.sleep(5)
        return() 
    else:
        log("{} Your folders are synced. Congratulations".format(time.strftime('%X')))
        continueSync()

# Function to build AC/GC folders
def build(build_batch_file,build_folder,ACGC,projectType):
    log("{} Running {} batch file:{}".format(time.strftime('%X'), ACGC, build_batch_file))
    os.chdir(build_folder)
    # subprocess.run([build_batch_file + ".bat"])
    if projectType==0 and ACGC=="GC":
        process = subprocess.Popen([build_batch_file + ".bat"], stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
        process.communicate(input=variant)
    else:
        # Run the batch file in a separate subprocess, while printing log in current terminal
        process = subprocess.Popen([build_batch_file + ".bat"], stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
        # Wait for the process to finish and simulate an Enter key press
        stdout,stderr = process.communicate(input='\n')
    
    return

def choose_sequence():
    while True:
        first_folder = input("Choose which folder to build first: ").upper()
        if (first_folder == "AC" or first_folder == "GC"):
            return first_folder
        log("{} Please input a valid folder".format(time.strftime('%X')))

def log(log_data):
    print(log_data)
    os.chdir(main_directory)
    data_to_write = log_data[2:]
    with open(log_file, "a") as f:
        f.write(data_to_write + "\n")

def getPrgSym(build_folder, projectType):
    if projectType == FPKM or projectType == FPKE:
        prgFolder = os.path.join(os.getcwd(),build_folder, "tool", "integration", "tool", "deliver", "core")
        if os.path.exists(prgFolder):
            os.chdir(prgFolder)
            print(os.getcwd())
            getPrgProcess = subprocess.Popen([os.path.join(prgFolder, "get_prg.bat")],stdin=subprocess.PIPE, text=True)
            if projectType == FPKM:
                stdout, stderr = getPrgProcess.communicate(input='{} \n'.format(fpkmBrand))
            subprocess.run(os.path.join(prgFolder, "get_sym.bat"))
    elif projectType == WHUD:
        prgFolder = os.path.join(os.getcwd(),build_folder,"prv", "tool", "_GEN")
        if os.path.exists(prgFolder):
            print("prgFolder is: " + prgFolder)
            os.chdir(prgFolder)
            print(os.getcwd())
            subprocess.run(os.path.join(prgFolder, "__changeRSA_PubKey.bat"))
            subprocess.run(os.path.join(prgFolder, "__Gen_ALL.bat"))
    
def getFpkmBrand():
    while True:
        fpkmBrand = input("{} Enter brand (VW, AU, SE, or ALL): ".format(time.strftime('%X'))).upper()
        if(fpkmBrand == "VW" or fpkmBrand == "AU" or fpkmBrand == "SE" or fpkmBrand == "ALL"):
            return fpkmBrand
        log("{} Please enter a valid brand".format(time.strftime('%X')))

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
# = = = = = = = = = = = = = = = START OF CODE FLOW  = = = = = = = = = = = = = = = 
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 


# Start log file
log("{} Script started \n".format(time.strftime('%x %X')))


# Prompt user for AC and GC folders
build_folder_AC = select_entry("{} Choose build folder for AC: ".format(time.strftime('%X'))).upper()
build_folder_GC = select_entry("{} Choose build folder for GC: ".format(time.strftime('%X'))).upper()

# Set file paths for icom_export.sdh
file_AC = os.path.join(build_folder_AC, "core", "pkg", "icom", "icom_export.sdh")
file_GC = os.path.join(build_folder_GC, "adapt", "gen", "tofac", "core", "pkg", "icom", "icom_export.sdh")

file_AC_2 = os.path.join(build_folder_AC, "adapt", "gen", "ToFGC", "core", "pkg", "icom", "icom_export.sdh")
file_GC_2 = os.path.join(build_folder_GC, "core", "pkg", "icom", "icom_export.sdh")

# Define search word
search_word = "INTERFACEID"

# Find lines containing search word in AC and GC files
line1 = find_line(file_AC)
line2 = find_line(file_GC)

line3 = find_line(file_AC_2)
line4 = find_line(file_GC_2)

# Compare lines
compare_lines(line1,line2,line3,line4)

#Prompt if building WHUD or FPKX
projectType = getProjectType()
if projectType==FPKM:
    while True:
        variant = input("Select Build variant to build\n-------------------------------------------------------------\n  1    -- for FPKM 24S1 (GEN1)\n  2    -- for FPKM Seamless (GEN2)\n").upper()
        if(variant == '1' or variant == '2'):
            getFpkmBrand()
            break

# Prompt user for build variants
os.chdir(main_directory + "/AC")
build_AC_batch = select_entry("Choose build variant for AC: ")
os.chdir(main_directory + "/GC")
build_GC_batch = select_entry("Choose build variant for GC: ")

# Choose which folder to build first
if(choose_sequence() == "AC"): # AC build first
    # Run AC build
    os.chdir(main_directory)
    build(build_AC_batch,build_folder_AC, "AC",projectType)

    # Copy files from AC to GC folder (dirs_exist_ok true: if directory is alr inside, overwrite)
    log("{} Copying files from AC to GC".format(time.strftime('%X')))
    time.sleep(2) #for debugging
    os.chdir(main_directory) # return to parent dir
    shutil.copytree(os.path.join(os.getcwd(), build_folder_AC, "adapt", "gen", "ToFGC", "core", "pkg"),
                    os.path.join(os.getcwd(), build_folder_GC, "core", "pkg"),
                    dirs_exist_ok=True)

    # Run GC build
    build(build_GC_batch,build_folder_GC,"GC",projectType)

    # Copy files from GC to AC folder
    log("{} Copying files from GC to AC".format(time.strftime('%X')))
    os.chdir(main_directory) # return to parent dir
    shutil.copytree(os.path.join(build_folder_GC, "adapt", "gen", "tofac", "core", "pkg"),
                    os.path.join(build_folder_AC, "core", "pkg"),
                    dirs_exist_ok=True)

    # Run AC build again
    build(build_AC_batch,build_folder_AC,"AC",projectType)

    # Run get_prg and get_sym for AC
    os.chdir(os.path.dirname(os.getcwd())) # return to parent dir
    if(projectType == FPKM): 
        log("{} AC: Running get_prg and get_sym".format(time.strftime('%X')))
        getPrgSym(build_folder_AC, FPKM)
        log("{} GC: Running get_prg and get_sym".format(time.strftime('%X')))
        getPrgSym(build_folder_GC, FPKM)
    elif projectType == FPKE: 
        log("{} AC: Running get_prg and get_sym".format(time.strftime('%X')))
        getPrgSym(build_folder_AC, FPKE)
        log("{} GC: Running get_prg and get_sym".format(time.strftime('%X')))
        getPrgSym(build_folder_GC, FPKE)
    elif projectType == WHUD:
        log("{} AC: Running __changeRSA_PubKey and __Gen_ALL".format(time.strftime('%X')))
        getPrgSym(build_folder_AC, WHUD)
        log("{} GC: Running __changeRSA_PubKey and __Gen_ALL".format(time.strftime('%X')))
        getPrgSym(build_folder_GC, WHUD)

    # End log file
    log("{} Script finished \n".format(time.strftime('%x %X')))
    input("Press Enter to continue...")
else: #GC build first
    os.chdir(main_directory)
    # Run GC build
    build(build_GC_batch,build_folder_GC,"GC",projectType)

    # Copy files from GC to AC folder
    log("{} Copying files from GC to AC".format(time.strftime('%X')))
    os.chdir(main_directory) # return to parent dir
    shutil.copytree(os.path.join(build_folder_GC, "adapt", "gen", "tofac", "core", "pkg"),
                    os.path.join(build_folder_AC, "core", "pkg"),
                    dirs_exist_ok=True)

    # Run AC build
    build(build_AC_batch,build_folder_AC,"AC",projectType)

    # Copy files from AC to GC folder (dirs_exist_ok true: if directory is alr inside, overwrite)
    log("{} Copying files from AC to GC".format(time.strftime('%X')))
    time.sleep(2) #for debugging
    os.chdir(main_directory) # return to parent dir
    shutil.copytree(os.path.join(os.getcwd(), build_folder_AC, "adapt", "gen", "ToFGC", "core", "pkg"),
                    os.path.join(os.getcwd(), build_folder_GC, "core", "pkg"),
                    dirs_exist_ok=True)

    # Run GC build again
    build(build_GC_batch,build_folder_GC,"GC",projectType)

    # Run get_prg and get_sym for AC
    os.chdir(os.path.dirname(os.getcwd())) # return to parent dir
    
    if projectType == FPKM: 
        log(" {} AC: Running get_prg and get_sym".format(time.strftime('%X')))
        getPrgSym(build_folder_AC, FPKM)
        log("{} GC: Running get_prg and get_sym".format(time.strftime('%X')))
        getPrgSym(build_folder_GC, FPKM)
    elif projectType == FPKE: 
        log("{} AC: Running get_prg and get_sym".format(time.strftime('%X')))
        getPrgSym(build_folder_AC, FPKE)
        log("{} GC: Running get_prg and get_sym".format(time.strftime('%X')))
        getPrgSym(build_folder_GC, FPKE)
    elif projectType == WHUD:
        log("{} AC: Running __changeRSA_PubKey and __Gen_ALL".format(time.strftime('%X')))
        getPrgSym(build_folder_AC, WHUD)
        log("{} GC: Running __changeRSA_PubKey and __Gen_ALL".format(time.strftime('%X')))
        getPrgSym(build_folder_GC, WHUD)

    # End log file
    log("{} Script finished \n".format(time.strftime('%x %X')))
    input("Press Enter to continue...")

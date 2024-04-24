import os
import subprocess
import shutil
import time
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
# = = = = = = = = = = = = = = DEFINING FUNCTIONS  = = = = = = = = = = = = = = = = 
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 

#global variables
main_folder = os.getcwd() 

# Function to prompt user for folder selection
def select_entry(prompt_message):
    while True:
        folder_path = input(prompt_message)
        if os.path.exists(folder_path) | os.path.exists(folder_path + ".bat") :
            return folder_path
        else:
            print("🔴 File/Folder not found. Please check spelling.")

# Function to find line containing search word
def find_line(file_path):
    with open(file_path, "r") as file:
        for line in file:
            if search_word in line:
                return line.strip()
    return None

# Function to compare lines between AC and GC folder
def compare_lines(line1,line2,line3,line4):
    if line1 is None:
        print("INTERFACEID not found in", file_AC)
    if line2 is None:
        print("INTERFACEID not found in", file_GC)
    if line3 is None:
        print("INTERFACEID not found in", file_AC_2)
    if line4 is None:
        print("INTERFACEID not found in", file_GC_2)
    if line1 != line2:
        print("🔴 Your folders are not synced \n")
        print(f"{file_AC}: ❌ {line1}")
        print(f"{file_GC}: ❌ {line2} \n")
        time.sleep(2)
        print("Proceeding with ICOM build syncing...")
        time.sleep(5)
        return
    elif line3 != line4:
        print("🔴 Your folders are not synced \n")
        print(f"{file_AC_2}: ❌ {line3}")
        print(f"{file_GC_2}: ❌ {line4} \n")
        time.sleep(2)
        print("🟢 Proceeding with ICOM build syncing...")
        time.sleep(5)
        return() 
    else:
        print("🟢 Your folders are synced. Congratulations")
        while True:
            continue_sync = input("⏩ Do you still want to proceed with sync? (y/n): ").lower()
            if continue_sync == "y":
                break
            elif continue_sync == "n":
                print("Script finished at", time.strftime('%x %X'))
                input("⏩ Press Enter to continue...")
                exit()

# Function to build AC/GC folders
def build(build_batch_file,build_folder):
    print("🟢 Running AC batch file:", build_batch_file)
    os.chdir(build_folder)
    subprocess.run([build_batch_file + ".bat"])
    return

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
# = = = = = = = = = = = = = = = START OF CODE FLOW  = = = = = = = = = = = = = = = 
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 


# Start log file
log_file = "logFile.txt"
with open(log_file, "a") as f:
    f.write(f"Script started at {time.strftime('%x %X')}\n")


# Prompt user for AC and GC folders
build_folder_AC = select_entry("⏩ Choose build folder for AC: ").upper()
build_folder_GC = select_entry("⏩ Choose build folder for GC: ").upper()

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

# Prompt user for build variants
os.chdir(main_folder + "/AC")
build_AC_batch = select_entry("⏩ Choose build variant for AC: ")
os.chdir(main_folder + "/GC")
build_GC_batch = select_entry("⏩ Choose build variant for GC: ")

# Run AC build
os.chdir(main_folder)
build(build_AC_batch,build_folder_AC)

# Copy files from AC to GC folder (dirs_exist_ok true: if directory is alr inside, overwrite)
print("🟢 Copying files from AC to GC")
time.sleep(2) #for debugging
os.chdir(os.path.dirname(os.getcwd())) # return to parent dir
shutil.copytree(os.path.join(os.getcwd(), build_folder_AC, "adapt", "gen", "ToFGC", "core", "pkg"),
                os.path.join(os.getcwd(), build_folder_GC, "core", "pkg"),
                dirs_exist_ok=True)

# Run GC build
build(build_GC_batch,build_folder_GC)

# Copy files from GC to AC folder
print("🟢 Copying files from GC to AC")
os.chdir(os.path.dirname(os.getcwd())) # return to parent dir
shutil.copytree(os.path.join(build_folder_GC, "adapt", "gen", "tofac", "core", "pkg"),
                os.path.join(build_folder_AC, "core", "pkg"),
                dirs_exist_ok=True)

# Run AC build again
build(build_AC_batch,build_folder_AC)

# Run get_prg and get_sym for AC
os.chdir(os.path.dirname(os.getcwd())) # return to parent dir
print("🟢 AC: Running get_prg and get_sym")
subprocess.run([os.path.join(os.getcwd(), build_folder_AC, "tool", "integration", "tool", "deliver", "core", "get_prg.bat")])
subprocess.run([os.path.join(os.getcwd(), build_folder_AC, "tool", "integration", "tool", "deliver", "core", "get_sym.bat")])

# Run get_prg and get_sym for GC
print("🟢 GC: Running get_prg and get_sym")
subprocess.run([os.path.join(build_folder_GC, "tool", "integration", "tool", "deliver", "core", "get_prg.bat")])
subprocess.run([os.path.join(build_folder_GC, "tool", "integration", "tool", "deliver", "core", "get_sym.bat")])

# End log file
with open(log_file, "a") as f:
    f.write(f"Script finished at {time.strftime('%x %X')}\n")
input("Press Enter to continue...")

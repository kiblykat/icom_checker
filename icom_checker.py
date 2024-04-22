import os
import subprocess
import shutil
import time

# = = = DEFINING FUNCTIONS = = = 

# Function to prompt user for folder selection
def select_folder(prompt_message):
    while True:
        folder_path = input(prompt_message)
        if os.path.exists(folder_path):
            return folder_path
        else:
            print("🔴 Project folder not found. Please check spelling.")

# Function to find line containing search word
def find_line(file_path):
    with open(file_path, "r") as file:
        for line in file:
            if search_word in line:
                return line.strip()
    return None

# = = = START OF CODE FLOW = = = 

# Start log file
log_file = "logFile.txt"
with open(log_file, "a") as f:
    f.write(f"Script started at {time.strftime('%x %X')}\n")


# Prompt user for AC and GC folders
build_folder_AC = select_folder("⏩ Choose build folder for AC: ")
build_folder_GC = select_folder("⏩ Choose build folder for GC: ")

# Set file paths
file_AC = os.path.join(build_folder_AC, "core", "pkg", "icom", "icom_export.sdh")
file_GC = os.path.join(build_folder_GC, "adapt", "gen", "tofac", "core", "pkg", "icom", "icom_export.sdh")

# Search word
search_word = "INTERFACEID"

# Find lines containing search word in AC and GC files
line1 = find_line(file_AC)
line2 = find_line(file_GC)

# Compare lines
if line1 is None:
    if line2 is None:
        print("INTERFACEID not found in either file.")
    else:
        print("INTERFACEID not found in", file_AC)
elif line2 is None:
    print("INTERFACEID not found in", file_GC)
else:
    if line1 == line2:
        print("Your folders are synced. Congratulations")
        while True:
            continue_sync = input("Do you still want to proceed with sync? (y/n): ").lower()
            if continue_sync == "y":
                break
            elif continue_sync == "n":
                print("Script finished at", time.strftime('%x %X'))
                input("Press Enter to continue...")
                exit()
    else:
        print("Your folders are not synced. Proceeding with ICOM build syncing...")
        time.sleep(2)
        print("Please gitclean project folders before running ICOM sync")
        time.sleep(5)

# Prompt user for build variants
build_AC = input("Choose build variant for AC: ")
build_GC = input("Choose build variant for GC: ")

# Run AC build
print("🟢 Running AC batch file:", build_AC)
os.chdir(build_folder_AC)
subprocess.run([build_AC + ".bat"])

# Copy files from AC to GC folder (dirs_exist_ok true: if directory is alr inside, overwrite)
print("🟢 Copying files from AC to GC")
time.sleep(2) #to comment
os.chdir(os.path.dirname(os.getcwd())) # return to parent dir
shutil.copytree(os.path.join(os.getcwd(), build_folder_AC, "adapt", "gen", "ToFGC", "core", "pkg"),
                os.path.join(os.getcwd(), build_folder_GC, "core", "pkg"),
                dirs_exist_ok=True)

# Run GC build
print("🟢 Running GC batch file:", build_GC)
print("CURRENT DIR" + os.getcwd())
os.chdir(build_folder_GC)
subprocess.run([build_GC + ".bat"])

# Copy files from GC to AC folder
print("🟢 Copying files from GC to AC")
os.chdir(os.path.dirname(os.getcwd())) # return to parent dir
shutil.copytree(os.path.join(build_folder_GC, "adapt", "gen", "tofac", "core", "pkg"),
                os.path.join(build_folder_AC, "core", "pkg"),
                dirs_exist_ok=True)

# Run AC build again
print("🟢 Running AC batch file again:", build_AC)
os.chdir(build_folder_AC)
subprocess.run([build_AC + ".bat"])

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

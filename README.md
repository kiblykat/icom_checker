# ICOM Sync Tool

1. Background
    - Motivation
2. Tool
    - Overview
    - How it works

## 1. Background

ICOM synchronization is an integral process to building and flashing our FPK and WHUD clusters.

This tool is meant to automate the process of ICOM Synchronization through the use of the .bat file.
<u>### 1.1 Motivation </u>
There are 3 main workflow 'hassles' that are present with the current process of ICOM syncing: 

#### 1. Tedious. </br>
It requires 'manual' labour of moving files from one project folder to another. The project folder structure is rather confusing. This may also lead to human errors that might waste more time.
#### 2. Requires user to be present after first and second build steps are finished. </br>
When a project folder finishes building, user needs to copy the files over and needs to proceed to the next step by building the next project folder. 
#### 3. Time-consuming </br>
The entire process of ICOM syncing can take ~4-5 hours
## 2. Tool 
This tool helps to reduce manual labour and reduce the propensity to make any errors within ICOM syncing process by automating the whole process from start to finish. This allows for the script to be run overnight.
### 2.1 Overview
The tool aims to achieve the following:

1. Immediate response from tool to check if icom is synced without digging through complicated file structure.
2. Eliminate manual labour of shifting and copying over files from one project folder to another is automated.
3. Eliminate the need for user to be present after each build process, by asking all input at the start of the whole process.
4. Allow for whole ICOM sync process to through a few inputs without further user interaction, allowing the ability to run it overnight.
5. Run the get_prg.bat and get_sym.bat files after ICOM sync so that user can immediately use the flashloader and flash cluster after sync is done.
### 2.2 How it works
1. Run the icom_checker.bat file icom_checker.py(type "python icom_checker.py" in console). User will be prompted to input AC and GC folders.
2. Depending on whether the user chooses FPKM, FPKE or WHUD: Program flow will differ according to choice.
3. The tool will then proceed with running the build-and-copy steps as shown in the overview image in Background:
    a. Build AC → copy AC to GC→ Build GC → copy GC to AC → Build AC
4. Tool will then run get_prg.bat and get_sym.bat files in the following locations <Project_Folder>/tool/integration/tool/deliver/core for FPKX projects (this differs for WHUD)
5. User can then proceed to flash the program into the cluster using .prg file that is generated in <Project_Folder>/adapt/out (pkg\fls\tool\mapscrpt\out for WHUD)

### Note: This is merely a helper tool. No proprietary files were uploaded into this github 


#imports
import os
import easygui

#prompt
easygui.msgbox("Please select the top level folder where the gamepass game is located.", "gHub GamesPass Profile Creator")

#get game directory 
gameDirectory = easygui.diropenbox()

#vars
exeFileLocations = []
logoFileNames = []
logoFileLocations = []

#find all exe files in the provided directory 
for (root, dirs, files) in os.walk(gameDirectory, topdown=True):
    for file in files:
        #get game files
        if file.endswith(".exe"):
            #add file location to list
            exeFileLocations.append(root + "\\" + file)
        #get logo files
        if file.endswith(".png"):
            #add file name to list
            logoFileNames.append(file)

            #add file location to list
            logoFileLocations.append(root + "\\" + file)

# create multiple choice select box with exe files
title='gHub GamesPass Profile Creator'
exeSelection=easygui.multchoicebox('Please select the exec files you would like the profile to be active on.', title, exeFileLocations, preselect=None)

#vars
looping = True
logoIndex = 0

# loop through all logo images in single msgbox to prevent overfill (There is definitely a better way to do this I am just lazy)
while looping:
        
    #create msgbox with all buttons (can go back or fourth)
    if logoIndex > 0 and logoIndex < len(logoFileLocations) - 1:
        response = easygui.buttonbox("Do you want to use this image as the logo?", image=logoFileLocations[logoIndex], choices=["Previous Image", "Use this Image", "Next Image"])
    #create msgbox with back button (at end of list)
    elif logoIndex > 0 and logoIndex == len(logoFileLocations) -1 :
        response = easygui.buttonbox("Do you want to use this image as the logo?", image=logoFileLocations[logoIndex], choices=["Previous Image", "Use this Image"])
    #create msgbox with next button (at front of list)
    elif logoIndex == 0 and logoIndex < len(logoFileLocations) - 1:
        response = easygui.buttonbox("Do you want to use this image as the logo?", image=logoFileLocations[logoIndex], choices=["Use this Image", "Next Image"])
    #error
    else:
        logoIndex = 0

    #image chosen
    if response == "Use this Image":
        looping = False
    #next button clicked
    elif response == "Next Image":
        logoIndex += 1
    #back button clicked
    elif response == "Previous Image":
        logoIndex -= 1


# get name of the profile
profileName = easygui.enterbox("Please enter the name of the profile")

#edit the paths in exeFileLocations to have // instead of /
for exeFileIndex in range(len(exeSelection)):
    exeSelection[exeFileIndex] = exeSelection[exeFileIndex].replace("\\", "\\\\")

#edit the paths in logoFileLocations to have // instead of /
for logoFileIndex in range(len(logoFileLocations)):
    logoFileLocations[logoFileIndex] = logoFileLocations[logoFileIndex].replace("\\", "\\\\")

#create text to input into settings file (for single application)
if len(exeSelection) == 1:
    profileText = """
    {
        "applicationId": "REPLACE WITH APPLICATION ID",
        "applicationPath": "%s",
        "isCustom": true,
        "name": "%s",
        "posterPath": "%s"
    }
    """%(exeSelection[0], profileName, logoFileLocations[logoIndex])
#more than one application selected
else:
    #vars
    firstPath = exeSelection.pop()

    for currentString in exeSelection:
        otherPaths = """"%s","""%(currentString)

        profileText = """
        {
            "applicationId": "REPLACE WITH APPLICATION ID",
            "applicationPath": "%s",
            "isCustom": true,
            "name": "%s",
            "posterPath": "%s",
            "userPaths": [
            %s
            ]
        }
        """%(exeSelection[0], profileName, logoFileLocations[logoIndex], otherPaths)

#write output to file
f = open("profileTextOutput.txt", "w")
f.write(profileText)

    

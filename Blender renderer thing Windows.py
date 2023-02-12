#Blender renderer thing
ver = "2.0"
import base64
from tarfile import DEFAULT_FORMAT
import PySimpleGUI as sg
import tkinter
from tkinter import Button, filedialog
import os
import sys
import subprocess
import webbrowser
import requests
import pickle


def findThemes():
    themes = []
    files = os.listdir("Themes/")
    for line in files:
        size = len(line)
        filetype = line[size-5:]
        if filetype == "theme":
            themes.append(line[:size-6])
    return(themes)
def getTheme(themeName):
    with open("Themes/" + themeName + ".theme") as f:
        lines = f.readlines()
        command = []
        var = []
        isVar = 0
        for line in lines:

            size = len(line)
            NewLine = line[:size-1]

            if isVar == 1:
                var.append(NewLine)
            if isVar == 0:
                if NewLine != "images":
                    command.append(NewLine)
                if NewLine == "images":
                    isVar = 1
    return[command, var]

#sg.set_options(font=("Ariel, 10"))
sg.set_options(icon=base64.b64encode(open(r'icon.png', 'rb').read()))

sg.theme('Black')
sg.theme_background_color("#0f0f0f")
sg.theme_text_element_background_color("#0f0f0f")
sg.theme_element_background_color("#0f0f0f")
buttonTextColor = "white"
ButtonIMG = "Themes/Dark/button.png"

def check_for_update(version):
    latestresponse = requests.get("https://raw.githubusercontent.com/AbsoluteGirth/BlenderRendererThing/main/LatestVersion")
    latest = latestresponse.text[:3]
    if version != latest:
        patchnotes = requests.get("https://raw.githubusercontent.com/AbsoluteGirth/BlenderRendererThing/main/Patchnotes")
        layout = [  [sg.Text('New update available!')],
                    [sg.Text('Patchnotes:')],
                    [sg.Text(str(patchnotes.text))],
                    [sg.Button('Update now!', border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(1, 10)), sg.Button("Remind me later", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(1, 10))]]
        window = sg.Window("Update available!", layout)
        while True:
            event, values = window.read()
            # End program if user closes window or
            # presses the OK button
            if event == "Remind me later":
                window.close()
                break
            if event == "Update now!":
                webbrowser.open("https://github.com/assfartman/Blender-Render-Queue/releases")
                window.close()
                break
            elif event == sg.WIN_CLOSED:
                sys.exit() 
def set_blender_path():
    list_of_lines = ["", "", ""]
    list_of_lines[0] = ("\n")
    list_of_lines[1] = ("False")
    list_of_lines[2] = ("\nDark")
    with open("BlenderRendererThingPrefs", "w+") as f:
        f.writelines(list_of_lines)
        f.close

#startup shit
check_for_update(ver)
if os.path.exists("Render.command") == True:
    os.remove("Render.command")
if os.path.exists("BlenderRendererThingPrefs") == False:
    set_blender_path()
f = open("BlenderRendererThingPrefs", "r")
prefs = f.readlines()
f.close
blenderpath = prefs[0]
skip_dono = prefs[1]
theme = prefs[2]

#get themes
themes = findThemes()
themeFile = getTheme(theme)
Commands = themeFile[0]
Images = themeFile[1]

#set theme
for line in Commands:
    exec(line)
disabledColor = Images[0]
buttonTextColor = Images[1]
ButtonIMG = Images[2]
ButtonEditIMG = Images[3]
ButtonRenderIMG = Images[4]

def main(files, args):   
    MenuLayout =    [
                        ["File", ["New session", "Save session", "Open session", "Preferences"]],
                        ["About", ["About"]]
                    ]  
    Title =     [
                    [sg.Menu(MenuLayout)],
                    [sg.Text("Filename", size=(68)), sg.VerticalSeparator(), sg.Text("Arguments", size=(45))], 
                    [sg.HorizontalSeparator()]
                ]
    Files = []
    line = []
    Files.extend(line)
    lineNum = 0
    for blend in files:
        line = [[sg.InputText(default_text=(blend), readonly=True, disabled_readonly_background_color=(disabledColor), p=(0,1), border_width=(3), size=(70)), sg.InputText(default_text=(args[lineNum]), readonly=True, disabled_readonly_background_color=(disabledColor), p=(0,1), border_width=(3), size=(20)), sg.Button("Edit", p=(0,1), k=str(str(lineNum) + "e"), border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonEditIMG)), sg.Button("Remove", p=(0,1), k=str(str(lineNum) + "r"), border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonRenderIMG))]]
        Files.extend(line)
        lineNum = lineNum + 1

    Preferences =[
                    [sg.HorizontalSeparator()],
                    [sg.Button("Add files", k="add", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(1, 10)), sg.Sizer(h_pixels=480), sg.Button("Start render", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonRenderIMG), p=(0, 10)), sg.Button("Save command", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonRenderIMG), p=(0, 10))]
                ]
    Console =   [
                    [sg.Output(size=(116,11), background_color=disabledColor, sbar_background_color=("#666666"))]
                ]
    layout =    [
                    [sg.Column(Title, size=(830, 40))], [sg.Column(Files, scrollable=True, vertical_scroll_only=True, sbar_background_color=("#666666"),  size=(830, 300))], [sg.Column(Preferences, size=(830, 55))], [sg.Frame("Console", Console)]
                ]
    mainWindow = sg.Window('Blender Renderer Thing', layout, size=(875,625), icon=base64.b64encode(open(r'icon.png', 'rb').read()))
    while True:
        event, values = mainWindow.Read()
        #mainWindow.set_title("Blender Renderer Thing")
        if event == sg.WIN_CLOSED:
            donowindow()

        if event == "New session":
            if confirmNewSession() != None:
                mainWindow.close()
                return("remove", [] ,[])

        if event == "Start render":
            generateCommand(files, args)
            print("Starting render")
            print("Window will become unresponsive while render in progress")
            runCommand("Render.command", None, mainWindow)
            os.remove("Render.command")

        if event == "About":
            aboutWindow()
        if event == "Save session":
            saveDIR = saveSessionPath()
            if saveDIR != None:
                saveSession(saveDIR)

        if event == "Preferences":
            PreferencesWindow()

        if event == "Open session":
            if confirmOpenSession() != None:
                openDIR = openSessionPath()
                if openDIR != None:
                    openedFile = openSession(openDIR)
                    openfile = openedFile[0]
                    openargs = openedFile[1]
                    mainWindow.close()
                    return("remove", openfile, openargs)

        if event == "Save command":
            saveDIR = savePath()
            if saveDIR != None:
                generateCommand(files, args, saveDIR)
        if event == "add":
            Render_flags_new = []
            filesnew = (search_for_new_file_path())
            if filesnew == None:
                mainWindow.close()
                return
            for blend in filesnew:
                argsnew = arg_window(blend)
                Render_flags_new.append(argsnew)
                #listpos = listpos + 1
            mainWindow.close()
            return["add", filesnew, Render_flags_new]
        if event[:1].isdigit() == True:
            if event[1:] == "e":
                newarg = arg_edit(files, int(event[:1]))
                if newarg != None:
                    mainWindow.close()
                    return("edit", newarg, event[:1])
            if event [1:] == "r":
                del files[int(event[:1])]
                del args[int(event[:1])]
                mainWindow.close()
                return("remove", files, args)

def PreferencesWindow():

    title =         [
                        [sg.Text("Preferences")],
                        [sg.HorizontalSeparator()]
                    ]

    Preferences =    [
                        [sg.Text("Theme:")],
                        [sg.OptionMenu(themes, k=("themeSelect"), default_value=theme, background_color=disabledColor), sg.Button("Open folder", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonRenderIMG))],
                        [sg.Sizer(5,100)]
                    ]

    buttons =       [
                        [sg.HorizontalSeparator()],
                        [sg.Sizer(225), sg.Button("Apply", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(1, 10)), sg.Button("Cancel", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(10, 10))]
                        
                    ]

    layout =        [
                        [sg.Column(title)],
                        [sg.Column(Preferences)],
                        [sg.VPush(), sg.Column(buttons)]
                    ]
        
    window = sg.Window('Preferences', layout, size=(500,320))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            return       
        if event == "Open folder":
            subprocess.call(["open", "./Themes/"])
        if event == "Cancel":
            window.close()
            return
        if event == "Apply":
            newTheme = values["themeSelect"]
            status = updatePrefs(newTheme)
            if status == "updated":
                window.close()
                return
            if status == "cancelled":
                window["pathBox"].update(blenderpath)
                window["themeSelect"].update(theme)
                window.refresh()
def updatePrefs(newTheme):
    lol = []
    f = open("BlenderRendererThingPrefs", "r")
    lol = f.readlines()
    f.close
    lol[0] = ("\n")
    lol[2] = newTheme
    if confirmPopup() == "confirm":
        f = open("BlenderRendererThingPrefs", "w+")
        f.writelines(lol)
        f.close
        return("updated")
    else:
        return("cancelled")
def confirmPopup():
    layout =    [
                    [sg.Text("Apply changes?")],
                    [sg.Text("(changes will apply after restart)")],
                    [sg.Button("Confirm", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(1, 10)), sg.Button("Cancel", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(1, 10))]
                ]
    window = sg.Window("Apply changes?", layout)
    while True:
        event, values = window.read()
        if event == "Confirm":
            window.close()
            return("confirm")
        else:
            window.close()
            return
def aboutWindow():    
    layout =    [
                    [sg.Image("Logo.png", subsample=2)],
                    [sg.Text("Version " + str(ver))],
                    [sg.Text("Special thanks to StackOverflow")],
                    [sg.Text("for writing more code in this project than me")],
                    [sg.Text("Support the program? Donations help keep programs like this free for everyone!")],
                    [sg.Button("Donate now!", k="dono", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(1, 10)), 
                    sg.Button("Done", k="Done", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(1, 10)),
                    sg.Button("GitHub", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(1, 10))]
                ]

    window = sg.Window("About", layout, element_justification="c")
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            return()
        if event == "GitHub":
            webbrowser.open("https://github.com/AbsoluteGirth/BlenderRendererThing/tree/main")
        if event == "dono":
            webbrowser.open("https://www.buymeacoffee.com/AbsoluteGirth")
        if event == "Done":
            window.close()
            return()
def savePath():
    currdir = os.getcwd()
    root = tkinter.Tk()
    savedir = filedialog.asksaveasfilename(initialfile="Render.command", parent=root, initialdir="shell:::{5b934b42-522b-4c34-bbfe-37a3ef7b9c90}", defaultextension=".command", title='Select output file', filetypes=[("Command", "*.command")])
    root.destroy()
    if len(savedir) == 0:
        return
    return(savedir)
def saveSessionPath():
    currdir = os.getcwd()
    root = tkinter.Tk()
    savedir = filedialog.asksaveasfilename(initialfile="session.brts", parent=root, initialdir="shell:::{5b934b42-522b-4c34-bbfe-37a3ef7b9c90}", defaultextension=".brts", title='Save session', filetypes=[("Session File", "*.brts")])
    root.destroy()
    if len(savedir) == 0:
        return
    return(savedir)
def openSessionPath():
    currdir = os.getcwd()
    root = tkinter.Tk()
    savedir = filedialog.askopenfilename(initialfile="session.brts", parent=root, initialdir="shell:::{5b934b42-522b-4c34-bbfe-37a3ef7b9c90}", defaultextension=".brts", title='Open session', filetypes=[("Session File", "*.brts")])
    root.destroy()
    if len(savedir) == 0:
        return
    return(savedir)
def saveSession(savePath):
    lines = [file_import, Render_flags]
    with open(str(savePath), "wb") as f:
#        f.write(str(lines[0]))
#        f.write("\n")
#        f.write(str(lines[1]))
        pickle.dump(lines, f)

    return()
def openSession(openPath):
    f = open(str(openPath), "rb")
#    openList = f.readlines()
#    newfilesx = openList[0]
#    newflags = openList[1]
#    newfiles = str(newfilesx[:1])
    openList = pickle.load(f)
    f.close
    return(openList)
def generateCommand(files, args, path=os.getcwd()+"/"+"Render.command"):
    #generate text
    Render_command_list = []
    listpos = 0
    for blend in files:
        Render_command_list.append('"' + blend + '" ')
        Render_command_list.append(args[listpos] + " ")
        listpos = listpos + 1
    size = len(blenderpath)
    Render_command = "".join(Render_command_list)
    lines = ["blender", " -b " +  Render_command, "\necho Render Finished!"]

    #write to file
    with open(os.open(str(path), os.O_CREAT | os.O_WRONLY, 0o777), "w+") as f:
        for line in lines:
            f.write(line)
    return()
def runCommand(cmd, timeout=None, window=None):
    p = subprocess.Popen("'"+os.getcwd()+"/"+cmd+"'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        window.Refresh() if window else None        # yes, a 1-line if, so shoot me
#    retval = p.wait(timeout)
    return (output)
def search_for_new_file_path ():
    currdir = os.getcwd()
    root = tkinter.Tk()
    tempdir = filedialog.askopenfilenames(parent=root, initialdir="shell:::{20D04FE0-3AEA-1069-A2D8-08002B30309D}", title='Select files to be rendered', filetypes=[("Blender files", "*.blend")])
    root.destroy()
    if len(tempdir) == 0:
        return
    return tempdir
def arg_window(filename):
    layout1 =   [
                    [sg.Text(filename)], 
                    [sg.InputText(default_text=("1"), k="imageFrame", size=(4, 5)), sg.Text("Frame to be rendered")],
                    #[sg.Text("Set custom output path (leave if you set it in blender)")],
                    #[sg.Button("Select output file", k="selfile")],
                    [sg.VPush()],
                    [sg.Push(), sg.Button("Confirm", k="confirmImage", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(10, 10))]
                ]

    layout2 =   [
                    [sg.Text(filename)],
                    [sg.Checkbox("Use frames set by project", default=True, k="projectFrames")],
                    [sg.InputText(default_text=("1"), k="startFrame", size=(4, 5)), sg.Text("Start frame")],
                    [sg.InputText(default_text=("1"), k="endFrame", size=(4, 5)), sg.Text("End frame")],
                    #[sg.Text("Set custom output path (leave if you set it in blender)")],
                    #[sg.Button("Select output directory", k="seldir")],
                    [sg.VPush()],
                    [sg.Push(), sg.Button("Confirm", k="confirmAnim", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(10, 10))]
                ]

    layout3 =   [
                    [sg.Text(filename)], 
                    [sg.Text("Input custom arguments here")],
                    [sg.InputText(k="customArgs")],
                    [sg.VPush()],
                    [sg.Push(), sg.Button("Confirm", k="confirmCustom", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(10, 10))]
                ]

    tabgroup =  [
                    [sg.TabGroup([[
                                sg.Tab("Image", layout1),
                                sg.Tab("Animation", layout2),
                                sg.Tab("Custom", layout3)]], 
                                selected_background_color=sg.theme_background_color(), s=(500, 175)
                        )
                    ]
                ]
    
    window = sg.Window("Set render arguments", tabgroup)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            return
        if event == "confirmImage":
            returnImage = ("-x 1 -f " + values["imageFrame"])
            window.close()
            return(returnImage)

        if event == "confirmAnim":
            if values["projectFrames"] == False:
                returnAnim = ("-x 1 -s " + values["startFrame"] + " -e " + values["endFrame"])
                window.close()
                return(returnAnim)
            elif values["projectFrames"] == True:
                window.close()
                returnAnim = ("-x 1 -a")
                return(returnAnim)

        if event == "confirmCustom":
            window.close()
            return(values["customArgs"])
        if event == "Cancel":
            window.close()
            return()
def arg_edit(files, listpos):
    layout1 =   [
                    [sg.Text(files[listpos])], 
                    [sg.InputText(default_text=("1"), k="imageFrame", size=(4, 5)), sg.Text("Frame to be rendered")],
                    #[sg.Text("Set custom output path (leave if you set it in blender)")],
                    #[sg.Button("Select output file", k="selfile")],
                    [sg.VPush()],
                    [sg.Push(), sg.Button("Confirm", k="confirmImage", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(1, 10)), sg.Button("Cancel", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(10, 10))]
                ]

    layout2 =   [
                    [sg.Text(files[listpos])],
                    [sg.Checkbox("Use frames set by project", default=True, k="projectFrames")],
                    [sg.InputText(default_text=("1"), k="startFrame", size=(4, 5)), sg.Text("Start frame")],
                    [sg.InputText(default_text=("1"), k="endFrame", size=(4, 5)), sg.Text("End frame")],
                    #[sg.Text("Set custom output path (leave if you set it in blender)")],
                    #[sg.Button("Select output directory", k="seldir")],
                    [sg.VPush()],
                    [sg.Push(), sg.Button("Confirm", k="confirmAnim", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(1, 10)), sg.Button("Cancel", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(10, 10))]
                ]

    layout3 =   [
                    [sg.Text(files[listpos])], 
                    [sg.Text("Input custom arguments here")],
                    [sg.InputText(k="customArgs")],
                    [sg.VPush()],
                    [sg.Push(), sg.Button("Confirm", k="confirmCustom", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(1, 10)), sg.Button("Cancel", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(10, 10))]
                ]

    tabgroup =  [
                    [sg.TabGroup([[
                                sg.Tab("Image", layout1),
                                sg.Tab("Animation", layout2),
                                sg.Tab("Custom", layout3)]], 
                                selected_background_color=sg.theme_background_color(), s=(500, 175)
                        )
                    ]
                ]
    
    window = sg.Window("Edit render arguments", tabgroup)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            return
        if event == "confirmImage":
            returnImage = ("-x 1 -f " + values["imageFrame"])
            window.close()
            return(returnImage)

        if event == "confirmAnim":
            if values["projectFrames"] == False:
                returnAnim = ("-x 1 -s " + values["startFrame"] + " -e " + values["endFrame"])
                window.close()
                return(returnAnim)
            elif values["projectFrames"] == True:
                window.close()
                returnAnim = ("-x 1 -a")
                return(returnAnim)

        if event == "confirmCustom":
            window.close()
            return(values["customArgs"])
        if event == "Cancel":
            window.close()
            return
def donowindow():
    if skip_dono == "False\n":
        layout =    [
                        [sg.Text("Enjoying the program?")], [sg.Text("A donation would be greatly appreciated!"), sg.Sizer(40,0)], 
                        [sg.Button("Yes!", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonRenderIMG)), sg.Button("Not right now", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonRenderIMG))],
                        [sg.Push(), sg.Text("Don't show again"), sg.Checkbox("", k="Don't show again", pad=(1,1))]
                    ]
        window = sg.Window("Thanks for using my program!", layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                sys.exit()
            elif event == "Yes!":
                webbrowser.open("https://www.buymeacoffee.com/AbsoluteGirth")
                if values["Don't show again"] == True:
                    window.close()
                    f = open("BlenderRendererThingPrefs", "r")
                    lol = f.readlines()
                    f.close
                    f = open("BlenderRendererThingPrefs", "w")
                    lol[1] = "True\n"
                    f.writelines(lol)
                    f.close
                    sys.exit()
                else:
                    window.close()
                    break
            elif event == "Not right now":
                if values["Don't show again"] == True:
                    window.close()
                    f = open("BlenderRendererThingPrefs", "r")
                    lol = f.readlines()
                    f.close
                    f = open("BlenderRendererThingPrefs", "w")
                    lol[1] = "True\n"
                    f.writelines(lol)
                    f.close
                    sys.exit()
                else:
                    window.close()
                    break
        
        sys.exit()
    else:
        sys.exit()
def confirmNewSession():
    layout =    [
                    [sg.Text("Start new session?")],
                    [sg.Text("any unsaved changes will be lost")],
                    [sg.Button("Confirm", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(1, 10)), sg.Button("Cancel", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(1, 10))]
                ]
    window = sg.Window("New session?", layout)
    while True:
        event, values = window.read()
        if event == "Confirm":
            window.close()
            return("confirm")
        else:
            window.close()
            return
def confirmOpenSession():
    layout =    [
                    [sg.Text("Open session?")],
                    [sg.Text("any unsaved changes will be lost")],
                    [sg.Button("Confirm", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(1, 10)), sg.Button("Cancel", border_width="0", button_color=(buttonTextColor,sg.theme_background_color()), mouseover_colors=(buttonTextColor, sg.theme_background_color()), image_source=(ButtonIMG), p=(1, 10))]
                ]
    window = sg.Window("Open session?", layout)
    while True:
        event, values = window.read()
        if event == "Confirm":
            window.close()
            return("confirm")
        else:
            window.close()
            return


file_import = []
Render_flags = []

file_open = (sys.argv)
file_open.append("none")
if file_open[1] != "none":
    file_open_fixed = file_open[1].replace("\\","/")
    openedFile = openSession(file_open_fixed)
    file_import = openedFile[0]
    Render_flags = openedFile[1]

while True:
    fromMain = main(file_import, Render_flags)
    if fromMain != None:
        returnReason = fromMain[0]
        if returnReason == "add":
            file_import.extend(fromMain[1])
            Render_flags.extend(fromMain[2])
        if returnReason == "edit":
            newarg = fromMain[1]
            argno = int(fromMain[2])
            Render_flags[argno] = newarg
        if returnReason == "remove":
            file_import = fromMain[1]
            Render_flags = fromMain[2]

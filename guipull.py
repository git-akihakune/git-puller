#!/usr/bin/env python3

## PySimpleGUI installing instructions:
## Run one if these commands:
## - py -m pip install pysimplegui
## - pip install pysimplegui
## - pip3 install pysimplegui
## If there's Tkinter error afterwards, install `python-tk` or `python3-tk` from your package manager

import os
from typing import List

try:
    import PySimpleGUI as sg
except ModuleNotFoundError:
    print("PySimpleGUI was not installed properly. See installing instructions in the script.")
    exit()


def createWindow():
    sg.theme("DarkBlack")

    optionColumn = [
            [sg.Text('✦Git Recursive Puller✦', font='Atari-Regular 30')],
            [sg.Text('Command to run: '), sg.InputText(default_text="git pull", focus=False)],
            [sg.Text('Path to executing directory: '), sg.InputText()],
            [sg.Text('Excluding paths: '), sg.InputText()],
        ]
    layout = [
        [
            sg.Column(optionColumn),
            sg.VSeparator(),
            sg.Column([[sg.Output(size=(40,15))]])
        ],
        [sg.Button('Run'), sg.Button('Cancel')]
    ]
    window = sg.Window('Git Puller', layout)
    return window


def recursivePull(directories: List[str], exclude: List[str], command: str) -> None:
    def changeDirectory(r_path):  
        ack = 1
        try:
            root = os.path.dirname(__file__)
            rel_path = os.path.join("..", r_path)

            abs_path = os.path.join(root, rel_path)
            os.chdir(abs_path)
            ack = 0
        except Exception as details:
            print('problem to get to the path '+r_path+' (0001) : ' + str(details))
        return ack

    print(f"[@] Working with configurations:\n- Executing directories: {directories}\n- Excluding: {exclude}\n- Command: {command}\n")
    print("[!] Operation started\n")

    for directory in directories:
        for root, dirs, files in os.walk(directory, topdown=True):

            if '.git' in dirs and root.split('/')[-1] not in exclude:
                print(f"[*] Running {command} on {root}")
                changeDirectory(root)
                print(os.popen(command).read())

            dirs[:] = [d for d in dirs if d not in ['.git']]
        
    print("[+] Operation successfully completed")
    

def main():
    window = createWindow()
    while True:
        event, values = window.read()
        if event in [sg.WIN_CLOSED, 'Cancel']:
            break

        command = values[0]
        directories = values[1].split()
        exclude = values[2]
        recursivePull(directories, exclude, command)
        
    window.close()


if __name__ == '__main__':
    main()
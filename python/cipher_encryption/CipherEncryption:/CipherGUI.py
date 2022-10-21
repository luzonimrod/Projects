import PySimpleGUI as sg
import tkinter as tk
from CipherEncryption.Encryption import encryption
sg.theme('DarkAmber')
layout = [ [sg.Text("Welcome To Caesar Cipher !")],
            [sg.Text("Please enter the words you want to encrypt:")],
            [sg.Input()],
            [sg.Button('SUBMIT')],
            [sg.Button('SUBMIT',visible=False,bind_return_key=True)]
           ]

window=sg.Window("Caesar Cipher",layout)
event,values=window.read()
cipher=values[0]

result=encryption(cipher)

sg.popup("The new Encryption is: ",result)








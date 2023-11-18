################################################################################
##                                                                            ##
##  ██████  ████████          █████                                           ##
##    ██       ██     ████   ██   ██                                          ##
##    ██       ██   ██    ██ ███████                                          ##
##    ██       ██   ██    ██ ██   ██                                          ##
##  ██████     ██     ████   ██   ██                                          ##
##                                                                            ##
##  BY SLAVLASAGNA                                                            ##
##                                                                            ##
##  Thank you for using it!                                                   ##
##                                                                            ##
################################################################################

### libs import
import PIL.Image
from PIL.ImageOps import invert
import PIL.ImageGrab
import easygui as gui
import pyperclip
import requests

box_title = "IToA - Image to ASCII Converter !"                 # Box title, common to all the boxes

title = """████ ████████        █████  
 ██     ██    ████  ██   ██ 
 ██     ██   ██  ██ ███████ 
 ██     ██   ██  ██ ██   ██ 
████    ██    ████  ██   ██"""                                  # This is the name of the program in Ascii

author = """ _____ _             _                                       
/  ___| |           | |                                      
\ `--.| | __ ___   _| |     __ _ ___  __ _  __ _ _ __   __ _ 
 `--. \ |/ _` \ \ / / |    / _` / __|/ _` |/ _` | '_ \ / _` |
/\__/ / | (_| |\ V /| |___| (_| \__ \ (_| | (_| | | | | (_| |
\____/|_|\__,_| \_/ \_____/\__,_|___/\__,_|\__, |_| |_|\__,_|
                                            __/ |            
                                           |___/             """ # This is my pseudo in Ascii
                                           
icon = r"./_internal/itoa.ico"

######################################################################################################################################################################################
### /!\ Except the finish_flag Yes/No box, every easygui box have a "if box == None: finish_flag = True; break" that will close the program if the close/cancel button is pressed ###
######################################################################################################################################################################################

# "Yes/No" box : displays the welcoming message and asks between Yes or No -> Yes returns True, No returns False;
# -> finish_flag gets the opposite value of the "Yes/No" box
finish_flag = not gui.ynbox(f"Welcome on \n\n{title}\n\nthe ASCII picture converter (IToA stands for Image To Ascii)!\n\nWanna get started with this crap ?",
                            title=box_title,
                            icon=icon)

# while loop : runs the script until the finish flag is True
while finish_flag == False:
        
    # "while True: try: except:" loop : asks from where to choose the file/file path and checks if valid (-> raises error if not and exits the program)
    while True:
        img = None
        # "Button" box : gives plenty choices to the user to click on -> see options on commentaries below
        choice = gui.buttonbox("Choose where to pick the image :",
                               title=box_title,
                               choices=('Direct Path','Open Explorer','Clipboard','URL'),
                               icon=icon)
        if choice == None:
            finish_flag = True
            break

        try:
            if choice == 'Direct Path':                                                 ####### Direct path choice :
                path = gui.enterbox("Enter file path :",                                # . The user enters a file path
                                    title=box_title,                                    # |
                                    icon=icon)                                          # |
                error_msg = "Invalid path, please retry..."                             # . Sets the error message in case the path given is invalid
                img = PIL.Image.open(path)                                              # . Tries to open the image from path with PIL.Image

            elif choice == 'Open Explorer':                                             ####### Open explorer choice :
                path = gui.fileopenbox(msg="Choose a picture to convert...",            # . Opens file explorer and gets the path of the chosen file
                                       title=box_title)                                 # |
                error_msg = "Invalid file, please retry..."                             # . Sets the error message in case the file is not an image
                img = PIL.Image.open(path)                                              # . Tries to open the image from path with PIL.Image

            elif choice == 'Clipboard':                                                 ####### Clipboard option :
                path = ''                                                               #
                error_msg = "No image in the clipboard, please retry..."                # . Sets the error message if there's no file in the clipboard
                img = PIL.ImageGrab.grabclipboard()                                     # . Tries to grab the image from clipboard with PIL.ImageGrab
                error_msg = "Invalid image type, please retry..."                       # . Sets the error message if the clipboard's content is invalid
                img.verify()                                                            # . Checks if the clipboard's content is valid
                
            elif choice == 'URL':                                                       ####### URL option :
                path = gui.enterbox("Enter file URL :",                                 # . The user enters a file URL 
                                    title=box_title,                                    # |
                                    icon=icon)                                          # |
                error_msg = "Invalid URL, please retry..."                              # . Sets the error message for an invalid URL
                img = PIL.Image.open(requests.get(path, stream=True).raw)               # . Tries to open the image from URL using PIL.Image and requests
                
            if img == None:                                                             ### If there's no image in the end
                    raise FileNotFoundError()

            break                                                                       ### Gets out of the while loop if there's no error
        except:
            if gui.buttonbox(msg=error_msg,                                             # . Opens a message box that displays there's an error
                             title=box_title,                                           # |
                             choices=["Retry"],                                         # |
                             icon=icon) == None:                                        # . See /!\ at the beginning
                finish_flag = True                                                      # |
                break                                                                   # |
    
    if img == None:
        break
    
    width, height = img.size                                                # Grab width and height of the image
    aspect_ratio = height/width                                             # Stores the ratio width/height
        
    new_width = gui.integerbox(f"Enter the width of the final image (original size : {width}x{height}) :",  # . Opens a box that asks the user an interger between 1 and the original size of the image
                               title=box_title,                                                             # |
                               lowerbound=1,                                                                # |
                               upperbound=width,                                                            # |
                               icon=icon)                                                                   # |
    if new_width == None:                                                                                   # . See /!\ at the beginning
        finish_flag = True                                                                                  # |
        break                                                                                               # |

    new_height = aspect_ratio * new_width * 0.5                             # Stores the height of the new picture in a var
    img = img.resize((new_width, int(new_height)))                          # Resizes the image to the new dimensions
    img = img.convert('L')                                                  # Convert the picture in black and white

    # Message asked in the next box
    chars_msg = """Do you want to create the ascii image 
    with this set (0) : \"@%$#+=;:,. \"
    Or this set (1) : \"\u2588\u2593\u2592\u2591 \"
    Or this set (2) : \"@%#$§80o+=;:-,. \"
    Or a custom set (3) ?"""

    # Asks about the characters set used for the ASCII image
    chars_ans = gui.buttonbox(msg=chars_msg,                                                            # . "Button" box : asks between 4 choices
                              title=box_title,                                                          # |
                              choices=('0','1','2','3'),                                                # |
                              icon=icon)                                                                # |
    if chars_ans == None:                                                                               # . See /!\ at the beginning
        finish_flag = True                                                                              # |
        break                                                                                           # |

    if chars_ans == '0':                                                                                # . Basic set of chars
        chars = ["@", "%", "$", "#", "+", "=", ";", ":", ",", ".", " "]                                 # |
    elif chars_ans == '1':                                                                              # . Unicode set of full (I mean the fill the entire space) chars
        chars = ["\u2588","\u2588","\u2593","\u2593","\u2592","\u2592","\u2591","\u2591"," "," "," "]   # |
    elif chars_ans == '2':                                                                              # . Detailed set of chars
        chars = ["@", "%", "#", "$", "§", "8", "0", "o", "+", "=", ";", ":", "-", ",", ".", " "]        # |
    elif chars_ans == '3':                                                                              # . Custom set of chars (asked by an "enter" box)
        chars = gui.enterbox(msg="Enter the custom set (split each of the characters with \\)\n\nThere needs to be at least 10 characters to work properly",
                             title=box_title,
                             icon=icon).split("\\")
        if chars == None:                                                                               # . See /!\ at the beginning
            finish_flag = True                                                                          # |
            break                                                                                       # |

    # Message asked in the next box
    invert_msg = "Do you want the image colors to be inverted ? (for example if you want to copy to Discord, Steam, etc.)"

    # Asks if the image needs to be reversed
    inverted = gui.ynbox(msg=invert_msg,title=box_title,icon=icon)              # . "Yes/No" box
    if inverted == None:                                                        # . See /!\ at the beginning
        finish_flag = True                                                      # |
        break                                                                   # |
    if inverted: invert(img)                                                    # . Reverse the image b/w
        
    pixels = img.getdata()                                                                                      # Gets all the pixels data from the image
    new_pixels = [chars[pixel//25] for pixel in pixels]                                                         # Assign a certain character to each pixel in the image
    new_pixels = ''.join(new_pixels)                                                                            # Joins all the characters together
    new_pixels_count = len(new_pixels)                                                                          # Stores the number of chars in the image in a new var
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]      # Divide the line of chars to match the height of the image
    ascii_image = "\n".join(ascii_image)                                                                        # Joins the new lines created to form the ASCII image

    # Message asked in the next box
    filewrite_msg = """Copy to clipboard, write in a file, or display the image in a window ?
    
    - note that option 2 won't display the best way and will display correctly pictures only up to a relatively small width -"""

    # Asks what to do with the final image
    filewrite = gui.buttonbox(msg=filewrite_msg,                                    # . "Button" box
                              title=box_title,                                      # |
                              choices=('Copy','Save','Display'),                    # |
                              icon=icon)                                            # |
    if filewrite == None :                                                          # . See /!\ at the beginning
        finish_flag = True                                                          # |
        break                                                                       # |

    if filewrite == 'Copy':                                                                                                     # . Copies the image to clipboard
        clipboard = pyperclip.copy(ascii_image)                                                                                 # |
    elif filewrite == 'Save':                                                                                                   # . Asks the user to write a name
        filename = gui.enterbox(msg="Enter the name of the file (the extension of the file will be .txt):",                     # | for the file and saves it in the same 
                                title=box_title,                                                                                # | directory as the program is
                                icon=icon)                                                                                      # |
        if filename == None:                                                                                                    # | . See /!\ at the beginning
            finish_flag = True                                                                                                  # | |
            break                                                                                                               # | |
        with open(filename + ".txt", "w", encoding="utf-8") as f:                                                               # |
            f.write(ascii_image)                                                                                                # |
    elif filewrite == 'Display':                                                                                                # . Opens a new "code" box that displays
        gui.codebox(msg=ascii_image,                                                                                            # | the image with a monospace font
                    title=box_title)                                                                                            # |

    # "Yes/No" box : displays the exit message and asks between Yes or No -> Yes returns True, No returns False; 
    # -> finish_flag gets the opposite value of the "Yes/No" box
    finish_flag = not gui.ynbox(msg="Need to do anything more here ?",
                                title=box_title,
                                icon=icon)

# "Message" box : displays the final message with an "exit" button beneath
gui.msgbox(msg=f"Thanks for using this crap !\nProposed by:\n{author}",
           title=box_title,
           ok_button="Exit",
           icon=icon)
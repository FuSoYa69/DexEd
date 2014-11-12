# dexed.py
#
# Program Description -
#  Convert various ASCII data to other formats and layouts.
#
# Execution Example -
#  prompt>python dexed.py
#
# Supported InterpretterVersions
#  Python 3.3.2 with Tcl/Tk 8.5
#

from tkinter import *
import datetime
import re
import itertools
import os

root=Tk()
root.title(" DexEd - a (Dex)terous (Ed)itor")
root.wm_resizable(0,0)

################################################################################
# Global Variable Declaration(s)
################################################################################

convert_formats = ('%s','%.2e','%.3e','%.4e','%.5e','%.1f','%.3f','%.5f','%5i')

################################################################################
# Generic Functions
################################################################################

def print_2status(mtype,message):
    today = datetime.datetime.now()
    s = today.strftime('%b %d %Y %H:%M:%S : ')+str(message)+"\n"

    if mtype == "warning":
       textbox_status_log.insert(END, s,('warning'))
       textbox_status_log.tag_configure('warning', foreground='#DD0000',background='#DDDDDD')
    else:
       textbox_status_log.insert(END, s,)

    textbox_status_log.see(END)

def clearinput():
    textbox_input.delete(1.0,END)

def copyinput():
    root.clipboard_clear()
    root.clipboard_append(textbox_input.get(1.0,END))

def clearoutput():
    textbox_output.delete(1.0,END)

def copyoutput():
    root.clipboard_clear()
    root.clipboard_append(textbox_output.get(1.0,END))

def output2input():
    textbox_input.delete(1.0,END)
    textbox_input.insert(1.0,textbox_output.get(1.0,END))

################################################################################

###############################################################################
def y2x():
    s = textbox_input.get(1.0,END)
    s = re.sub(r"$"     , r"\n" , s)
    s = re.sub(r"\n+"   , r"\n" , s)
    s = re.sub(r"\s+"   , r" "  , s)
    s = re.sub(r"\t+"   , r" "  , s)

    s = s.strip()

    textbox_output.delete(1.0,END)
    textbox_output.insert(1.0,s)
    print_2status("notice","Converted columnar data to row data (y2x).")

###############################################################################
def x2y():
    s = textbox_input.get(1.0,END)
    s = re.sub(r"$"     , r" "  , s)
    s = re.sub(r"\n+"   , r" "  , s)
    s = re.sub(r"\s+"   , r" "  , s)
    s = re.sub(r"\t+"   , r" "  , s)
    s = re.sub(r"\s+"   , r"\n" , s)

    s = s.strip()

    textbox_output.delete(1.0,END)
    textbox_output.insert(1.0,s)
    print_2status("notice","Converted row data to columnar data (x2y).")

###############################################################################
def arr2index():
    s = textbox_input.get(1.0,END)
    s = re.sub(r"\t+"   , r" " , s)
    s = re.sub(r"\n$"   ,"",s)
    lines = s.split("\n")

    s = ""
    i,j = 0,len(lines)-1
    for line in lines:
       line = line.split()
       for word in line:
          s = s + str(i) + " " + str(j) + " " + word + "\n"
          i = i + 1
       j = j - 1
       i = 0
       s = s + "\n"

    textbox_output.delete(1.0,END)
    textbox_output.insert(1.0,s)
    print_2status("notice","Converted row data to indexed columnar data.")

###############################################################################
def reverselines():
    s = textbox_input.get(1.0,END)
    s = re.sub(r"\n$","",s)
    lines = s.split("\n")

    s = ""
    for i in range(len(lines)-1,-1,-1):
       s = s + lines[i] + "\n"

    textbox_output.delete(1.0,END)
    textbox_output.insert(1.0,s)
    print_2status("notice","Reversed line order.")

###############################################################################
def reversecols():
    s = textbox_input.get(1.0,END)
    s = re.sub(r"\n$","",s)
    lines = s.split("\n")

    s = ""
    for i in range(0,len(lines)):
       line = lines[i].split(" ")
       for j in range(len(line)-1,-1,-1):
          s = s + line[j] + " "
       s = s + "\n"

    textbox_output.delete(1.0,END)
    textbox_output.insert(1.0,s)
    print_2status("notice","Reversed column order.")

###############################################################################
## Inspired by: Jianwei Chen
## This function will transpose blocks of space- and/or tab-delimited data.
##    Furthermore, it will function on non-rectangular arrays.  Output will be
##    space-delimited by default.
def transpose():
    s = textbox_input.get(1.0,END)
    s = re.sub(r"\s+$", r""  ,s)
    s = re.sub(r"\t+" , r" " ,s)
    s = re.sub(r"^\s$", r""  ,s)
    s = re.sub(r"\s+\n", r"\n"  ,s)

    s = s.split("\n")
    for i in range(0,len(s)):
        s[i] = s[i].split(" ")

    s = list(itertools.zip_longest(*s))

    t = ""
    for i in range(0,len(s)):
        for j in range(0, len(s[i])):
            t = t + s[i][j]
            if j != len(s[i])-1:
               t = t + " "
        if i != len(s)-1:
            t = t + "\n"

    s = t

    textbox_output.delete(1.0,END)
    textbox_output.insert(1.0,s)
    print_2status("notice","Transposed data.")

###############################################################################
def convertuppercase():
    s = textbox_input.get(1.0,END)
    s = s.upper()

    textbox_output.delete(1.0,END)
    textbox_output.insert(1.0,s)
    print_2status("notice","Converted text to all uppercase.")

###############################################################################
def convertlowercase():
    s = textbox_input.get(1.0,END)
    s = s.lower()

    textbox_output.delete(1.0,END)
    textbox_output.insert(1.0,s)
    print_2status("notice","Converted text to all lowercase.")

###############################################################################
def space2tab():
    s = textbox_input.get(1.0,END)
    s = re.sub(r"( )+","\t",s)

    textbox_output.delete(1.0,END)
    textbox_output.insert(1.0,s)
    print_2status("notice","Converted spaces to tabs.")

###############################################################################
def tab2space():
    s = textbox_input.get(1.0,END)
    s = re.sub(r"\t","   ",s)

    textbox_output.delete(1.0,END)
    textbox_output.insert(1.0,s)
    print_2status("notice","Converted tabs to spaces.")

###############################################################################
def removeblanklines():
    s = textbox_input.get(1.0,END)

    s = re.sub(r"\n\s*\n",r"\n",s)

    textbox_output.delete(1.0,END)
    textbox_output.insert(1.0,s)
    print_2status("notice","Removed blank lines.")

###############################################################################
def collapsespaces():
    s = textbox_input.get(1.0,END)

    s = re.sub(r"( )+",r" ",s)

    textbox_output.delete(1.0,END)
    textbox_output.insert(1.0,s)
    print_2status("notice","Collapsed multiple spaces to a single space.")

###############################################################################
def convert():
    s = textbox_input.get(1.0,END)

    s = s.split("\n")
    textbox_output.delete(0.0,END)

    for i in s:
        row = i.split()
        for j in row:
            if(("e" in output_fmt.get()) or
               ("f" in output_fmt.get()) or
               ("i" in output_fmt.get())):
                out = output_fmt.get() % float(j) + " "
            else:
                out = output_fmt.get() % j + " "
            textbox_output.insert(END,out)
        textbox_output.insert(END,"\n")

    print_2status("notice","Converted data formats ("+output_fmt.get()+").")

###############################################################################
def row2table():
    s = textbox_input.get(1.0,END)
    s = re.sub(r"$",r"\n",s)
    s = re.sub(r"\n",r" ",s)
    s = re.sub(r"\s+",r" ",s)
    s = re.sub(r"\t+",r" ",s)
    s = re.sub(r"^\s+",r"",s)
    s = s.split()
    textbox_output.delete(0.0,END)

    for i,j in enumerate(s):
        if(("e" in output_fmt.get()) or
           ("f" in output_fmt.get()) or
           ("i" in output_fmt.get())):
            out = output_fmt.get() % float(j)
        else:
            out = output_fmt.get() % j
        textbox_output.insert(END,out)
        for k in range(int(output_colwidth.get())-len(out)):    
            textbox_output.insert(END," ")
        if((i+1) % int(output_columns.get()) == 0):
            textbox_output.insert(END,"\n")
        else:
            if(int(output_colwidth.get()) - len(out) <= 0):
                print_2status("warning","WARNING! Element Length Exceeded or Matched Column Width ( " + str(output_colwidth.get()) + " <= " + str(len(out)) + " ); Consider Increasing Column Width!")
                    
    print_2status("notice","Created table-wise data from row data with " + str(output_columns.get()) + " columns " + str(output_colwidth.get()) + " characters wide with format (" + str(format_choice.get()) + ").")

###############################################################################
def convert2FIDO():
    textbox_output.delete(1.0,END)
    textbox_output.insert(1.0,s)
    print_2status("notice","Converted data to a more-compact FIDO format.")

###############################################################################
def expandFIDO():
    textbox_output.delete(1.0,END)
    textbox_output.insert(1.0,s)
    print_2status("notice","Expaned FIDO data.")

###############################################################################
def alignLaTeXColumns():
    textbox_output.delete(1.0,END)
    textbox_output.insert(1.0,s)
    print_2status("notice","Converted row data to columnar data (x2y).")

###############################################################################
def convert2Mathematica():
    s = textbox_input.get(1.0,END)

    s = re.sub(r"(\d+\.*\d*)[eE]([+-]*)(\d+)",r"\1*10^(\2\3)",s)

    textbox_output.delete(1.0,END)
    textbox_output.insert(1.0,s)
    print_2status("notice","Converted scientific number formats to be Mathematica-compliant.")

###############################################################################
def convert2MathematicaList():
    s = textbox_input.get(1.0,END)

    s = re.sub(r"[,\s\t ]+",", ",s)
    s = re.sub(r", $","",s)
    s = "{" + s + "};"

    textbox_output.delete(1.0,END)
    textbox_output.insert(1.0,s)
    print_2status("notice","Formatted values into Mathematica list.")

###############################################################################
def countlinelength():
    s = textbox_input.get(1.0,END)

    s = s.split("\n")
    s.pop()

    num_chars = ""
    for line in s:
        num_chars = num_chars + str(len(line)) + "\n"


    s = num_chars
    textbox_output.delete(1.0,END)
    textbox_output.insert(1.0,s)
    print_2status("notice","Counted the amount of characters and whitespace on each line.")

###############################################################################
def coundcharsonline():
    s = textbox_input.get(1.0,END)

    s = s.split("\n")
    s.pop()

    num_chars = ""
    for line in s:
        line = re.sub(r" ", r"", line)
        num_chars = num_chars + str(len(line)) + "\n"

    s = num_chars
    textbox_output.delete(0.0,END)
    textbox_output.insert(END,s)
    print_2status("notice","Counted the amount of characters on each line.")

###############################################################################
def coundwordsonline():
    s = textbox_input.get(1.0,END)

    s = s.split("\n")
    s.pop()

    num_words = ""
    for line in s:
        l = line.split()
        num_words = num_words + str(len(l)) + "\n"

    s = num_words
    textbox_output.delete(0.0,END)
    textbox_output.insert(END,s)
    print_2status("notice","Counted the amount of character groupings (word separated by whitespace) on each line.")

###############################################################################
def makehistogram():
    textbox_output.delete(1.0,END)
    textbox_output.insert(1.0,s)
    print_2status("notice","Converted row data to columnar data (x2y).")

###############################################################################
# Setup frames to hold GUI elements.
###############################################################################

frame=Frame(root)
frame.pack(fill="both",expand=True)

frame_main_all  =Frame(frame)
frame_main_all.pack(side=TOP)

frame_main_top  =Frame(frame_main_all)
frame_main_top.pack(side=TOP)

frame_main_top_L=Frame(frame_main_top)
frame_main_top_L.pack(side=LEFT)
frame_main_top_L_top=Frame(frame_main_top_L)
frame_main_top_L_top.pack(side=TOP)
frame_main_top_L_top.grid_propagate(True)
frame_main_top_L_bottom=Frame(frame_main_top_L)
frame_main_top_L_bottom.pack(side=BOTTOM)
frame_main_top_L_bottom.grid_propagate(True)
frame_main_top_L_bottom.grid_rowconfigure(0,weight=1)
frame_main_top_L_bottom.grid_columnconfigure(0,weight=1)

frame_main_top_C=Frame(frame_main_top)
frame_main_top_C.pack(side=LEFT)

frame_main_top_R=Frame(frame_main_top)
frame_main_top_R.pack(side=RIGHT)
frame_main_top_R_top=Frame(frame_main_top_R)
frame_main_top_R_top.pack(side=TOP)
frame_main_top_R_top.grid_propagate(True)
frame_main_top_R_bottom=Frame(frame_main_top_R)
frame_main_top_R_bottom.pack(side=BOTTOM)
frame_main_top_R_bottom.grid_propagate(True)
frame_main_top_R_bottom.grid_rowconfigure(0,weight=1)
frame_main_top_R_bottom.grid_columnconfigure(0,weight=1)

frame_main_center1=Frame(frame_main_all)
frame_main_center1.pack(side=TOP,fill="x",expand=True)
frame_main_center1.grid_propagate(True)
frame_main_center2=Frame(frame_main_all)
frame_main_center2.pack(side=TOP,fill="x",expand=True)
frame_main_center2.grid_propagate(True)
frame_main_center3=Frame(frame_main_all)
frame_main_center3.pack(side=TOP,fill="x",expand=True)
frame_main_center3.grid_propagate(True)

frame_main_bottom=Frame(frame_main_all)
frame_main_bottom.pack(side=BOTTOM)

frame_main_bottom_label=Frame(frame_main_bottom)
frame_main_bottom_label.pack(side=TOP)

frame_main_bottom_box=Frame(frame_main_bottom)
frame_main_bottom_box.pack(fill="both",expand=True, side=BOTTOM)
frame_main_bottom_box.pack_propagate(True)

# Setup top elements (input/output boxes and corresponding buttons).

# Setup left (input) elements.

button_clear_input=Button(frame_main_top_L_top, text="Clear Input", command=clearinput).grid(row=0,column=0)
label_input=Label(frame_main_top_L_top, text="  Input  ", anchor=N, justify=CENTER).grid(row=0,column=1)
button_copy2clipboard_input=Button(frame_main_top_L_top, text="Copy Input to Clipboard", command=copyinput).grid(row=0,column=2)

textbox_input=Text(frame_main_top_L_bottom,background="white",font="courier 8",wrap="none",height=25,width=80)
textbox_input.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

textbox_input.delete(1.0,END)
#textbox_input.insert(1.0,"a b c\nd e f\ng h i\n1 2 3")
textbox_input.insert(1.0,"1 2 3 4.0e2 5.0e-3 5.66e+1")

scrollbar_Y_input=Scrollbar(frame_main_top_L_bottom, orient=VERTICAL)
scrollbar_Y_input.grid(row=0, column=1, sticky="nsew")
textbox_input['yscrollcommand']=scrollbar_Y_input.set
scrollbar_Y_input.config(command=textbox_input.yview)

scrollbar_X_input=Scrollbar(frame_main_top_L_bottom, orient=HORIZONTAL)
scrollbar_X_input.grid(row=1, column=0, sticky="nsew")
textbox_input['xscrollcommand']=scrollbar_X_input.set
scrollbar_X_input.config(command=textbox_input.xview)

# Setup output-to-input transfer button.
button_output2input=Button(frame_main_top_C, text="<---", command=output2input)
button_output2input.pack(padx=5)

# Setup right (output) elements.

button_clear_output=Button(frame_main_top_R_top, text="Clear Output", command=clearoutput).grid(row=0,column=0)
label_output=Label(frame_main_top_R_top, text="Output", anchor=N, justify=CENTER).grid(row=0,column=1)
button_copy2clipboard_output=Button(frame_main_top_R_top, text="Copy Output to Clipboard", command=copyoutput).grid(row=0,column=2)

textbox_output=Text(frame_main_top_R_bottom,background="white",font="courier 8",wrap="none",height=25,width=80)
textbox_output.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

scrollbar_Y_output=Scrollbar(frame_main_top_R_bottom, orient=VERTICAL)
scrollbar_Y_output.grid(row=0, column=1, sticky="nsew")
textbox_output['yscrollcommand']=scrollbar_Y_output.set
scrollbar_Y_output.config(command=textbox_output.yview)

scrollbar_X_output=Scrollbar(frame_main_top_R_bottom, orient=HORIZONTAL)
scrollbar_X_output.grid(row=1, column=0, sticky="nsew")
textbox_output['xscrollcommand']=scrollbar_X_output.set
scrollbar_X_output.config(command=textbox_output.xview)

# Setup "Status Log."
label_status_log=Label(frame_main_bottom_label, text="Status Log", anchor=N, justify=CENTER)
label_status_log.pack(side=TOP)

textbox_status_log=Text(frame_main_bottom_box,background="grey",font="courier 8",wrap="none",height=10,width=170)
textbox_status_log.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
#textbox_status_log.config(state=DISABLED)

scrollbar_Y_status_log=Scrollbar(frame_main_bottom_box, orient=VERTICAL)
scrollbar_Y_status_log.grid(row=0, column=1, sticky="nsew")
textbox_status_log['yscrollcommand']=scrollbar_Y_status_log.set
scrollbar_Y_status_log.config(command=textbox_status_log.yview)

scrollbar_X_status_log=Scrollbar(frame_main_bottom_box, orient=HORIZONTAL)
scrollbar_X_status_log.grid(row=1, column=0, sticky="nsew")
textbox_status_log['xscrollcommand']=scrollbar_X_status_log.set
scrollbar_X_status_log.config(command=textbox_status_log.xview)


# Setup middle buttons.

button_y2x            = Button(frame_main_center1, text='Y to X',                          command=y2x)
button_x2y            = Button(frame_main_center1, text='X to Y',                          command=x2y)
button_arr2indexed    = Button(frame_main_center1, text='Array to Indexed List',           command=arr2index)
button_reverselines   = Button(frame_main_center1, text='Reverse Lines',                   command=reverselines)
button_reversecols    = Button(frame_main_center1, text='Reverse Columns',                 command=reversecols)
button_transpose      = Button(frame_main_center1, text='Transpose Data',                  command=transpose)
button_2uppercase     = Button(frame_main_center1, text='Convert to Uppercase',            command=convertuppercase)
button_2lowercase     = Button(frame_main_center1, text='Convert to Lowercase',            command=convertlowercase)
button_space2tab      = Button(frame_main_center1, text='Spaces to Tabs',                  command=space2tab)
button_tab2space      = Button(frame_main_center1, text='Tabs to Spaces',                  command=tab2space)
button_rm_blank_lns   = Button(frame_main_center1, text='Remove Blank Lines',              command=removeblanklines)
button_min_spaces     = Button(frame_main_center1, text='Collapse Spaces to Single Space', command=collapsespaces)

button_y2x.pack(side=LEFT,fill="x",expand=True)
button_x2y.pack(side=LEFT,fill="x",expand=True)
button_arr2indexed.pack(side=LEFT,fill="x",expand=True)
button_reverselines.pack(side=LEFT,fill="x",expand=True)
button_reversecols.pack(side=LEFT,fill="x",expand=True)
button_transpose.pack(side=LEFT,fill="x",expand=True)
button_2uppercase.pack(side=LEFT,fill="x",expand=True)
button_2lowercase.pack(side=LEFT,fill="x",expand=True)
button_space2tab.pack(side=LEFT,fill="x",expand=True)
button_tab2space.pack(side=LEFT,fill="x",expand=True)
button_rm_blank_lns.pack(side=LEFT,fill="x",expand=True)
button_min_spaces.pack(side=LEFT,fill="x",expand=True)

format_choice = StringVar()
format_choice.set(convert_formats[0])
output_columns = StringVar()
output_columns.set(5)
output_colwidth = StringVar()
output_colwidth.set(14)

ddl_outputfmt         = OptionMenu(frame_main_center2,format_choice,*convert_formats)
ddl_outputfmt.config(width=5)
output_fmt            =      Entry(frame_main_center2, textvariable=format_choice, width=7, justify="center")
btn_convert           =     Button(frame_main_center2, text="Format Convert", command=convert)
label_row2tablemaxcol =      Label(frame_main_center2, text="Row to Table Maximum Columns:")
output_col_num        =      Entry(frame_main_center2, textvariable=output_columns, width=7, justify="center")
label_maxcolwidth     =      Label(frame_main_center2, text="Maximum Column Width in Characters:")
output_col_width      =      Entry(frame_main_center2, textvariable=output_colwidth, width=7, justify="center")
btn_row2table         =     Button(frame_main_center2, text="Convert Row Data to Table Data", command=row2table)
btn_LaTeXPerlAlign    =     Button(frame_main_center2, text="Align LaTeX Table Columns", bg="#FF0000")#, command=print_2status(textbox_status_log, "hi"))

ddl_outputfmt.pack(side=LEFT,fill="x",expand=True)
output_fmt.pack(side=LEFT,fill="x",expand=True,padx=3)
btn_convert.pack(side=LEFT,fill="x",expand=True)
label_row2tablemaxcol.pack(side=LEFT,fill="x",expand=True)
output_col_num.pack(side=LEFT,fill="x",expand=True,padx=3)
label_maxcolwidth.pack(side=LEFT,fill="x",expand=True)
output_col_width.pack(side=LEFT,fill="x",expand=True,padx=3)
btn_row2table.pack(side=LEFT,fill="x",expand=True)
btn_LaTeXPerlAlign.pack(side=LEFT,fill="x",expand=True)

button_convert2fido            = Button(frame_main_center3, text="Convert Data to FIDO", bg="#FF0000")#, command=output2input)
button_expandfido              = Button(frame_main_center3, text="Expand FIDO Data", bg="#FF0000")#, command=output2input)
button_convert2mathematica     = Button(frame_main_center3, text='Convert Numbers to "Mathematica" Scientific', command=convert2Mathematica)
button_convert2mathematicaList = Button(frame_main_center3, text='Convert to "Mathematica" List', command=convert2MathematicaList)
button_countlinelength         = Button(frame_main_center3, text="Count Line Length", command=countlinelength)
button_countcharsonline        = Button(frame_main_center3, text="Count Characters on Line", command=coundcharsonline)
button_countwordsonline        = Button(frame_main_center3, text="Count Words on Line", command=coundwordsonline)
button_makehistogram           = Button(frame_main_center3, text="Make Histogram", bg="#FF0000")#, command=output2input)

button_convert2fido.pack(side=LEFT,fill="x",expand=True)
button_expandfido.pack(side=LEFT,fill="x",expand=True)
button_convert2mathematica.pack(side=LEFT,fill="x",expand=True)
button_convert2mathematicaList.pack(side=LEFT,fill="x",expand=True)
button_countlinelength.pack(side=LEFT,fill="x",expand=True)
button_countcharsonline.pack(side=LEFT,fill="x",expand=True)
button_countwordsonline.pack(side=LEFT,fill="x",expand=True)
button_makehistogram.pack(side=LEFT,fill="x",expand=True)

root.mainloop()

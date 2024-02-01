import sys
import os
import ctypes
import winreg as wirg
import json
import subprocess
import threading
import dearpygui.dearpygui as dpg
import yt_dlp

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

##################################################################################################
#=============================================Winreg=============================================#
##################################################################################################

#shit for winreg
#Here goto the current user registry
#soft = wirg.ConnectRegistry(None,wirg.HKEY_CURRENT_USER)
global key
global keys
keys = []
#then we create/open our folder
soft = wirg.OpenKeyEx(wirg.HKEY_CURRENT_USER,r'SOFTWARE\\')
key = wirg.CreateKey(soft,'retardsinc\\youtubedlgui')

#then we findout howmeny values are in the folder and add the names of the values
#to the keys table

#if no values are found then we create a new value
for i in range(10):
    try:
        x=wirg.EnumValue(key,i)
        keys.append(x[0])
        #print(i)
    except:
        if i == 0 or i < 4:
            wirg.SetValueEx(key,'Default Theme',0,wirg.REG_SZ,'gold')
            wirg.SetValueEx(key,'Tooltips',0,wirg.REG_SZ,'True')
            wirg.SetValueEx(key,'dlpath',0,wirg.REG_SZ,'.\\')
            wirg.SetValueEx(key,'addmediaid',0,wirg.REG_SZ,'True')
            keys.append('Default Theme')
            keys.append('Tooltips')
            keys.append('dlpath')
            keys.append('addmediaid')
        break

##################################################################################################
#==========================================4K checker============================================#
##################################################################################################


is_4k_monitor = False #This varabial only exists because when windows scales up a program for a 4k monitor it fuckes up our custom menubar dragging system
#so the fix is to just disable menubar dragging and reenable the default windows decorator(the bar at the top of a window that has the x button in it)
#2560 1440 2k
#3840 2160 4k
#2149 1234 huh?k
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
if screensize == (2194 ,1234) or screensize == (3840,2160):
    is_4k_monitor = True

dpg.create_context()
#adding fonts
with dpg.font_registry():
    # first argument ids the path to the .ttf or .otf file
    big_font = dpg.add_font(resource_path("font/lucon.ttf"), 18)

##################################################################################################
#=====================================File handleing functions===================================#
##################################################################################################

def loadfiles():
    themepath = 'json/themes.json' if os.path.isfile('json/themes.json') else resource_path('json/themes.json')
    if os.path.isfile('./themes.json'):
        themepath = 'themes.json'
    global theme
    global theming
    theme = open(themepath)
    theming = json.load(theme)

loadfiles()

def localfilegen(sender,app_data,user_data):
    if not os.path.isfile(user_data[0]):
        with open(user_data[0],'w') as wfile:
            user_data[1].seek(0)
            wfile.write(str(user_data[1].read()))


##################################################################################################
#=====================================Theme functions/Defs=======================================#
##################################################################################################

current_theme = theming[wirg.QueryValueEx(key,keys[0])[0]]
def set_theme():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 140, 23), category=dpg.mvThemeCat_Core) #This is kinda pointless as we dont use the thing this controls
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1.5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 3, category=dpg.mvThemeCat_Core)

            dpg.add_theme_color(dpg.mvThemeCol_WindowBg,current_theme["background"])
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive,current_theme["background"])
            dpg.add_theme_color(dpg.mvThemeCol_Button,current_theme["button"])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,current_theme["buttonHover"])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,current_theme["buttonActive"])
            #stuff for menu bar
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg,current_theme["background"])
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg,current_theme["background"])
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered,current_theme["buttonHover"])
            dpg.add_theme_color(dpg.mvThemeCol_Header,current_theme["buttonActive"])
            #stuff for sliders
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab,current_theme["buttonActive"])
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive,current_theme["buttonHover"])
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg,current_theme["button"])
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered,current_theme["button"])
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive,current_theme["button"])
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding,8)
        
        with dpg.theme_component(dpg.mvCheckbox):
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark,current_theme["checkMarkColor"])
            dpg.add_theme_color(dpg.mvThemeCol_Border,current_theme["checkBoxBorder"])
        
        with dpg.theme_component(dpg.mvCheckbox,enabled_state=False):
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark,current_theme["buttonDisabledText"])
            dpg.add_theme_color(dpg.mvThemeCol_Border,current_theme['disabledBorder'])
            dpg.add_theme_color(dpg.mvThemeCol_Text,current_theme['disabledText'])
        
        with dpg.theme_component(dpg.mvRadioButton):
            dpg.add_theme_color(dpg.mvThemeCol_Border,current_theme['checkBoxBorder'])
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark,current_theme['checkMarkColor'])
        
        with dpg.theme_component(dpg.mvRadioButton,enabled_state=False):
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark,current_theme["buttonDisabledText"])
            dpg.add_theme_color(dpg.mvThemeCol_Border,current_theme['disabledBorder'])
            dpg.add_theme_color(dpg.mvThemeCol_Text,current_theme['disabledText'])
        
        with dpg.theme_component(dpg.mvInputInt,enabled_state=False):
            dpg.add_theme_color(dpg.mvThemeCol_Border,current_theme['disabledBorder'])
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow,current_theme['disabledBorder'])
            dpg.add_theme_color(dpg.mvThemeCol_Text,current_theme['disabledText'])

        with dpg.theme_component(dpg.mvButton, enabled_state=False): # Disabled Button coloring
            dpg.add_theme_color(dpg.mvThemeCol_Button,current_theme["buttonDisabled"])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,current_theme["buttonDisabled"])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,current_theme["buttonDisabled"])
            dpg.add_theme_color(dpg.mvThemeCol_Text,current_theme["buttonDisabledText"])

        with dpg.theme_component(dpg.mvTooltip):
            dpg.add_theme_color(dpg.mvThemeCol_Border,current_theme["text_color1"])
            dpg.add_theme_color(dpg.mvThemeCol_Text,current_theme["text_color1"])
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding,64)
    dpg.bind_theme(global_theme)

themetext = []

def themechanger(sender,app_data,user_data):
    global current_theme
    current_theme = theming[user_data]
    wirg.SetValueEx(key,keys[0],0,wirg.REG_SZ,user_data)
    for i in themetext:
        dpg.configure_item(i,color=current_theme['text_color1'])
    set_theme()

set_theme()

with dpg.theme() as closebtn:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign ,1.00,category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button,[0,0,0,0])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,[255,0,0,155])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,[0,0,0,0])
        dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core)

with dpg.theme() as minimizebtn:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign ,1.00,category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button,[0,0,0,0])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,[255,255,255,155])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,[0,0,0,0])
        dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core)



##################################################################################################
#====================================Misc/callback functions=====================================#
##################################################################################################

if not is_4k_monitor: #If is_4k_monitor is True then dont do any of this shit
    #all this just to drag it
    is_menu_bar_clicked = False #if you dont define the functions in this order then youd get an error when you tried to drag the window
    #but if you just define this variable first then it does not matter

    def mouse_click_callback():
        try:
            global is_menu_bar_clicked
            is_menu_bar_clicked = True if dpg.get_mouse_pos(local=False)[1] < 30 else False # 30 pixels is slightly more than the height of the default menu bar 
        except:
            pass
    def mouse_drag_callback(_, app_data): # functions for window draging
        try:
            if is_menu_bar_clicked:
                _, drag_delta_x, drag_delta_y = app_data
                viewport_pos_x, viewport_pos_y = dpg.get_viewport_pos()
                new_pos_x = viewport_pos_x + drag_delta_x
                new_pos_y = max(viewport_pos_y + drag_delta_y, 0)
                dpg.set_viewport_pos([new_pos_x, new_pos_y])
        except:
            print("fuck u")
    with dpg.handler_registry(): #function so we can drag the top of the window
        dpg.add_mouse_click_handler(button=0, callback=mouse_click_callback)
        dpg.add_mouse_drag_handler(button=0, threshold=0, callback=mouse_drag_callback)

# This function that neither of us wrote is how we keep the custom close button aligned to the corner even when the width of the window changes
#for the minimize button we just positioned it relitve to the close button
def auto_align(item, alignment_type: int, x_align: float = 0.5, y_align: float = 0.5):
    def _center_h(_s, _d, data):
        parent = dpg.get_item_parent(data[0])
        while dpg.get_item_info(parent)['type'] != "mvAppItemType::mvWindowAppItem":
            parent = dpg.get_item_parent(parent)
        parent_width = dpg.get_item_rect_size(parent)[0]
        width = dpg.get_item_rect_size(data[0])[0]
        new_x = (parent_width // 2 - width // 2) * data[1] * 2
        dpg.set_item_pos(data[0], [new_x, dpg.get_item_pos(data[0])[1]])

    def _center_v(_s, _d, data):
        parent = dpg.get_item_parent(data[0])
        while dpg.get_item_info(parent)['type'] != "mvAppItemType::mvWindowAppItem":
            parent = dpg.get_item_parent(parent)
        parent_width = dpg.get_item_rect_size(parent)[1]
        height = dpg.get_item_rect_size(data[0])[1]
        new_y = (parent_width // 2 - height // 2) * data[1] * 2
        dpg.set_item_pos(data[0], [dpg.get_item_pos(data[0])[0], new_y])

    if 0 <= alignment_type <= 2:
        with dpg.item_handler_registry():
            if alignment_type == 0:
                # horizontal only alignment
                dpg.add_item_visible_handler(callback=_center_h, user_data=[item, x_align])
            elif alignment_type == 1:
                # vertical only alignment
                dpg.add_item_visible_handler(callback=_center_v, user_data=[item, y_align])
            elif alignment_type == 2:
                # both horizontal and vertical alignment
                dpg.add_item_visible_handler(callback=_center_h, user_data=[item, x_align])
                dpg.add_item_visible_handler(callback=_center_v, user_data=[item, y_align])

        dpg.bind_item_handler_registry(item, dpg.last_container())

tips = []
def toggletooltips():
    var = dpg.get_value('enabletipcb')
    wirg.SetValueEx(key,keys[1],0,wirg.REG_SZ,str(var))
    for i in tips:
        dpg.configure_item(i,show=var)

global lastline

def print_console(inp,console_window='conwin',color=[255,255,255]):
    global lastline
    if lastline and '[download]' in dpg.get_value(lastline) and '[download]' in inp and not '[download] Destination:' in dpg.get_value(lastline) and not '[download] Destination:' in inp:
        dpg.set_value(lastline,inp)
        dpg.configure_item(lastline,color=current_theme['text_color1'])
    else:
        lastline = dpg.add_text(inp, parent=console_window,wrap=dpg.get_item_width(console_window))
        dpg.configure_item(lastline,color=color)
        dpg.set_y_scroll(console_window, dpg.get_y_scroll_max(console_window)+1000)

def modetog(sender):
    if dpg.get_value(sender) == 'Full video':
        dpg.configure_item('thumbnail',enabled=False)
        dpg.set_value('format','mp4')
    elif dpg.get_value(sender) == 'Audio only':
        dpg.configure_item('thumbnail',enabled=True)
        dpg.set_value('format','mp3')
    elif dpg.get_value(sender) == 'Video only':
        dpg.configure_item('thumbnail',enabled=False)
        dpg.set_value('format','mp4')

def download():
    dpg.configure_item('dlbutton',enabled=False) #disable download button while download is in progress

    dl_options=[ #redefine options list for new download and grab user settings like rate limit
        f' --ffmpeg-location "{resource_path("exe/")}" ',
        f'-r {dpg.get_value("ratelimit")}m ',
        f'-o "{dpg.get_value("dllocation")}%(title)s{" [%(id)s]" if dpg.get_value("addmediaid") else ""}.%(ext)s" ',
        '--windows-filenames ',
        '--restrict-filenames '
    ]


    if dpg.get_value('isplaylist') == True: #set start/endpoint for playlist if defined by user
        if dpg.get_value('plpoint2') == 0:
            dl_options.append(f'--playlist-items {dpg.get_value("plpoint1")}: ')
        else:
            dl_options.append(f'--playlist-items {dpg.get_value("plpoint1")}:{dpg.get_value("plpoint2")} ')

    if not dpg.get_value('cookies') == '': #add cookies file if provided
        dl_options.append(f'--cookies "{dpg.get_value("cookies")}" ')

    if dpg.get_value('modesel') == 'Full video': #download video+audio
        dl_options.append(f'-f bestvideo+bestaudio --merge-output-format {dpg.get_value("format")} ')

    elif dpg.get_value('modesel') == 'Audio only': #only download audio file
        dl_options.append(f'-x --audio-format {dpg.get_value("format")} ')

        if dpg.get_value('thumbnail') == True:
            dl_options.append('--embed-thumbnail ')
    
    elif dpg.get_value('modesel') == 'Video only': #only download video file
        dl_options.append(f'-f bestvideo/best --remux-video {dpg.get_value("format")} ')
    dl_options.append(dpg.get_value('url'))
    with subprocess.Popen(resource_path('exe\\yt-dlp.exe')+''.join(dl_options),stdout=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=1,universal_newlines=True,creationflags=subprocess.CREATE_NO_WINDOW) as process:
        for line in process.stdout:
            if len(line) > 1:
                print_console(line)
        for line in process.stderr:
            if len(line) > 1:
                if 'Requested format is not available.' in line:
                    print_console('[Error] is looks like this website might not seperate its audio from its video try switching to "Video only" mode.',color=[255,0,0])
                else:
                    print_console(line,color=[255,0,0])
    dpg.configure_item('dlbutton',enabled=True)#reenable download button
    print_console('All operations complete.',color=[0,255,0])

def pltog(sender):
    if dpg.get_value(sender) == True:
        dpg.configure_item('plpoint1',enabled=True)
        dpg.configure_item('plpoint2',enabled=True)
    else:
        dpg.configure_item('plpoint1',enabled=False)
        dpg.configure_item('plpoint2',enabled=False)

def pathfixer(sender):
    var = dpg.get_value(sender)
    if var[-1] != '/' or var[-1] != '\\':
        dpg.set_value(sender,var+'\\')
        wirg.SetValueEx(key,keys[2],0,wirg.REG_SZ,var+'\\')
    else:
        wirg.SetValueEx(key,keys[2],0,wirg.REG_SZ,var)

def wavEMBEDblock(sender):
    if dpg.get_value(sender) == 'wav' and dpg.get_value('modesel') == 'Audio only':
        dpg.configure_item('thumbnail',enabled=False)
        dpg.set_value('thumbnail',False)
    elif dpg.get_value('modesel') == 'Audio only':
        dpg.configure_item('thumbnail',enabled=True)

def fib_confirm(_,app_data):
    var = app_data['current_path']
    if not len(var) > 1:
        var = '.\\'
    elif var[-1] != '\\' or var[-1] != '/':
        var+='\\'
    dpg.set_value('dllocation',var)
    wirg.SetValueEx(key,keys[2],0,wirg.REG_SZ,var)

def fib_cancel():
    pass

def fib_confirm2(_,app_data):
    dpg.set_value('cookies',app_data['file_path_name'])

##################################################################################################
#===========================================Main window==========================================#
##################################################################################################

with dpg.window(tag="primary",width=700, height=600,no_move=True,no_resize=False,no_title_bar=True,pos=[0,0],max_size=[3000,3000]):
    #download directory selector
    dpg.add_file_dialog(directory_selector=True,show=False,callback=fib_confirm,tag='file_browser',cancel_callback=fib_cancel,width=600,height=500,modal=True,default_path=wirg.QueryValueEx(key,keys[2])[0])
    #cookies file selector
    with dpg.file_dialog(directory_selector=False,show=False,callback=fib_confirm2,tag='file_browser2',cancel_callback=fib_cancel,width=600,height=500,modal=True):
        dpg.add_file_extension('.txt')
    
    mtext = dpg.add_text("Youtube-dl GUI",color=current_theme['text_color1'])
    lastline = mtext#This is only here so print_console dosent error on its first run
    dpg.bind_item_font(mtext,big_font)
    themetext.append(mtext)

    dpg.add_radio_button(['Full video','Video only','Audio only'],tag='modesel',callback=modetog,default_value='Full video')

    dpg.add_input_int(label='Rate limit in MB',tag='ratelimit',default_value=35,width=100)
    dpg.add_input_text(label='Output format',tag='format',default_value='mp4',width=50,callback=wavEMBEDblock)
    dpg.add_input_text(label='Url/videoID',tag='url',default_value='dQw4w9WgXcQ')
    with dpg.group(horizontal=True):
        dpg.add_input_text(default_value=wirg.QueryValueEx(key,keys[2])[0],tag='dllocation',callback=pathfixer,width=402)
        dpg.add_button(label='...',callback=lambda: dpg.show_item('file_browser'),width=40,tag='file_button')
        dpg.add_text('Download location')

    with dpg.tooltip('dllocation') as dllocationtip:
        tips.append(dllocationtip)
        dpg.add_text('This is where the downloaded videos will be placed.\nDefault: ".\\" this means that they will be placed\nnext to the exe.')
    
    with dpg.tooltip('file_button') as file_buttontip:
        tips.append(file_buttontip)
        dpg.add_text('File browser')

    with dpg.group(horizontal=True):
        dpg.add_input_text(tag='cookies',width=250)
        dpg.add_button(label='...',callback=lambda: dpg.show_item('file_browser2'),width=40,tag='file_button2')
        dpg.add_text('Cookies.txt file location *optional*')

    with dpg.tooltip('cookies') as cookiestip:
        tips.append(cookiestip)
        dpg.add_text('You only need this if youtube says you need to be loged in\nInorder to access the video otherwise you will be fine')
    
    with dpg.tooltip('file_button2') as file_buttontip2:
        tips.append(file_buttontip2)
        dpg.add_text('File browser')

    dpg.add_checkbox(label='Embed thumbnail',tag='thumbnail',enabled=False)
    with dpg.tooltip('thumbnail') as thumbnailtip:
        tips.append(thumbnailtip)
        dpg.add_text('Audio only when enabled the thumbnail will be downloaded\nand the icon of the audio file will be set to that.\nNote this can occasionally hang for a few seconds at the end.')
    
    dpg.add_checkbox(label='Playlist?',tag='isplaylist',callback=pltog)
    with dpg.tooltip('isplaylist') as playlisttip:
        tips.append(playlisttip)
        dpg.add_text('You only need to enable this if you want to\ndefine a custom start/stop for your playlist\nother wise it will just go from 1 to end')
    dpg.add_input_int(label='Starting point for the playlist',min_value=1,default_value=1,tag='plpoint1',enabled=False,width=100)
    dpg.add_input_int(label='Ending point for the playlist',min_value=0,default_value=0,tag='plpoint2',enabled=False,width=100)
    with dpg.tooltip('plpoint2') as plpoint2tip:
        tips.append(plpoint2tip)
        dpg.add_text('leave at 0 if you want to download all videos\nFrom the starting point untill the end')
    
    dpg.add_separator()
    with dpg.group(horizontal=True):
        dpg.add_button(label='Download',tag='dlbutton',callback=lambda: threading.Thread(target=download).start())
        dpg.add_checkbox(label='Add media id to filename?',tag='addmediaid',default_value=True if wirg.QueryValueEx(key,keys[3])[0] == 'True' else False,callback=lambda s,a:wirg.SetValueEx(key,keys[3],0,wirg.REG_SZ,str(a)))
        with dpg.tooltip('addmediaid') as mediaidtip:
            tips.append(mediaidtip)
            dpg.add_text('normally the output would look like (mediatitle [mediaID].mp4)\nBut this can sometimes cause problems with the video only mode\nIf an error is thrown saying so such file or directory try turning this off.')
    dpg.add_separator()
    dpg.add_text('Console',tag='consoleheader')
    dpg.bind_item_font('consoleheader',big_font)
    with dpg.child_window(label='Console',tag='conwin',autosize_x=True,autosize_y=True):
        pass
    
    

    with dpg.menu_bar():
        with dpg.menu(label="Theme"):#Grab the names of all the themes if themes.json and add them to the options
            for i in theming:
                if not i == 'default':
                    dpg.add_menu_item(label=f"{i}", callback=themechanger,user_data=f"{i}")
        
        with dpg.menu(label='extra'):
            o1 = dpg.add_menu_item(label="create themes.json file",callback=localfilegen,user_data=['./themes.json',theme])
            with dpg.tooltip(o1) as themetip:
                tips.append(themetip)
                dpg.add_text('Generate a jsonfile next to the exe for user modification\nThis json file will be used on startup\nInsted of the default file')

            dpg.add_checkbox(label="Enable tooltips",default_value=True if wirg.QueryValueEx(key,keys[1])[0] == 'True' else False,tag='enabletipcb',callback=toggletooltips)
        if is_4k_monitor == False:
            dpg.add_button(label='X',tag='closebtn',callback=lambda: os._exit(0))
            dpg.add_button(label='-',tag='minbtn',callback=lambda: dpg.minimize_viewport())
            dpg.bind_item_font('minbtn',big_font)
            dpg.bind_item_theme('closebtn',closebtn)
            dpg.bind_item_theme('minbtn',minimizebtn)
            auto_align('closebtn', 0, x_align=1, y_align=0.1)
            #auto_align(item tag,int alignment mode 0 1 or 2, x_align=0 to 1, y_align=0 to 1)

#funfact 
#lets say you do test=5
#but you want it to = 10 while test2 = True
#you can just do test = 5 if test2 == False else 10
dpg.create_viewport(title='Youtube-dlp gui', decorated=False if not is_4k_monitor else True,large_icon=resource_path('icon/icon.ico'))
if is_4k_monitor == True:
    dpg.set_primary_window("primary", True)
dpg.setup_dearpygui()
dpg.show_viewport()
toggletooltips() #this is easier than making every tooltip do its own check for weather it should be on

while dpg.is_dearpygui_running():
    if is_4k_monitor == False:
        #if the window is resized so that the close button is not visible it wont get moved so here we check if that happened and if so move
        #both the close and minimize buttons back into visible space
        cx, _ = dpg.get_item_pos('closebtn')
        if cx > dpg.get_viewport_width():
            dpg.set_item_pos('closebtn',[0,0])
            dpg.set_item_pos('minbtn',[0,0])
        dpg.set_item_pos('minbtn',[cx-26,0])
        w,h = dpg.get_item_width('primary'),dpg.get_item_height('primary')
        dpg.set_viewport_width(w)
        dpg.set_viewport_height(h)
        dpg.set_item_pos('primary',[0,0])
    dpg.render_dearpygui_frame()
dpg.destroy_context()

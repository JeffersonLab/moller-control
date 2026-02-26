import os, sys
import phoebusgen.screen
import phoebusgen.widget as widget

def make_button_seg_ON(index, x, y, pv_list):
    # Create segment ON button

    name = "Action_Button_ON_" + str(index)
    width = 20
    height = 20

    action_button = widget.ActionButton(name, "ON", None, x, y, width, height)

    def make_js_script(pv_list):
        js_code = """
importClass(org.csstudio.display.builder.runtime.script.PVUtil);
importClass(org.csstudio.display.builder.runtime.script.ScriptUtil);
logger = ScriptUtil.getLogger();
logger.info("Turn ON Seg");
        """
        for pv_name in pv_list:
            # pv_name, value, timeout
            pv = '"%s:Pw"' % pv_name
            cmd_str = "PVUtil.writePV(%s, 1, 1000)" % pv
            js_code = js_code + "\n" + cmd_str

        return js_code

    # embedded script
    js_code = make_js_script(pv_list)
    action_button.action_execute_javascript_script(js_code, "Execute Script")

    # set font
    action_button.font_family("Liberation Sans")
    action_button.font_size(9.0)
    
    return action_button

def make_button_seg_OFF(index, x, y, pv_list):
    # Create segment ON button

    name = "Action_Button_OFF_" + str(index)
    width = 20
    height = 20

    action_button = widget.ActionButton(name, "OFF", None, x, y, width, height)

    def make_js_script(pv_list):
        js_code = """
importClass(org.csstudio.display.builder.runtime.script.PVUtil);
importClass(org.csstudio.display.builder.runtime.script.ScriptUtil);
logger = ScriptUtil.getLogger();
logger.info("Turn OFF Seg");
        """
        for pv_name in pv_list:
            # pv_name, value, timeout
            pv = '"%s:Pw"' % pv_name
            cmd_str = "PVUtil.writePV(%s, 0, 1000)" % pv
            js_code = js_code + "\n" + cmd_str

        return js_code

    # embedded script
    js_code = make_js_script(pv_list)
    action_button.action_execute_javascript_script(js_code, "Execute Script")

    # set font
    action_button.font_family("Liberation Sans")
    action_button.font_size(9.0)
    
    return action_button

def make_LED(index, pv_name, x, y):
    name = "LED_" + str(index)
    width = 20
    height = 20

    led = widget.LEDMultiState(name, pv_name, x, y, 20, 20)

    # Red
    led._add_state(0, None, phoebusgen.colors.STOP, None, None, None, None)
    # Green
    led._add_state(80, None , phoebusgen.colors.On, None, None, None, None)

    # Set properties
    led.square(True)
    led.fallback_label(None)
    led.alarm_border(False)

    return led

def make_button_ch(index, pv_name, x, y):
    name = "Action_Button_Ch_" + str(index)
    width = 20
    height = 20

    # name, text, pv_name, x, y, width, height
    action_button = widget.ActionButton(name, None, pv_name, x, y, width, height)
    action_button.action_write_pv("$(pv_name)", 1, "PW-ON")
    action_button.action_write_pv("$(pv_name)", 0, "PW-OFF")
    action_button.transparent(True)

    return action_button

def add_info_labels(screen):
    rec_on = widget.Rectangle("Rectangle_on", 950, 100, 20, 20)
    rec_on.background_color(0, 255, 0) # green
    rec_on.line_color(255,255,255,0)
    rec_on.line_width(0)

    rec_off = widget.Rectangle("Rectangle_off", 950, 140, 20, 20)
    rec_off.background_color(255, 0, 0) # red
    rec_off.line_color(255,255,255,0)
    rec_off.line_width(0)

    lab_on = widget.Label("lab_on", "Power ON", 983, 94, 77, 30)
    lab_on.vertical_alignment_middle()

    lab_off = widget.Label("lab_off", "Power OFF", 983, 135, 77, 30)
    lab_off.vertical_alignment_middle()

    lab_seg = widget.Label("lab_seg", "Segment:", 950, 64, 130, 30)
    lab_seg.vertical_alignment_middle()    

    lab_FF = widget.Label("lab_FF", "FF", 1020, 64, 20, 30)
    lab_FF.font_size(14)
    lab_FF.foreground_color(0,0,255) # blue
    lab_FF.font_style_bold()
    lab_FF.vertical_alignment_middle()

    lab_BF = widget.Label("lab_BF", "/ BF", 1041, 64, 43, 30)
    lab_BF.font_size(14)
    lab_BF.font_style_bold()
    lab_BF.vertical_alignment_middle()

    screen.add_widget(rec_on)
    screen.add_widget(rec_off)
    screen.add_widget(lab_on)
    screen.add_widget(lab_off)
    screen.add_widget(lab_seg)
    screen.add_widget(lab_FF)
    screen.add_widget(lab_BF)

def add_open_table(name, x, y, width, height):
    action_button = widget.ActionButton(name, None, None, x, y, width, height)
    action_button.action_open_display("MD-Table.bob", "window")
    action_button.transparent(True)
    return action_button

# Read LV map and make a pv list
def read_map(infile):
    # Ring : PMT_number
    pmt = {"1":0, "2":1, "3":2, "4":3, "5C":4, "5L":5, "5R":6, "6":7}
    d_pv = {}
    with open(infile, 'r') as f:
        lines = [x.strip() for x in f.readlines()]
        for line in lines:
            if "#" in line:
                continue
            else:
                crate = int(line.split()[0])
                slot = int(line.split()[1])
                ch = int(line.split()[2])
                seg = int(line.split()[3])
                ring = line.split()[4]
                pv_name = "MollerPS%02d:%02d:%03d" % (crate, slot, ch)
                d_pv[(seg, pmt[ring])] = pv_name
    return d_pv

def get_ch_name(d_pv, iseg, ipmt):
    ch_name = d_pv[(iseg, ipmt)]
    return ch_name

def get_seg_pvlist(d_pv, iseg):
    pv_list = []
    for i in range(8):
        pv_list.append(d_pv[(iseg, i)])
    return pv_list

#----------------------------------
#   Main detector display
#----------------------------------
my_screen = phoebusgen.screen.Screen("Main Detector Overview")

# Title label
label_0 = widget.Label("Label_0", "Main Detector Overview", 70, 10, 220, 40)
label_0.background_color(128,128,128)
label_0.transparent(False)
label_0.horizontal_alignment_center()
label_0.vertical_alignment_middle()
label_0.font_style_bold()
label_0.font_size(14)
my_screen.add_widget(label_0)

# Open table view of the channels
button_table = add_open_table("Action_Button_Table", 70, 10, 220, 40)
my_screen.add_widget(button_table)

# ALL ON/OFF
label_100 = widget.Label("Label_100", "Turn ALL ON/OFF", 345, 27, 140, 30)
label_100.font_size(14)
label_100.font_style_bold()
my_screen.add_widget(label_100)

button_on = widget.ActionButton("Action_Button_ALLON", "ON", None, 485, 21, 50, 30)
my_screen.add_widget(button_on)
button_off = widget.ActionButton("Action_Button_ALLOFF", "OFF", None, 550, 21, 50, 30)
my_screen.add_widget(button_off)

# Add Ring labels
label_1 = widget.Label("Label_1", "Ring 1", 10, 95, 70, 30)
label_1.vertical_alignment_middle()
label_1.font_style_bold()
my_screen.add_widget(label_1)

label_2 = widget.Label("Label_2", "Ring 2", 10, 135, 70, 30)
label_2.vertical_alignment_middle()
label_2.font_style_bold()
my_screen.add_widget(label_2)

label_3 = widget.Label("Label_3", "Ring 3", 10, 175, 70, 30)
label_3.vertical_alignment_middle()
label_3.font_style_bold()
my_screen.add_widget(label_3)

label_4 = widget.Label("Label_4", "Ring 4", 10, 215, 70, 30)
label_4.vertical_alignment_middle()
label_4.font_style_bold()
my_screen.add_widget(label_4)

label_5C = widget.Label("Label_5C", "Ring 5C", 10, 255, 70, 30)
label_5C.vertical_alignment_middle()
label_5C.font_style_bold()
my_screen.add_widget(label_5C)

label_5L = widget.Label("Label_5L", "Ring 5L", 10, 295, 70, 30)
label_5L.vertical_alignment_middle()
label_5L.font_style_bold()
my_screen.add_widget(label_5L)

label_5R = widget.Label("Label_5R", "Ring 5R", 10, 335, 70, 30)
label_5R.vertical_alignment_middle()
label_5R.font_style_bold()
my_screen.add_widget(label_5R)

label_6 = widget.Label("Label_6", "Ring 6", 10, 375, 70, 30)
label_6.vertical_alignment_middle()
label_6.font_style_bold()
my_screen.add_widget(label_6)

# Add Seg labels
for seg in range(28):
    name = "Label_seg" + str(seg)
    x = 70 + seg*30
    y = 70
    label = widget.Label(name, str(seg), x, y, 20, 20)
    label.font_style_bold()
    label.horizontal_alignment_center()
    label.vertical_alignment_middle()

    # Set color for FF/BF
    # For now, we assume FF is even segment 
    if seg%2 == 0:
        label.foreground_color(0, 0, 255) # blue
    my_screen.add_widget(label)

# Read map and make a pv data
d_pv = read_map(sys.argv[1])

# Channel display
index = 0
for seg in range(28):
    for ipmt in range(8):
        x = 70 + seg*30
        y = 100 + ipmt*40

        # FIXME: put randmon pv for not yet connected seg
        if seg < 4:
            pv_name = get_ch_name(d_pv, seg,ipmt) + ":Status"
        else:
            pv_name = get_ch_name(d_pv, 1,ipmt) + ":Status"

        led = make_LED(index, pv_name, x, y)
        my_screen.add_widget(led)

        index = index+1

# Channel action button
index = 0
for seg in range(28):
    # FIXME: remove it once we have all channels
    if seg > 3:
        continue

    for ipmt in range(8):
        x = 70 + seg*30
        y = 100 + ipmt*40
        pv_name = get_ch_name(d_pv, seg,ipmt) + ":Pw"
        button = make_button_ch(index, pv_name, x, y)
        my_screen.add_widget(button)

        index = index+1

# Create segment ON/OFF buttons
for i in range(0, 28):

    x1 = 70 + 30*i
    y1 = 420

    x2 = 70 + 30*i
    y2 = 450

    # FIXME: put randmon pv for not yet connected seg
    if i < 4:
        pv_list = get_seg_pvlist(d_pv, i)
    else:
        pv_list = get_seg_pvlist(d_pv, 1)

    button1 = make_button_seg_ON(i, x1, y1, pv_list)
    button2 = make_button_seg_OFF(i,x2, y2, pv_list)

    my_screen.add_widget(button1)
    my_screen.add_widget(button2)

# Add information labels
add_info_labels(my_screen)

# Save to .bob file
#print(my_screen)
with open("MD_overview.bob", "w") as f:
    f.write(str(my_screen))



    

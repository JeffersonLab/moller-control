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
            cmd_str = "PVUtil.writePV(%s, 1, 1000)" % pv_name
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

    name = "Action_Button_ON_" + str(index)
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
            cmd_str = "PVUtil.writePV(%s, 0, 1000)" % pv_name
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

# Main detector display
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
label_1 = widget.Label("Label_1", "Ring 1", 10, 85, 70, 30)
label_1.vertical_alignment_middle()
label_1.font_style_bold()
my_screen.add_widget(label_1)

label_2 = widget.Label("Label_2", "Ring 2", 10, 125, 70, 30)
label_2.vertical_alignment_middle()
label_2.font_style_bold()
my_screen.add_widget(label_2)

label_3 = widget.Label("Label_3", "Ring 3", 10, 165, 70, 30)
label_3.vertical_alignment_middle()
label_3.font_style_bold()
my_screen.add_widget(label_3)

label_4 = widget.Label("Label_4", "Ring 4", 10, 205, 70, 30)
label_4.vertical_alignment_middle()
label_4.font_style_bold()
my_screen.add_widget(label_4)

label_5 = widget.Label("Label_5", "Ring 5", 10, 285, 70, 30)
label_5.vertical_alignment_middle()
label_5.font_style_bold()
my_screen.add_widget(label_5)

label_6 = widget.Label("Label_6", "Ring 6", 10, 365, 70, 30)
label_6.vertical_alignment_middle()
label_6.font_style_bold()
my_screen.add_widget(label_6)

# Add Seg labels
for seg in range(28):
    name = "Label_seg" + str(seg)
    x = 70 + seg*30
    y = 60
    label = widget.Label(name, str(seg), x, y, 20, 20)
    label.font_style_bold()
    label.horizontal_alignment_center()
    label.vertical_alignment_middle()
    my_screen.add_widget(label)

# Read pv list (FIXME: this should be done from input file later)
# (seg, ring, pmt)
d_pv = {(0, 0): "MollerPS13:08:000",
        (0, 1): "MollerPS13:08:001",
        (0, 2): "MollerPS13:08:002",
        (0, 3): "MollerPS13:08:003",
        (0, 4): "MollerPS13:08:004",
        (0, 5): "MollerPS13:08:005",
        (0, 6): "MollerPS13:08:006",
        (0, 7): "MollerPS13:08:007",
        (1, 0): "MollerPS13:09:000",
        (1, 1): "MollerPS13:09:001",
        (1, 2): "MollerPS13:09:002",
        (1, 3): "MollerPS13:09:003",
        (1, 4): "MollerPS13:09:004",
        (1, 5): "MollerPS13:09:005",
        (1, 6): "MollerPS13:09:006",
        (1, 7): "MollerPS13:09:007",
        }

def get_ch_name(iseg, ipmt):
    ch_name = d_pv[(iseg, ipmt)]
    return ch_name

def get_seg_pvlist(iseg):
    pv_list = []
    for i in range(8):
        pv_list.append(d_pv[(iseg, i)])
    return pv_list

# Channel display
index = 0
for seg in range(28):
    for ipmt in range(8):
        x = 70 + seg*30
        y = 90 + ipmt*40

        # FIXME: put randmon pv for not yet connected seg
        if seg < 2:
            pv_name = get_ch_name(seg,ipmt) + ":Status"
        else:
            pv_name = get_ch_name(1,ipmt) + ":Status"

        led = make_LED(index, pv_name, x, y)
        my_screen.add_widget(led)

        index = index+1

# Channel action button
index = 0
for seg in range(2):
    for ipmt in range(8):
        x = 70 + seg*30
        y = 90 + ipmt*40
        pv_name = get_ch_name(seg,ipmt) + ":Pw"
        button = make_button_ch(index, pv_name, x, y)
        my_screen.add_widget(button)

        index = index+1

# Create segment ON/OFF buttons
for i in range(0, 28):

    x1 = 70 + 30*i
    y1 = 410

    x2 = 70 + 30*i
    y2 = 440

    # FIXME: put randmon pv for not yet connected seg
    if i < 2:
        pv_list = get_seg_pvlist(i)
    else:
        pv_list = get_seg_pvlist(1)

    button1 = make_button_seg_ON(i, x1, y1, pv_list)
    button2 = make_button_seg_OFF(i,x2, y2, pv_list)

    my_screen.add_widget(button1)
    my_screen.add_widget(button2)

# Save to .bob file

print(my_screen)

with open("MD_overview.bob", "w") as f:
    f.write(str(my_screen))



    

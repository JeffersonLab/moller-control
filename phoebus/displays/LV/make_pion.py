import phoebusgen.screen
import phoebusgen.widget as widget
import argparse

# argument  parser
argparser = argparse.ArgumentParser(description="Create Pion Detector LV screen")
argparser.add_argument("--expert", help="Expert mode screen", action="store_true")
args = argparser.parse_args()

my_screen = phoebusgen.screen.Screen("Pion Detector LV Overview")

# Title
title_label = widget.Label("Label_title", "Pion Detector LV Controls and Monitoring", 20, 10, 450, 40)
title_label.background_color(255,255,0)
title_label.transparent(False)
title_label.horizontal_alignment_center()
title_label.vertical_alignment_middle()
title_label.predefined_font(phoebusgen.fonts.Header1)
my_screen.add_widget(title_label)

# Add All ON/OFF buttons
on_button = widget.ActionButton("Action_Button_ON", "ALL ON", None, 40, 80, 90, 40)
off_button = widget.ActionButton("Action_Button_OFF", "ALL OFF", None, 150, 80, 90, 40)

pw_rectangle = widget.Rectangle("Rectangle_pw", 20, 70, 240, 60)
pw_rectangle.line_color(0,0,0)
pw_rectangle.line_width(2)
pw_rectangle.background_color(240, 240, 240)

my_screen.add_widget(pw_rectangle)
my_screen.add_widget(on_button)
my_screen.add_widget(off_button)

# Expert/Shift mode button
mode_button_1 = widget.ActionButton("Action_Button_mode_1", "Shift Mode", None, 500, 80, 150, 40)
mode_button_1.action_open_display("Pion_Expert.bob", "replace")
mode_button_1.font_size(16)
mode_button_1.alarm_border(False)
mode_button_1.confirmation_dialog("Are your sure you want to do this?")

mode_rectangle_1 = widget.Rectangle("Rectangle_mode",500, 80, 150, 40)
mode_rectangle_1.line_color(0,255,0) # green
mode_rectangle_1.transparent(True)

mode_button_2 = widget.ActionButton("Action_Button_mode_2", "Expert Mode", None, 500, 80, 150, 40)
mode_button_2.action_open_display("Pion.bob", "replace")
mode_button_2.font_size(16)
mode_button_2.alarm_border(False)
mode_button_2.background_color(255,255,0) # yellow
mode_button_2.transparent(False)

mode_rectangle_2 = widget.Rectangle("Rectangle_mode",500, 80, 150, 40)
mode_rectangle_2.line_color(255,0,0) # red
mode_rectangle_2.transparent(True)

# Add LV table
table_display_1 = widget.EmbeddedDisplay("LV table display", "Pion-Table.bob", 20, 140, 680, 880)
table_display_2 = widget.EmbeddedDisplay("LV table display", "Pion-Table_Expert.bob", 20, 140, 680, 880)

if args.expert:
    my_screen.add_widget(mode_button_2)
    my_screen.add_widget(mode_rectangle_2)
    my_screen.add_widget(table_display_2)
    ofname = "Pion_Expert.bob"
else:
    my_screen.add_widget(mode_button_1)
    my_screen.add_widget(mode_rectangle_1)
    my_screen.add_widget(table_display_2)
    ofname = "Pion.bob"

with open(ofname, "w") as f:
    f.write(str(my_screen))

    

import os
import sys

Skeleton_Format=\
'<?xml version="1.0" encoding="UTF-8"?>\n\
<display version="2.0.0">\n\
  <name>Display</name>\n\
  <widget type="label" version="2.0.0">\n\
    <name>Label_238</name>\n\
    <text>Difference</text>\n\
    <x>314</x>\n\
    <y>42</y>\n\
    <width>69</width>\n\
    <height>16</height>\n\
    <font>\n\
      <font name="Default Bold" family="Liberation Sans" style="BOLD" size="14.0">\n\
      </font>\n\
    </font>\n\
    <horizontal_alignment>1</horizontal_alignment>\n\
    <auto_size>true</auto_size>\n\
    <wrap_words>false</wrap_words>\n\
  </widget>\n\
  <widget type="label" version="2.0.0">\n\
    <name>Label_239</name>\n\
    <text>Voltage</text>\n\
    <x>245</x>\n\
    <y>20</y>\n\
    <width>51</width>\n\
    <height>16</height>\n\
    <font>\n\
      <font name="Default Bold" family="Liberation Sans" style="BOLD" size="14.0">\n\
      </font>\n\
    </font>\n\
    <horizontal_alignment>1</horizontal_alignment>\n\
    <auto_size>true</auto_size>\n\
    <wrap_words>false</wrap_words>\n\
  </widget>\n\
  <widget type="label" version="2.0.0">\n\
    <name>Label_240</name>\n\
    <text>Current</text>\n\
    <x>498</x>\n\
    <y>20</y>\n\
    <width>51</width>\n\
    <height>16</height>\n\
    <font>\n\
      <font name="Default Bold" family="Liberation Sans" style="BOLD" size="14.0">\n\
      </font>\n\
    </font>\n\
    <horizontal_alignment>1</horizontal_alignment>\n\
    <auto_size>true</auto_size>\n\
    <wrap_words>false</wrap_words>\n\
  </widget>\n\
  <widget type="polyline" version="2.0.0">\n\
    <name>Polyline</name>\n\
    <x>166</x>\n\
    <y>40</y>\n\
    <width>220</width>\n\
    <height>1</height>\n\
    <points>\n\
      <point x="0.0" y="0.0">\n\
      </point>\n\
      <point x="220.3826320482337" y="0.0">\n\
      </point>\n\
    </points>\n\
    <line_width>1</line_width>\n\
    <line_color>\n\
      <color name="Text" red="0" green="0" blue="0">\n\
      </color>\n\
    </line_color>\n\
  </widget>\n\
  <widget type="label" version="2.0.0">\n\
    <name>Label_241</name>\n\
    <text>Difference</text>\n\
    <x>560</x>\n\
    <y>42</y>\n\
    <width>69</width>\n\
    <height>16</height>\n\
    <font>\n\
      <font name="Default Bold" family="Liberation Sans" style="BOLD" size="14.0">\n\
      </font>\n\
    </font>\n\
    <horizontal_alignment>1</horizontal_alignment>\n\
    <auto_size>true</auto_size>\n\
    <wrap_words>false</wrap_words>\n\
  </widget>\n\
  <widget type="polyline" version="2.0.0">\n\
    <name>Polyline_1</name>\n\
    <x>412</x>\n\
    <y>40</y>\n\
    <width>220</width>\n\
    <height>1</height>\n\
    <points>\n\
      <point x="0.0" y="0.0">\n\
      </point>\n\
      <point x="220.3826320482337" y="0.0">\n\
      </point>\n\
    </points>\n\
    <line_width>1</line_width>\n\
    <line_color>\n\
      <color name="Text" red="0" green="0" blue="0">\n\
      </color>\n\
    </line_color>\n\
  </widget>\n\
  <widget type="label" version="2.0.0">\n\
    <name>Label_242</name>\n\
    <text>Readback</text>\n\
    <x>481</x>\n\
    <y>42</y>\n\
    <width>67</width>\n\
    <height>16</height>\n\
    <font>\n\
      <font name="Default Bold" family="Liberation Sans" style="BOLD" size="14.0">\n\
      </font>\n\
    </font>\n\
    <horizontal_alignment>1</horizontal_alignment>\n\
    <auto_size>true</auto_size>\n\
    <wrap_words>false</wrap_words>\n\
  </widget>\n\
  <widget type="label" version="2.0.0">\n\
    <name>Label_243</name>\n\
    <text>Set</text>\n\
    <x>430</x>\n\
    <y>42</y>\n\
    <width>22</width>\n\
    <height>16</height>\n\
    <font>\n\
      <font name="Default Bold" family="Liberation Sans" style="BOLD" size="14.0">\n\
      </font>\n\
    </font>\n\
    <horizontal_alignment>1</horizontal_alignment>\n\
    <auto_size>true</auto_size>\n\
  </widget>\n\
  <widget type="label" version="2.0.0">\n\
    <name>Label_244</name>\n\
    <text>Power</text>\n\
    <x>101</x>\n\
    <y>42</y>\n\
    <width>43</width>\n\
    <height>16</height>\n\
    <font>\n\
      <font name="Default Bold" family="Liberation Sans" style="BOLD" size="14.0">\n\
      </font>\n\
    </font>\n\
    <horizontal_alignment>1</horizontal_alignment>\n\
    <auto_size>true</auto_size>\n\
  </widget>\n\
  <widget type="label" version="2.0.0">\n\
    <name>Label_246</name>\n\
    <text>Channel</text>\n\
    <x>30</x>\n\
    <y>42</y>\n\
    <width>56</width>\n\
    <height>16</height>\n\
    <font>\n\
      <font name="Default Bold" family="Liberation Sans" style="BOLD" size="14.0">\n\
      </font>\n\
    </font>\n\
    <auto_size>true</auto_size>\n\
    <wrap_words>false</wrap_words>\n\
  </widget>\n\
  <widget type="label" version="2.0.0">\n\
    <name>Label_247</name>\n\
    <text> Set</text>\n\
    <x>178</x>\n\
    <y>42</y>\n\
    <width>26</width>\n\
    <height>16</height>\n\
    <font>\n\
      <font name="Default Bold" family="Liberation Sans" style="BOLD" size="14.0">\n\
      </font>\n\
    </font>\n\
    <horizontal_alignment>1</horizontal_alignment>\n\
    <auto_size>true</auto_size>\n\
    <wrap_words>false</wrap_words>\n\
  </widget>\n\
  <widget type="label" version="2.0.0">\n\
    <name>Label_248</name>\n\
    <text>Readback</text>\n\
    <x>234</x>\n\
    <y>42</y>\n\
    <width>67</width>\n\
    <height>16</height>\n\
    <font>\n\
      <font name="Default Bold" family="Liberation Sans" style="BOLD" size="14.0">\n\
      </font>\n\
    </font>\n\
    <horizontal_alignment>1</horizontal_alignment>\n\
    <auto_size>true</auto_size>\n\
    <wrap_words>false</wrap_words>\n\
  </widget>'
    
VSet_Format=\
'  <widget type="textentry" version="3.0.0">\n\
    <name>this_name</name>\n\
    <pv_name>this_pv_name</pv_name>\n\
    <x>xpos</x>\n\
    <y>ypos</y>\n\
    <width>52</width>\n\
    <height>28</height>\n\
    <background_color>\n\
      <color name="Read_Background" red="240" green="240" blue="240">\n\
      </color>\n\
    </background_color>\n\
    <horizontal_alignment>1</horizontal_alignment>\n\
  </widget>'    

VMon_Format=\
'  <widget type="textupdate" version="2.0.0">\n\
    <name>this_name</name>\n\
    <pv_name>this_pv_name</pv_name>\n\
    <x>xpos</x>\n\
    <y>ypos</y>\n\
    <width>52</width>\n\
    <height>28</height>\n\
    <horizontal_alignment>1</horizontal_alignment>\n\
    <vertical_alignment>1</vertical_alignment>\n\
  </widget>'

VDiff_Format=\
'  <widget type="textupdate" version="2.0.0">\n\
    <name>this_name</name>\n\
    <pv_name>this_pv_name</pv_name>\n\
    <x>xpos</x>\n\
    <y>ypos</y>\n\
    <width>52</width>\n\
    <height>28</height>\n\
    <vertical_alignment>1</vertical_alignment>\n\
  </widget>'


Label_format=\
'  <widget type="label" version="2.0.0">\n\
    <name>this_name</name>\n\
    <text>ch_num</text>\n\
    <x>xpos</x>\n\
    <y>ypos</y>\n\
    <width>52</width>\n\
    <height>28</height>\n\
    <font>\n\
      <font name="Default Bold" family="Liberation Sans" style="BOLD" size="14.0">\n\
      </font>\n\
    </font>\n\
    <horizontal_alignment>1</horizontal_alignment>\n\
    <auto_size>true</auto_size>\n\
    <wrap_words>false</wrap_words>\n\
  </widget>'

#------------------------------------------------------

def read_map(infile):
    lv_map = {}

    with open(infile, 'r') as f:
        for line in [x.strip() for x in f.readlines()]:
            if "#" in line:
                continue
            index = int(line.split()[0])
            crate = int(line.split()[1])
            slot = int(line.split()[2])
            channel = int(line.split()[3])
            pv_name = "MollerPS%d:%02d:%03d" % (crate, slot, channel)
            
            lv_map[str(index)] = {}
            lv_map[str(index)]["crate"] = crate
            lv_map[str(index)]["slot"] = slot
            lv_map[str(index)]["channel"] = channel
            lv_map[str(index)]["pv_name"] = pv_name

    return lv_map

"""
NewEntry=VSet_Format.replace("this_name", "Text Entry_0")
NewEntry=NewEntry.replace("this_pv_name", "MollerPS13:08:000:VSet")
NewEntry=NewEntry.replace("xpos", "30")
NewEntry=NewEntry.replace("ypos", "20")
"""

def add_label(name, ch, x, y, this_format):
    NewEntry = this_format.replace("this_name", name)
    NewEntry = NewEntry.replace("ch_num", ch)
    NewEntry = NewEntry.replace("xpos", str(x))
    NewEntry = NewEntry.replace("ypos", str(y))
    return NewEntry

def add_entry(name, pv_name, x, y, this_format):
    NewEntry = this_format.replace("this_name", name)
    NewEntry = NewEntry.replace("this_pv_name", pv_name)
    NewEntry = NewEntry.replace("xpos", str(x))
    NewEntry = NewEntry.replace("ypos", str(y))
    return NewEntry

def get_format(field):
    if field == "V0Set":
        return VMon_Format
    elif field == "VMon":
        return VMon_Format
    elif field == "VDiff":
        return VDiff_Format
    elif field == "I0Set":
        return VMon_Format
    elif field == "IMon":
        return VMon_Format
    else:
        return VDiff_Format

def get_expert_format(field):
    if field == "V0Set":
        return VSet_Format
    elif field == "VMon":
        return VMon_Format
    elif field == "VDiff":
        return VDiff_Format
    elif field == "I0Set":
        return VSet_Format
    elif field == "IMon":
        return VMon_Format
    else:
        return VDiff_Format


fields = ["V0Set", "VMon", "VDiff", "I0Set", "IMon", "IDiff"]
xbin = 77
x0 = [169, 169+xbin, 169+xbin*2, 419, 419+xbin, 419+xbin*2]
y0 = 68

lv_map = read_map("LV.txt")

f = open("ShowerMax-Table.bob", "w")
f.write(Skeleton_Format)

n = 0
ich = 0
for index in lv_map:
    # add text update/entry
    for i in range(6):
        name = "Text Entry_" + str(n)
        pv_name = "%s:%s" % (lv_map[index]["pv_name"], fields[i])
        xpos  = x0[i]
        ypos  = y0 + 28*ich
        fmt = get_format(fields[i])
        new_textentry = add_entry(name, pv_name, xpos, ypos, fmt)
        f.write(new_textentry)

        n = n+1

    # add channel number label
    name = "Label_ch" + str(ich)
    new_label = add_label(name, str(ich), 51, ypos, Label_format)        
    f.write(new_label)       
    ich = ich+1

f.write("</display>")
f.close()

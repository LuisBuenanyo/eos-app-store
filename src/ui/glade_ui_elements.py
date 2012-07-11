
bugs_and_feedback  = "".join(
"""
<?xml version="1.0"?> <interface> <requires lib="gtk+" version="2.16"/> <!-- interface-naming-policy toplevel-contextual --> <object class="GtkTextBuffer" id="Bugbuffer1"> <property name="text" translatable="yes">Something unexpected happened. Please let us know how the problem occured and we will resolve it as soon as possible.</property> </object> <object class="GtkAction" id="action1"/> <object class="GtkWindow" id="main_window"> <property name="title" translatable="yes">Bugs And Feedback</property> <property name="resizable">False</property> <property name="modal">True</property> <property name="skip_taskbar_hint">True</property> <property name="skip_pager_hint">True</property> <property name="urgency_hint">True</property> <property name="gravity">center</property> <property name="opacity">0.98000000022351741</property> <child> <object class="GtkVBox" id="vbox"> <property name="visible">True</property> <property name="border_width">20</property> <property name="spacing">20</property> <child> <object class="GtkHBox" id="hbox1"> <property name="height_request">50</property> <property name="visible">True</property> <property name="homogeneous">True</property> <child> <object class="GtkRadioButton" id="bug"> <property name="label" translatable="yes">Report a Bug</property> <property name="visible">True</property> <property name="can_focus">True</property> <property name="receives_default">False</property> <property name="draw_indicator">False</property> </object> <packing> <property name="position">0</property> </packing> </child> <child> <object class="GtkRadioButton" id="feedback"> <property name="label" translatable="yes">Give us feedback</property> <property name="visible">True</property> <property name="can_focus">True</property> <property name="receives_default">False</property> <property name="related_action">action1</property> <property name="draw_indicator">False</property> <property name="group">bug</property> </object> <packing> <property name="position">1</property> </packing> </child> </object> <packing> <property name="expand">False</property> <property name="fill">False</property> <property name="position">0</property> </packing> </child> <child> <object class="GtkHBox" id="hbox2"> <property name="visible">True</property> <child> <object class="GtkTextView" id="message_text"> <property name="width_request">350</property> <property name="height_request">100</property> <property name="visible">True</property> <property name="can_focus">True</property> <property name="has_focus">True</property> <property name="pixels_above_lines">2</property> <property name="wrap_mode">word-char</property> <property name="left_margin">5</property> <property name="right_margin">5</property> <property name="indent">5</property> <property name="buffer" translatable="yes">Bugbuffer1</property> <property name="overwrite">True</property> </object> <packing> <property name="position">0</property> </packing> </child> </object> <packing> <property name="position">1</property> </packing> </child> <child> <object class="GtkHBox" id="hbox3"> <property name="height_request">50</property> <property name="visible">True</property> <child> <object class="GtkButton" id="submit_button"> <property name="label" translatable="yes">SUBMIT</property> <property name="visible">True</property> <property name="can_focus">True</property> <property name="receives_default">True</property> <signal name="released" handler="feedback-submitted"/> </object> <packing> <property name="position">0</property> </packing> </child> </object> <packing> <property name="expand">False</property> <property name="fill">False</property> <property name="position">2</property> </packing> </child> </object> </child> </object> </interface>
""")
feedback_response_dialog  = "".join(
"""
<?xml version="1.0"?> <interface> <requires lib="gtk+" version="2.16"/> <!-- interface-naming-policy project-wide --> <object class="GtkWindow" id="main_window"> <property name="width_request">300</property> <property name="height_request">200</property> <property name="visible">True</property> <property name="can_focus">True</property> <property name="has_focus">True</property> <property name="type">popup</property> <property name="resizable">False</property> <property name="window_position">center</property> <property name="default_width">300</property> <property name="default_height">200</property> <property name="skip_taskbar_hint">True</property> <property name="skip_pager_hint">True</property> <property name="gravity">center</property> <child> <object class="GtkVBox" id="vbox1"> <property name="visible">True</property> <child> <object class="GtkLabel" id="label1"> <property name="visible">True</property> <property name="label" translatable="yes">Thank you for your feedback.</property> </object> <packing> <property name="position">0</property> </packing> </child> <child> <object class="GtkButton" id="button1"> <property name="label" translatable="yes">button</property> <property name="visible">True</property> <property name="can_focus">True</property> <property name="receives_default">True</property> </object> <packing> <property name="position">1</property> </packing> </child> </object> </child> </object> </interface>
""")

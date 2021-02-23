import jarray
import jmri
import re
import csv
import json

class CreateSignals(jmri.jmrit.automat.AbstractAutomaton):
    
    BASEDIR = "/Users/banerjia/jmri_layouts/CMRI_Scripting.jmri/resources"

    # Node Addresses
    NODE_ADDR = {
        "SENSORS": 1,
        "TURNOUTS": 2,
        "PANELS" : 3,
        "SIGNALS" : 4
    }

    # Station Config
    STATION_CD = "MML"
    SIGNAL_PREFIX = "M"

    def init(self):

        filePath = "{}/MML_sig_config.csv".format(self.BASEDIR)
        with open(filePath, 'rt') as fileSignals:
            fileSignalReader = csv.reader(fileSignals, delimiter = ',')

            # Counters
            header_skipped = False
            signal_turnout_counter = 1
            signalHead_counter = 1

            for signal_entry in fileSignalReader:
                if not header_skipped:
                    header_skipped = True
                    continue

                signal_userName = "{} {}".format(self.STATION_CD, signal_entry[0])
                #signal_systemName = "{}H{}".format(self.SIGNAL_PREFIX, signal_count)
                signal_aspect = signal_entry[1].lower()
                signal_panel_switch = signal_entry[2]
                _prop_string = re.sub('(\w+):([^;}]+)',r'"\1":"\2"',signal_entry[3]).replace(';',',')
                signal_properties = json.loads(_prop_string)

                
                if signal_aspect == "4-distant-approach":
                    # Create 4 Turnouts Red, Yellow, Green, Yellow2
                    # Attach 3 turnouts to one head
                    # Attach 1 turnout to second head
                    # Create mast with two heads
                    color_array = ['red', 'yellow', 'green', 'yellow2']
                    nmh_turnouts = []
                    for signalHeadTurnoutIndex in range(3):
                        signalHeadTurnout_SystemName = "CT{}{:03d}".format(self.NODE_ADDR["SIGNALS"], signal_turnout_counter + signalHeadTurnoutIndex)
                        signalHeadTurnout_UserName = "{} SignalHead:{}H{}:{}".format(self.STATION_CD,self.SIGNAL_PREFIX,signalHead_counter, color_array[signalHeadTurnoutIndex])

                        signalHeadTurnout = turnouts.newTurnout(signalHeadTurnout_SystemName, None)
                        signalHeadTurnout.setComment(signalHeadTurnout_UserName)
                        for signal_property in signal_properties:
                            signalHeadTurnout.setProperty(signal_property, signal_properties[signal_property])
                        signalHeadTurnout.setProperty("SignalColor", color_array[signalHeadTurnoutIndex].upper())
                        turnouts.register(signalHeadTurnout)
                        nmh_turnouts.append(jmri.NamedBeanHandle(signalHeadTurnout_SystemName, signalHeadTurnout))
                    
                    signal_turnout_counter = signal_turnout_counter + 3

                    signalHead1_userName = "{} Lower".format(signal_userName)
                    signalHead1_systemName = "{}H{}".format(self.SIGNAL_PREFIX, signalHead_counter)
                    signalHead1 = jmri.implementation.TripleTurnoutSignalHead(signalHead1_systemName,signalHead1_userName, nmh_turnouts[2], nmh_turnouts[1],nmh_turnouts[0])
                    signalHead1.setComment("Red/Yellow/Green")
                    signals.register(signalHead1)

                    signalHead_counter = signalHead_counter + 1

                    signalHeadTurnout_SystemName = "CT{}{:03d}".format(self.NODE_ADDR["SIGNALS"], signal_turnout_counter)
                    signalHeadTurnout_UserName = "{} SignalHead:{}H{}:{}".format(self.STATION_CD,self.SIGNAL_PREFIX,signalHead_counter, color_array[3])

                    signalHeadTurnout = turnouts.newTurnout(signalHeadTurnout_SystemName, None)
                    signalHeadTurnout.setComment(signalHeadTurnout_UserName)
                    for signal_property in signal_properties:
                        signalHeadTurnout.setProperty(signal_property, signal_properties[signal_property])
                    signalHeadTurnout.setProperty("SignalColor", color_array[3].upper())
                    turnouts.register(signalHeadTurnout)
                    nmh_turnout_yellow2 = jmri.NamedBeanHandle(signalHeadTurnout_SystemName, signalHeadTurnout)

                    signalHead2_userName = "{} Upper".format(signal_userName)
                    signalHead2_systemName = "{}H{}".format(self.SIGNAL_PREFIX, signalHead_counter)
                    signalHead2 = jmri.implementation.SingleTurnoutSignalHead(signalHead2_systemName,signalHead2_userName, nmh_turnout_yellow2, jmri.SignalHead.YELLOW, jmri.SignalHead.DARK)
                    signalHead2.setComment("Yellow/Dark")
                    signals.register(signalHead2)

                    signalMast_systemName = "IF$shsm:IndianRailways-2021:{}({})({})".format(signal_aspect, signalHead2_systemName,signalHead1_systemName)            
                    signalMast_userName = "{} {}".format(self.STATION_CD, signal_userName)
                    sm = masts.provideSignalMast(signalMast_systemName)
                    sm.setUserName(signalMast_userName)
                    masts.register(sm)

                    signalHead_counter = signalHead_counter + 1
                    signal_turnout_counter = signal_turnout_counter + 1
                elif signal_aspect == "2-general" or signal_aspect == "2-mainline-starter":
                    # Create Green/Yellow Light
                    signalHeadTurnout_SystemName = "CT{}{:03d}".format(self.NODE_ADDR["SIGNALS"], signal_turnout_counter )
                    signalHeadTurnout = turnouts.newTurnout(signalHeadTurnout_SystemName, None)
                    for signal_property in signal_properties:
                        signalHeadTurnout.setProperty(signal_property, signal_properties[signal_property])
                    if signal_aspect == "2-general":
                        signal_color = "yellow"
                    else:
                        signal_color = "green"
                    
                    signalHeadTurnout_UserName = "{} SignalHead:{}H{}:{}".format(self.STATION_CD,self.SIGNAL_PREFIX,signalHead_counter, signal_color)

                    signalHeadTurnout.setComment(signalHeadTurnout_UserName)
                    signalHeadTurnout.setProperty("SignalColor", signal_color.upper())
                    turnouts.register(signalHeadTurnout)
                    nmh_signalHead_yg = jmri.NamedBeanHandle(signalHeadTurnout_SystemName, signalHeadTurnout)
                    
                    signal_turnout_counter = signal_turnout_counter + 1

                    signalHead_Comment = "Red/{}".format(signal_color.capitalize())

                    # Create Red Light
                    signalHeadTurnout_SystemName = "CT{}{:03d}".format(self.NODE_ADDR["SIGNALS"], signal_turnout_counter )
                    signalHeadTurnout = turnouts.newTurnout(signalHeadTurnout_SystemName, None)
                    for signal_property in signal_properties:
                        signalHeadTurnout.setProperty(signal_property, signal_properties[signal_property])
                    
                    signal_color = "red"
                    
                    signalHeadTurnout_UserName = "{} SignalHead:{}H{}:{}".format(self.STATION_CD,self.SIGNAL_PREFIX,signalHead_counter, signal_color)

                    signalHeadTurnout.setComment(signalHeadTurnout_UserName)
                    signalHeadTurnout.setProperty("SignalColor", signal_color.upper())
                    turnouts.register(signalHeadTurnout)
                    nmh_signalHead_r = jmri.NamedBeanHandle(signalHeadTurnout_SystemName, signalHeadTurnout)

                    signal_turnout_counter = signal_turnout_counter + 1

                    signalHead_userName = "{}".format(signal_userName)
                    signalHead_systemName = "{}H{}".format(self.SIGNAL_PREFIX, signalHead_counter)
                    signalHead = jmri.implementation.DoubleTurnoutSignalHead(signalHead_systemName,signalHead_userName, nmh_signalHead_yg, nmh_signalHead_r)
                    
                    
                    signalHead.setComment(signalHead_Comment)
                    signals.register(signalHead)

                    signalHead_counter = signalHead_counter + 1

                    signalMast_systemName = "IF$shsm:IndianRailways-2021:{}({})".format(signal_aspect, signalHead_systemName)            
                    signalMast_userName = "{} {}".format(self.STATION_CD, signal_userName)
                    sm = masts.provideSignalMast(signalMast_systemName)
                    sm.setUserName(signalMast_userName)
                    masts.register(sm)


                    
                    


        return
    
    def handle(self):
        return 0

CreateSignals().start()
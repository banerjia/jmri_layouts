import jarray
import jmri
import re
import csv
import json

class CreateSignals(jmri.jmrit.automat.AbstractAutomaton):
    
    BASEDIR = "/home/banerjia/jmri_layouts/CMRI_Scripting.jmri/resources"

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

    # Signal Head Types
    SINGLEOUTPUT = 1
    DOUBLEOUTPUT = 2
    TRIPLEOUTPUT = 3


    # Counters
    __turnout_counter = 1
    __signalHead_counter = 1

    def init(self):

        self.__turnout_counter = 1
        self.__signalHead_counter = 1

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
                signal_aspect = signal_entry[1].lower()
                signal_panel_switch = signal_entry[2]
                _prop_string = re.sub('(\w+):([^;}]+)',r'"\1":"\2"',signal_entry[3]).replace(';',',')
                signal_properties = json.loads(_prop_string)
                nmh_signal_heads = []
                
                if signal_aspect == "4-distant-approach":
                    # Create 4 Turnouts Red, Yellow, Green, Yellow2
                    # Attach 3 turnouts to one head
                    # Attach 1 turnout to second head
                    # Create mast with two heads
                    color_array = ['red', 'yellow', 'green', 'yellow2']
                    nmh_turnouts = []
                    for signalHeadTurnoutIndex in range(3):

                        nmh_created_turnout = self.__createSignalLight(color_array[signalHeadTurnoutIndex], signal_properties)
                        nmh_turnouts.append(nmh_created_turnout)                    

                    signalHeadCreated = self.__createSignalHead(self.TRIPLEOUTPUT, signal_userName, "Lower", "Red/Yellow/Green", nmh_turnouts)
                    nmh_signal_heads.append(signalHeadCreated)

                    """
                    signalHead1_userName = "{} Lower".format(signal_userName)
                    signalHead1_systemName = "{}H{}".format(self.SIGNAL_PREFIX, signalHead_counter)
                    signalHead1 = jmri.implementation.TripleTurnoutSignalHead(signalHead1_systemName,signalHead1_userName, nmh_turnouts[2], nmh_turnouts[1],nmh_turnouts[0])
                    signalHead1.setComment("Red/Yellow/Green")
                    signals.register(signalHead1)

                    signalHead_counter = signalHead_counter + 1
                    """

                    nmh_turnouts = []
                    nmh_turnouts.append(self.__createSignalLight(color_array[3], signal_properties))
                    signalHeadCreated = self.__createSignalHead(self.SINGLEOUTPUT, signal_userName, "Upper", "Yellow/Dark", nmh_turnouts)
                    nmh_signal_heads.append(signalHeadCreated)

                    """
                    signalHead2_userName = "{} Upper".format(signal_userName)
                    signalHead2_systemName = "{}H{}".format(self.SIGNAL_PREFIX, signalHead_counter)
                    signalHead2 = jmri.implementation.SingleTurnoutSignalHead(signalHead2_systemName,signalHead2_userName, nmh_turnout_yellow2, jmri.SignalHead.YELLOW, jmri.SignalHead.DARK)
                    signalHead2.setComment("Yellow/Dark")
                    signals.register(signalHead2)
                    """

                    """
                    signalMast_systemName = "IF$shsm:IndianRailways-2021:{}({})({})".format(signal_aspect, signal_heads[1].getSystemName(),signal_heads[0].getSystemName())            
                    signalMast_userName = "{} {}".format(self.STATION_CD, signal_userName)
                    sm = masts.provideSignalMast(signalMast_systemName)
                    sm.setUserName(signalMast_userName)
                    masts.register(sm)

                    signalHead_counter = signalHead_counter + 1
                    signal_turnout_counter = signal_turnout_counter + 1
                    """
                elif signal_aspect == "2-general1" or signal_aspect == "2-mainline-starter1":
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

                
                signal_heads_in_mast_string = ""
                for nmh_signal_head in nmh_signal_heads:
                    signal_heads_in_mast_string = "{}({})".format(signal_heads_in_mast_string,nmh_signal_head.getBean().getSystemName())

                signal_mast_systemName = "IF$shsm:IndianRailways-2021:{}{}".format(signal_aspect, signal_heads_in_mast_string)            
                signal_mast_userName = "{} {}".format(self.STATION_CD, signal_userName)
                signal_mast = masts.provideSignalMast(signal_mast_systemName)
                signal_mast.setUserName(signal_mast_userName)
                masts.register(signal_mast)

        return
    
    def handle(self):
        return 0

    def __createSignalLight(self, signal_color, properties):
        
        signalHead_turnout_systemName = "CT{}{:03d}".format(self.NODE_ADDR["SIGNALS"], self.__turnout_counter )
        # Turnouts associated with Signal Heads typically don't expect USERNAMES
        # So populating the relevant information in the comments section instead
        signalHead_turnout_Comment = "{} SignalHead:{}H{}:{}".format(self.STATION_CD,self.SIGNAL_PREFIX,self.__signalHead_counter, signal_color)

        signalHead_turnout = turnouts.newTurnout(signalHead_turnout_systemName, None)
        signalHead_turnout.setComment(signalHead_turnout_Comment)
        signalHead_turnout.setProperty("SignalColor", signal_color.upper())
        
        for prop in properties:
            signalHead_turnout.setProperty(prop, properties[prop])
        
        turnouts.register(signalHead_turnout)

        nmh_signalHead_turnout = jmri.NamedBeanHandle(signalHead_turnout_systemName, signalHead_turnout)

        self.__turnout_counter = self.__turnout_counter + 1

        return nmh_signalHead_turnout

    def __createSignalHead(self, signal_head_type, signal_userName, signal_userName_suffix, color_comment, signal_turnout_nmh):

        signalHead_userName = "{} {}".format(signal_userName, signal_userName_suffix)
        signalHead_systemName = "{}H{}".format(self.SIGNAL_PREFIX, self.__signalHead_counter)
    
        if signal_head_type == self.SINGLEOUTPUT:
            signalHead = jmri.implementation.SingleTurnoutSignalHead(signalHead_systemName,signalHead_userName, signal_turnout_nmh[0], jmri.SignalHead.YELLOW, jmri.SignalHead.DARK)
        elif signal_head_type == self.TRIPLEOUTPUT:
            signalHead = jmri.implementation.TripleTurnoutSignalHead(signalHead_systemName,signalHead_userName, signal_turnout_nmh[2], signal_turnout_nmh[1],signal_turnout_nmh[0])

        signalHead.setComment(color_comment)
        signals.register(signalHead)

        self.__signalHead_counter = self.__signalHead_counter + 1

        nmh_signal_head = jmri.NamedBeanHandle(signalHead_systemName, signalHead)

        return nmh_signal_head


CreateSignals().start()
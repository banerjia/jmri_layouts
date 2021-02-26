import jarray
import jmri
import re
import csv
import json

class CreateSignals(jmri.jmrit.automat.AbstractAutomaton):
    
    BASEDIR = "/home/banerjia/jmri_layouts/N_Scale_Indian_Railways.jmri/resources"

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
                signal_panel_switch = (signal_entry[2].upper() == "TRUE")
                _prop_string = re.sub('(\w+):([^;}]+)',r'"\1":"\2"',signal_entry[3]).replace(';',',')
                signal_properties = json.loads(_prop_string)
                nmh_signal_heads = []
                nmh_turnouts = []
                
                if signal_aspect == "4-aspect":
                    # Create 4 Turnouts Red, Yellow, Green, Yellow2
                    # Attach 3 turnouts to one head
                    # Attach 1 turnout to second head
                    # Create mast with two heads
                    color_array = ['red', 'yellow', 'green', 'yellow-attn']

                    # 1. Create head with Red/Yellow/Green
                    for signalHeadTurnoutIndex in range(3):

                        nmh_created_turnout = self.__createSignalLight(color_array[signalHeadTurnoutIndex], signal_properties)
                        nmh_turnouts.append(nmh_created_turnout)                    

                    signalHeadCreated = self.__createSignalHead(self.TRIPLEOUTPUT, signal_userName, "LW", "Red/Yellow/Green", nmh_turnouts)
                    nmh_signal_heads.append(signalHeadCreated)

                    # 2. Create head with just Yellow
                    nmh_turnouts = []
                    nmh_turnouts.append(self.__createSignalLight(color_array[3], signal_properties))
                    signalHeadCreated = self.__createSignalHead(self.SINGLEOUTPUT, signal_userName, "UP", "Yellow/Dark", nmh_turnouts)
                    nmh_signal_heads.append(signalHeadCreated)

                elif signal_aspect == "2-aspect-rg" or signal_aspect == "2-aspect-ry":
                    # Create Green/Yellow Light
                    signal_userName_suffix = signal_aspect.replace("2-aspect-","").upper()

                    if signal_aspect == "2-aspect-ry":
                        signal_color = "yellow"
                    else:
                        signal_color = "green"

                    nmh_created_turnout = self.__createSignalLight('red', signal_properties)
                    nmh_turnouts.append(nmh_created_turnout)

                    nmh_created_turnout = self.__createSignalLight(signal_color, signal_properties)
                    nmh_turnouts.append(nmh_created_turnout)

                    signal_head_comment = "Red/{}".format(signal_color.capitalize())
                    
                    nmh_signal_head = self.__createSignalHead(self.DOUBLEOUTPUT, signal_userName, signal_userName_suffix, signal_head_comment, nmh_turnouts)

                    nmh_signal_heads.append(nmh_signal_head)
                elif signal_aspect == "3-aspect-with-y-route":
                    # The yellow light sitting between the branch lights is created in the first head
                    # but in board construction will be loaded on the top
                    color_array = ['red', 'green', 'yellow-div-r', 'yellow-div-r']

                    # 1. Create head with Red/Yellow/Green
                    for signalHeadTurnoutIndex in range(3):

                        nmh_created_turnout = self.__createSignalLight(color_array[signalHeadTurnoutIndex], signal_properties)
                        nmh_turnouts.append(nmh_created_turnout)                    

                    signalHeadCreated = self.__createSignalHead(self.TRIPLEOUTPUT, signal_userName, "LW DV", "Red/Green/Yellow", nmh_turnouts)
                    nmh_signal_heads.append(signalHeadCreated)

                    # 2. Create head with just Yellow Diverging Left
                    nmh_turnouts = []
                    nmh_turnouts.append(self.__createSignalLight(color_array[3], signal_properties))
                    signalHeadCreated = self.__createSignalHead(self.SINGLEOUTPUT, signal_userName, "UP DVL", "Yellow/Dark", nmh_turnouts)
                    nmh_signal_heads.append(signalHeadCreated)

                    # 3. Create head with just Yellow Diverging Right
                    nmh_turnouts = []
                    nmh_turnouts.append(self.__createSignalLight(color_array[3], signal_properties))
                    signalHeadCreated = self.__createSignalHead(self.SINGLEOUTPUT, signal_userName, "UP DVR", "Yellow/Dark", nmh_turnouts)
                    nmh_signal_heads.append(signalHeadCreated)
                elif signal_aspect == "3-aspect-with-route":
                    color_array = ['red', 'green', 'yellow', 'yellow-div']

                    # 1. Create head with Red/Yellow/Green
                    for signalHeadTurnoutIndex in range(3):

                        nmh_created_turnout = self.__createSignalLight(color_array[signalHeadTurnoutIndex], signal_properties)
                        nmh_turnouts.append(nmh_created_turnout)                    

                    signalHeadCreated = self.__createSignalHead(self.TRIPLEOUTPUT, signal_userName, "LW DV", "Red/Green/Yellow", nmh_turnouts)
                    nmh_signal_heads.append(signalHeadCreated)

                    # 2. Create head with just Yellow Diverging
                    nmh_turnouts = []
                    nmh_turnouts.append(self.__createSignalLight(color_array[3], signal_properties))
                    signalHeadCreated = self.__createSignalHead(self.SINGLEOUTPUT, signal_userName, "UP DV", "Yellow/Dark", nmh_turnouts)
                    nmh_signal_heads.append(signalHeadCreated)
                elif signal_aspect == "3-aspect":
                    color_array = ['red', 'yellow', 'green']

                    # 1. Create head with Red/Yellow/Green
                    for signalHeadTurnoutIndex in range(3):

                        nmh_created_turnout = self.__createSignalLight(color_array[signalHeadTurnoutIndex], signal_properties)
                        nmh_turnouts.append(nmh_created_turnout)                    

                    signalHeadCreated = self.__createSignalHead(self.TRIPLEOUTPUT, signal_userName, "DV", "Red/Yellow/Green", nmh_turnouts)
                    nmh_signal_heads.append(signalHeadCreated)
                else:
                    continue
                
                signal_heads_in_mast_string = ""
                for nmh_signal_head in nmh_signal_heads:
                    signal_heads_in_mast_string = "({}){}".format(nmh_signal_head.getBean().getSystemName(),signal_heads_in_mast_string)

                signal_mast_systemName = "IF$shsm:IndianRailways-2021:{}{}".format(signal_aspect, signal_heads_in_mast_string)            
                signal_mast_userName = signal_userName
                signal_mast = masts.provideSignalMast(signal_mast_systemName)
                signal_mast.setUserName(signal_mast_userName)
                masts.register(signal_mast)

        return
    
    def handle(self):
        return 0

    def __createSignalLight(self, signal_color, properties):
        """
            Logic: 
                1. Create a turnout to correspond with the light that is being registered
                2. Set the comment of the turnout so that it is easily understood
                3. Make sure to set the SignalColor property
                4. Set all the other properties
                5. Register the turnout
                6. Generate a NamedBeanHandle to use as a return value
        """

        
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

        """
            Logic: 
                1. Generate the necessary Username and SystemNames for the signal head
                2. Based on the signal_head_type call the appropriate function to create the head
                3. Set the comment on the signal head to describe the color combination, purely for documentation
                4. Register the signal head
                5. Pass a NamedBeanHandle to the signal head back to the calling function
        """
        signalHead_userName = "{} {}".format(signal_userName, signal_userName_suffix)
        signalHead_systemName = "{}H{}".format(self.SIGNAL_PREFIX, self.__signalHead_counter)
        
        if signal_head_type == self.SINGLEOUTPUT:
            signalHead = jmri.implementation.SingleTurnoutSignalHead(signalHead_systemName,signalHead_userName, signal_turnout_nmh[0], jmri.SignalHead.YELLOW, jmri.SignalHead.DARK)
        elif signal_head_type == self.TRIPLEOUTPUT:
            signalHead = jmri.implementation.TripleTurnoutSignalHead(signalHead_systemName,signalHead_userName, signal_turnout_nmh[2], signal_turnout_nmh[1],signal_turnout_nmh[0])
        elif signal_head_type == self.DOUBLEOUTPUT:
            signalHead = jmri.implementation.DoubleTurnoutSignalHead(signalHead_systemName,signalHead_userName, signal_turnout_nmh[1],signal_turnout_nmh[0])

        signalHead.setComment(color_comment)
        signals.register(signalHead)

        self.__signalHead_counter = self.__signalHead_counter + 1

        nmh_signal_head = jmri.NamedBeanHandle(signalHead_systemName, signalHead)

        return nmh_signal_head


CreateSignals().start()
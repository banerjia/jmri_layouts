"""
    File: create_blocks.py
    Author: Abhishek Banerji
    Purpose: Create blocks, sensors and lights and associate them with each other as needed
    Algorithm
        - Step 1: Get basic information about the block - name, panel indicator and properties
        - Step 2: Create Sensor
        - Step 3: Create Block and connect to sensor
        - Step 4: If Panel Indicator is needed, create light and associate with sensor

    Block Configuration File Structure
        - User Name
        - Panel
        - Comments
        - Properties

"""


import csv
import json
import re
import jarray
import jmri


class CreateBlocks(jmri.jmrit.automat.AbstractAutomaton) :
    """
     Script Configuration
    """
    BASEDIR = "/home/banerjia/jmri_layouts/CMRI_Scripting.jmri/resources"
            
    # Node Addresses
    NODE_ADDR = {
        "SENSORS": 1,
        "TURNOUTS": 2,
        "PANELS" : 3
    }

    # Station Config
    STATION_CD = 'MML'


    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.

        filePath = "{}/MML_blk_config.csv".format(self.BASEDIR)
        with open(filePath, 'rt') as fileBlocks:
            
            fileBlocksReader = csv.reader(fileBlocks, delimiter = ',')

            # Counters
            header_skipped = False
            sensors_count = 1
            panel_lights_count = 1
            turnouts_count = 1
            blocks_count = 1

            for block_entry in fileBlocksReader:
                # Skip Header Row
                if not header_skipped:
                    header_skipped = True
                    continue
                
                # Gather basic information
                block_userName = block_entry[0]
                block_userName_for_related_objects = block_userName.replace(self.STATION_CD, '').lstrip()
                block_panel_ind = (block_entry[1] == '1')
                block_comments = block_entry[2]
                _prop_string = re.sub('(\w+):([^;}]+)',r'"\1":"\2"',block_entry[3]).replace(';',',')
                block_properties = json.loads(_prop_string)

                # Create Block and associate sensor
                block_systemName = "IB{}:AUTO:{:03d}".format(self.NODE_ADDR["SENSORS"],blocks_count)

                blocks_count = blocks_count + 1

                obj_block = blocks.provideBlock(block_systemName)
                obj_block.setUserName(block_userName)
                obj_block.setComment(block_comments)
                
                for block_property in block_properties:
                    obj_block.setProperty(block_property, block_properties[block_property])
                
                obj_block.setProperty('PanelIndicator', block_panel_ind)
                blocks.register(obj_block)


        return

    def handle(self):
        return 0

CreateBlocks().start()

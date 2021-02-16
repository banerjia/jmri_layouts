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


    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.

        filePath = "{}/MML_blk_config.csv".format(self.BASEDIR)
        with open(filePath, 'rt',encoding="utf8") as fileBlocks:
            
            fileBlocksReader = csv.reader(fileBlocks, delimiter = ',')

            # Counters
            header_skipped = False
            sensors_count = 1
            panel_lights_count = 1
            turnouts_count = 1
            blocks_count = 1
            blocks_prefix = 'TT1'

            for block_entry in fileBlocksReader:
                # Skip Header Row
                if not header_skipped:
                    header_skipped = True
                    continue
                
                # Gather basic information
                block_userName = block_entry[0]
                block_panel_ind = (block_entry[1] == '1')
                block_comments = block_entry[2]
                _prop_string = re.sub('(\w+):([^:]+)',r'"\1":"\2"',block_entry[3]).replace(';',',')
                block_properties = json.loads(_prop_string)

                # Create Sensor
                sensor_systemName = "CS{:d}{:03d}".format(self.NODE_ADDR["SENSORS"], sensors_count)
                sensor_userName = "SNSR IND {}".format(block_userName)

                sensors_count = sensors_count + 1

                obj_sensor = sensors.provideSensor(sensor_systemName)
                obj_sensor.setUserName(sensor_userName)
                obj_sensor.setComment("Sensor for block occupancy of {}".format(block_userName))
                obj_sensor.setProperty("Purpose", "BlockOccupancyDetection")
                sensors.register(obj_sensor)

                # Get NamedBeanHandle for the sensor to use with block
                nmh_sensor = jmri.NamedBeanHandle(sensor_systemName, obj_sensor)

                # Create Block and associate sensor
                block_systemName = "IB{}:AUTO:{:03d}".format(self.NODE_ADDR["SENSORS"],blocks_count)

                blocks_count = blocks_count + 1

                obj_block = blocks.provideBlock(block_systemName)
                obj_block.setUserName(block_userName)
                obj_block.setComment(block_comments)
                obj_block.setNamedSensor(nmh_sensor)
                for block_property in block_properties:
                    obj_block.setProperty(block_property, block_properties[block_property])
                
                blocks.register(obj_block)

                # Create light for panel if needed
                if block_panel_ind:
                    light_systemName = "CL{}{:03d}".format(self.NODE_ADDR["PANELS"],panel_lights_count)
                    light_userName = "PNL IND {}".format(block_userName)

                    panel_lights_count = panel_lights_count + 1

                    obj_light = lights.provideLight(light_systemName)
                    obj_light.setUserName(light_userName)
                    obj_light.setComment("Block occupany indicator on panel for {}".format(block_userName))

                    # Attach light to sensor
                    obj_light.addLightControl(jmri.implementation.LightControl())
                    obj_light_lightControl = obj_light.getLightControlList()[-1]
                    obj_light_lightControl.setControlSensorName(sensor_userName)
                    obj_light_lightControl.setControlType(jmri.Light.SENSOR_CONTROL)
                    obj_light_lightControl.setControlSensorSense(jmri.Sensor.ACTIVE)
                    obj_light_lightControl.setParentLight(obj_light)
                    obj_light_lightControl.activateLightControl()

                    lights.register(obj_light)
                    """
                    if block_properties["SensedObject"] != "BlockOverSwitch":
                        light_systemName = "CL{}{:03d}".format(self.NODE_ADDR["PANELS"],panel_lights_count)
                        light_userName = "PNL IND {}".format(block_userName)

                        panel_lights_count = panel_lights_count + 1

                        obj_light = lights.provideLight(light_systemName)
                        obj_light.setUserName(light_userName)
                        obj_light.setComment("Block occupany indicator on panel for {}".format(block_userName))

                        # Attach light to sensor
                        obj_light.addLightControl(jmri.implementation.LightControl())
                        obj_light_lightControl = obj_light.getLightControlList()[-1]
                        obj_light_lightControl.setControlSensorName(sensor_userName)
                        obj_light_lightControl.setControlType(jmri.Light.SENSOR_CONTROL)
                        obj_light_lightControl.setControlSensorSense(jmri.Sensor.ACTIVE)
                        obj_light_lightControl.setParentLight(obj_light)
                        obj_light_lightControl.activateLightControl()

                        lights.register(obj_light)
                    else:
                    """
        return

    def handle(self):
        return 0

CreateBlocks().start()

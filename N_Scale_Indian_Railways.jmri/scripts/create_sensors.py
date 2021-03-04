import jarray
import jmri
import re

class CreateSensors(jmri.jmrit.automat.AbstractAutomaton):
    """
     Script Configuration
    """
            
    # Node Addresses
    NODE_ADDR = {
        "SENSORS": 1,
        "TURNOUTS": 2,
        "PANELS" : 3,
        "SIGNALS" : 4
    }

    # Station Config
    STATION_CD = 'MML'

    def init(self):

        sensors_count = 1
        turnouts_sensors_counts = 1
        panel_sensors_count = 1

        #  Sensors for Turnouts
        
        switches = turnouts.getNamedBeanSet()

        for switch in switches:
            station_cd = switch.getProperty("StationCode")
            switch_type = switch.getProperty("SwitchType")
            switch_userName = switch.getUserName()

            # Ignore turnout of other stations and any turnouts that are not switches
            if station_cd != self.STATION_CD or switch_type == None:
                continue

            # Create Feedback Sensor
            sensor_systemName = "CS{:d}{:03d}".format(self.NODE_ADDR["TURNOUTS"], turnouts_sensors_counts)
            sensor_userName = "{} SNR IND {}".format(self.STATION_CD, switch_userName)
            
            obj_sensor = sensors.provideSensor(sensor_systemName)
            obj_sensor.setUserName(sensor_userName)
            obj_sensor.setComment("Feedback sensor for  {}".format(switch_userName))
            obj_sensor.setProperty("Purpose", "SwitchFeedback")
            obj_sensor.setProperty("StationCode", self.STATION_CD)
            turnouts_sensors_counts = turnouts_sensors_counts + 1
            sensors.register(obj_sensor)
            nmh_sensor = jmri.NamedBeanHandle(sensor_systemName, obj_sensor)

            # Attach feedback sensor to turnout
            switch.setFeedbackMode(jmri.Turnout.ONESENSOR)
            switch.provideFirstFeedbackNamedSensor(nmh_sensor)

            # Create Panel Sensor if a toggle switch is needed for this turnout
            if switch.getProperty('PanelSwitch'):
                sensor_systemName = "CS{:d}{:03d}".format(self.NODE_ADDR["PANELS"], panel_sensors_count)
                sensor_userName = "{} PNL SNR {}".format(self.STATION_CD, switch_userName)
                
                obj_sensor = sensors.provideSensor(sensor_systemName)
                obj_sensor.setUserName(sensor_userName)
                obj_sensor.setComment("Panel toggle sensor for  {}".format(switch_userName))
                obj_sensor.setProperty("Purpose", "SwitchFeedback")
                obj_sensor.setProperty("StationCode", self.STATION_CD)
                panel_sensors_count = panel_sensors_count + 1
                sensors.register(obj_sensor)   

                switch.setProperty("PanelSwitchSystemName", sensor_systemName)            


        # Create sensors for block detection
        layout_blocks = blocks.getNamedBeanSet()

        for layout_block in layout_blocks:

            station_cd = layout_block.getProperty("StationCode")
            block_userName = layout_block.getUserName()

            # Ignore switches of other stations
            if station_cd != self.STATION_CD:
                continue

            sensor_systemName = "CS{:d}{:03d}".format(self.NODE_ADDR["SENSORS"], sensors_count)
            sensor_userName = "{} BCD {}".format(self.STATION_CD, block_userName)
            
            obj_sensor = sensors.provideSensor(sensor_systemName)
            obj_sensor.setUserName(sensor_userName)
            obj_sensor.setComment("Block occupancy detector for  {}".format(block_userName))
            obj_sensor.setProperty("Purpose", "BlockOccupancyDetector")
            obj_sensor.setProperty("StationCode", self.STATION_CD)
            sensors_count = sensors_count + 1
            sensors.register(obj_sensor)  

            nmh_sensor = jmri.NamedBeanHandle(sensor_systemName, obj_sensor)

            layout_block.setNamedSensor(nmh_sensor)
            
        return
    
    def handle(self):
        return 0

CreateSensors().start()
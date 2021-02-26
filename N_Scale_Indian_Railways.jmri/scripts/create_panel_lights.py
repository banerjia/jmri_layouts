import jarray
import jmri


class CreatePanelLights(jmri.jmrit.automat.AbstractAutomaton):

    # Node Addresses
    NODE_ADDR = {
        "SENSORS":  1,
        "TURNOUTS": 2,
        "PANELS" :  3,
        "SIGNALS":  4
    }

    STATION_CODE = 'MML'

    def init(self):

        panel_lights_count = 1

        station_blocks = blocks.getNamedBeanSet()
        
        for station_block in station_blocks:

            try:
                station_code = station_block.getProperty('StationCode')
            except Exception:
                print("Station Code Exception")
                continue

            # If STATION CODE does not match with the ones for this iteration then move on.
            if(station_code != self.STATION_CODE):
                continue
               
            panel_indicator = (station_block.getProperty("PanelIndicator").upper() == "TRUE")

            # Create Lights only if block is configured to show a panel light
            if panel_indicator:
                try:
                    block_sensor = station_block.getNamedSensor().getBean()
                except Exception:
                    print("Unable to get sensor for: {}".format(station_block.getUserName()))
                    continue

                
                # Construct the names for the light object
                block_panel_light_systemName = "CL{}{:03d}".format(self.NODE_ADDR["PANELS"], panel_lights_count)
                block_panel_light_userName = "{} PNL LGT IND {}".format(self.STATION_CODE, station_block.getUserName())

                # Build Light Control
                block_light_control = jmri.implementation.LightControl()
                block_light_control.setControlSensorName(block_sensor.getUserName())
                block_light_control.setControlType(jmri.Light.SENSOR_CONTROL)
                block_light_control.setControlSensorSense(jmri.Sensor.ACTIVE)

                # Build Light
                block_panel_light = lights.newLight(block_panel_light_systemName, block_panel_light_userName)
                block_panel_light.addLightControl(block_light_control)
                block_light_control.setParentLight(block_panel_light)
                lights.register(block_panel_light)

                block_light_control.activateLightControl()

                panel_lights_count = panel_lights_count + 1
                
                # If this block has a switch then create another light that will show the switch state
                # We are going to be using the state reported by the switch's feedback sensor for this purpose 
                if(station_block.getProperty("SensedObject").upper() == "BLOCKOVERSWITCH"):
                    # Construct the names for the light object
                    
                    sw_userName = station_block.getProperty("RelatedStationObject")
                    sw_userName = "{} {}".format(self.STATION_CODE, sw_userName)
                    
                    blockos_switch = jmri.InstanceManager.getDefault(jmri.TurnoutManager).getByUserName(sw_userName)

                    blockos_feedback_sensor = blockos_switch.getFirstNamedSensor().getBean()

                    blockos_panel_light_systemName = "CL{}{:03d}".format(self.NODE_ADDR["PANELS"], panel_lights_count)
                    blockos_panel_light_userName = "{} PNL BLK SW IND {}".format(self.STATION_CODE, blockos_switch.getUserName())


                    # Build Light Control
                    blockos_light_control = jmri.implementation.LightControl()
                    blockos_light_control.setControlSensorName(blockos_feedback_sensor.getUserName())
                    blockos_light_control.setControlType(jmri.Light.SENSOR_CONTROL)
                    blockos_light_control.setControlSensorSense(jmri.Sensor.ACTIVE)

                    # Build Light
                    blockos_panel_light = lights.newLight(blockos_panel_light_systemName, blockos_panel_light_userName)
                    blockos_panel_light.addLightControl(blockos_light_control)
                    blockos_light_control.setParentLight(blockos_panel_light)
                    lights.register(blockos_panel_light)

                    blockos_light_control.activateLightControl()
                                        
                    panel_lights_count = panel_lights_count + 1

                    
                    

                    
                    

        return

    def handle(self):
        return 0

CreatePanelLights().start()

"""
def init(self):
        lc = jmri.implementation.LightControl()
        lc.setControlSensorName(sensors.provideSensor('CS1001').getUserName())
        lc.setControlType(jmri.Light.SENSOR_CONTROL)
        lc.setControlSensorSense(jmri.Sensor.ACTIVE)

        l = lights.newLight('CL4001','Test Light')
        l.addLightControl(lc)
        lights.register(l)
        return
    
    def handle(self):
        return 0
"""
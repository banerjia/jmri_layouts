"""
                # Create Sensor
                sensor_systemName = "CS{:d}{:03d}".format(self.NODE_ADDR["SENSORS"], sensors_count)
                sensor_userName = "{} SNSR IND {}".format(self.STATION_CD, block_userName_for_related_objects)

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
                    light_userName = "{} PNL IND {}".format(self.STATION_CD,block_userName_for_related_objects)

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

                    if block_properties["SensedObject"] != "BlockOverSwitch":
                        obj_turnout = block_properties["RelatedObject"]
                        # Lights to Represent when SW is in N position
                        bd_status = ['CLR', 'OCP']

                        lc_sw_closed = jmri.implementation.LightControl()
                        lc_sw_closed.setControlTurnout(obj_turnout)
                        lc_sw_closed.setControlTurnoutState(jmri.Turnout.CLOSED)

                        lc_sw_thrown = jmri.implementation.LightControl()
                        lc_sw_thrown.setControlTurnout(obj_turnout)
                        lc_sw_thrown.setControlTurnoutState(jmri.Turnout.THROWN)
                        for i in range(0,1):

                            light_systemName = "CL{}{:03d}".format(self.NODE_ADDR["PANELS"],panel_lights_count)
                            light_userName = "{} PNL IND SW {} CLS {}".format(self.STATION_CD, block_userName_for_related_objects, bd_status[i])

                            panel_lights_count = panel_lights_count + 1

                            obj_light = lights.provideLight(light_systemName)
                            obj_light.setUserName(light_userName)
                            obj_light.setComment("Block occupany indicator on panel for switch {} in CLOSED with BD status {}".format(block_userName_for_related_objects, bd_status[i]))

                           
                            # Attach Switch condition
                            obj_light.addLightControl(lc_sw_closed)
                            obj_light_lightControl = obj_light.getLightControlList()[-1]
                            obj_light_lightControl.setParentLight(obj_light)
                            obj_light_lightControl.activateLightControl()


                            obj_light.addLightControl(jmri.implementation.LightControl())
                            obj_light_lightControl = obj_light.getLightControlList()[-1]
                            obj_light_lightControl.setControlSensorName(sensor_userName)
                            obj_light_lightControl.setControlType(jmri.Light.SENSOR_CONTROL)
                            if x == 0:
                                # Switch is not occupied
                                obj_light_lightControl.setControlSensorSense(jmri.Sensor.INACTIVE)
                            else:
                                obj_light_lightControl.setControlSensorSense(jmri.Sensor.ACTIVE)
                            obj_light_lightControl.setParentLight(obj_light)
                            obj_light_lightControl.activateLightControl()

                            lights.register(obj_light)
                    """
                    """
                        # Lights to Represent when SW is in THR position
                        for x in range(0,1):
                            light_systemName = "CL{}{:03d}".format(self.NODE_ADDR["PANELS"],panel_lights_count)
                            light_userName = "{} PNL IND SW {} CLS CLR".format(self.STATION_CD, block_userName_for_related_objects)

                            panel_lights_count = panel_lights_count + 1

                            obj_light = lights.provideLight(light_systemName)
                            obj_light.setUserName(light_userName)
                            obj_light.setComment("Block occupany indicator on panel for switch {}".format(block_userName_for_related_objects))

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
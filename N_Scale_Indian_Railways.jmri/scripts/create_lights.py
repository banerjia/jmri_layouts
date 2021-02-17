import jarray
import jmri

class CreateLights(jmri.jmrit.automat.AbstractAutomaton):

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

CreateLights().start()
import jarray
import jmri

class CreateSignals(jmri.jmrit.automat.AbstractAutomaton):

    def init(self):
        SIGNALS_NODE_ADDR = 3
        turnout_count = 1

        signalHead_Green_SysName = "CT{}{:03d}".format(SIGNALS_NODE_ADDR, turnout_count)
        signalHead_Green_UserName = "SignalHead:{}:Green".format("CH1")
        turnout_count = turnout_count + 1
        t_Green = turnouts.newTurnout(signalHead_Green_SysName, signalHead_Green_UserName)
        t_Green.setComment(signalHead_Green_UserName)

        signalHead_Red_SysName = "CT{}{:03d}".format(SIGNALS_NODE_ADDR, turnout_count)
        signalHead_Red_UserName = "SignalHead:{}:Red".format("CH1")
        turnout_count = turnout_count + 1
        t_Red = turnouts.newTurnout(signalHead_Red_SysName, signalHead_Red_UserName)
        t_Red.setComment(signalHead_Red_UserName)

        nmh1 = jmri.NamedBeanHandle(signalHead_Green_SysName, t_Green)
        nmh2 = jmri.NamedBeanHandle(signalHead_Red_SysName, t_Red)
        sig = jmri.implementation.DoubleTurnoutSignalHead("CH1","SGH 1R", nmh1, nmh2)
        signals.register(sig)

        signalMastName = "IF$shsm:IndianRailways-2021:2-general({})".format(sig.getSystemName())
        sm = masts.provideSignalMast(signalMastName)
        sm.setUserName('SignalTest')

        

        return
    
    def handle(self):
        return 0

CreateSignals().start()
#!python3

import irsdk
import time
import subprocess
import sys
sys.stdout = open('my_stdout.log', 'w')
sys.stderr = open('my_stderr.log', 'w')
#Variable to check for change
stream_title = ""

# this is our State class, with some helpful variables
class State:
    ir_connected = True
    last_car_setup_tick = -1

# here we check if we are connected to iracing
# so we can retrieve some data
def check_iracing():
    if state.ir_connected and not (ir.is_initialized and ir.is_connected):
        state.ir_connected = False
        # don't forget to reset your State variables
        state.last_car_setup_tick = -1
        # we are shutting down ir library (clearing all internal variables)
        ir.shutdown()
        print('irsdk disconnected')
    elif not state.ir_connected and ir.startup() and ir.is_initialized and ir.is_connected:
        state.ir_connected = True
        print('irsdk connected')


# our main loop, where we retrieve data
# and do something useful with it
def loop():
    global stream_title

    # on each tick we freeze buffer with live telemetry
    # it is optional, but useful if you use vars like CarIdxXXX
    # this way you will have consistent data from those vars inside one tick
    # because sometimes while you retrieve one CarIdxXXX variable
    # another one in next line of code could change
    # to the next iracing internal tick_count
    # and you will get incosistent data
    ir.freeze_var_buffer_latest()

    # retrieve live telemetry data
    # check here for list of available variables
    # https://github.com/kutu/pyirsdk/blob/master/vars.txt
    # this is not full list, because some cars has additional
    # specific variables, like break bias, wings adjustment, etc
    current_session=ir['SessionNum']
    if  stream_title != ir['SessionInfo']['Sessions'][current_session]['SessionType']+' at '+ir['WeekendInfo']['TrackDisplayName']:
        stream_title = ir['SessionInfo']['Sessions'][current_session]['SessionType']+' at '+ir['WeekendInfo']['TrackDisplayName']
        print("Update stream title!")
        print(stream_title)
        try:
            subprocess.call("botwitch.exe -t \""+stream_title+"\"")
        except subprocess.CalledProcessError as error:
            exit("Subprocess exception")

if __name__ == '__main__':
    # initializing ir and state
    ir = irsdk.IRSDK()
    #ir.startup(test_file='data.bin')
    state = State()

    try:
        # infinite loop
        while True:
            # check if we are connected to iracing
            check_iracing()
            # if we are, then process data
            if state.ir_connected:
                loop()
            # sleep for 1 second
            # maximum you can use is 1/60
            # cause iracing updates data with 60 fps
            time.sleep(1)
    except KeyboardInterrupt:
        # press ctrl+c to exit
        pass

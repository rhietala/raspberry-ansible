from w1thermsensor import W1ThermSensor
import rrdtool
import os.path

DATABASE_PATH = '/home/pi/'
LAST_DAY_GRAPH_FILE = '/home/pi/current.png'
COLORS = ('#AA3939', '#226666', '#AA6C39', '#2D882D')
SENSOR_NAMES = {
    '0000075f24dc': 'Living room'
}

def sensor_name(id):
    if SENSOR_NAMES.has_key(id):
        return SENSOR_NAMES[id]
    else:
        return id

def create_rrd_unless_exists(filename):
    if os.path.isfile(filename):
        return

    print("Creating RRD database file %s" % filename)
    rrdtool.create(
        filename,
        'DS:temp:GAUGE:600:-100:100',
        'RRA:AVERAGE:0.5:1:525600'
    )

def graph_last_day(sensors):
    defs = []
    lines = []
    current_temps = ['COMMENT: \l']
    for i, sensor in enumerate(sorted(W1ThermSensor.get_available_sensors(),
                                      key=lambda sensor: sensor.id)):
        color = COLORS[i % len(COLORS)];
        defs.append('DEF:' + sensor.id + '=' +
                    DATABASE_PATH + sensor.id + '.rrd:temp:AVERAGE')
        lines.append('LINE1:' + sensor.id + color + ':' +
                     sensor_name(sensor.id))
        current_temps.append('GPRINT:' + sensor.id +
                             ':LAST:' + sensor_name(sensor.id) + '\: %4.2lf\l')

    params = [
        LAST_DAY_GRAPH_FILE,
        '-a', 'PNG',
        '-w', '640',
        '-h', '250',
        '--start', '-86400',
        '--end', 'now',
        '--lower-limit', '18',
        '--upper-limit', '28',
        '--rigid',
        '--vertical-label', 'Temp, deg C'] + defs + lines + current_temps

    rrdtool.graph(*params)

for sensor in W1ThermSensor.get_available_sensors():
    filename = sensor.id + '.rrd'
    create_rrd_unless_exists(filename)
    error = rrdtool.update(filename, 'N:%.2lf' % (sensor.get_temperature()))
    print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))

graph_last_day(W1ThermSensor.get_available_sensors())

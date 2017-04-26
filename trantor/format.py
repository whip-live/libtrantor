from construct import Struct, Int, Short, Int24ub, Byte, Double
from datetime import datetime


# A recording line
RecordingLine = Struct(
    'timestamp' / Int,
    'lat' / Double,
    'lon' / Double,
    'course' / Int,
    'geoid_height' / Int,
    'elevation' / Int,
    'fix' / Byte,
    'satellites' / Byte,
    'hdop' / Short,
    'vdop' / Short,
    'pdop' / Short,
    'tdop' / Short,
    'speed' / Int,
    'acc_x' / Short,
    'acc_y' / Short,
    'acc_z' / Short,
    'barometer' / Int24ub,
    'giroscope_x' / Short,
    'giroscope_y' / Short,
    'giroscope_z' / Short,
    'magnetometer_x' / Short,
    'magnetometer_y' / Short,
    'magnetometer_z' / Short,
    'temperature' / Short,
)


def build(timestamp, lat, lon, course, geoid_height, elevation, fix,
          satellites, hdop, vdop, pdop, tdop, speed, acc_x, acc_y, acc_z,
          barometer, giroscope_x, giroscope_y, giroscope_z, magnetometer_x,
          magnetometer_y, magnetometer_z, temperature):
    """
    Builds the binary representation given the data
    """
    # We expect a timestamp, but we only need one decimal precision and
    # we represent it as an integer
    timestamp = int(timestamp * 10)
    return RecordingLine.build(dict(
        timestamp=timestamp, lat=lat, lon=lon, course=course,
        geoid_height=geoid_height, elevation=elevation, fix=fix,
        satellites=satellites, hdop=hdop, vdop=vdop, pdop=pdop,
        tdop=tdop, speed=speed, acc_x=acc_x, acc_y=acc_y, acc_z=acc_z,
        barometer=barometer, giroscope_x=giroscope_x, giroscope_y=giroscope_y,
        giroscope_z=giroscope_z, magnetometer_x=magnetometer_x,
        magnetometer_y=magnetometer_y, magnetometer_z=magnetometer_z,
        temperature=temperature))


def parse(binary_data):
    """
    Takes a binary string as input, parse it, and yields one result at a time
    """
    results = RecordingLine[:].parse(binary_data)
    for element in results:
        row = dict(element)
        # TODO: Fix starting time of the timestamp when we'll
        #       have the configuration header
        row['timestamp'] = datetime.fromtimestamp(row['timestamp'] / 10)
        yield row

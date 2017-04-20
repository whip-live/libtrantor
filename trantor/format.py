from construct import Struct, Int, Short, Int24ub, Byte, Double


# A recording line
RecordingLine = Struct(
    'timestamp' / Int,
    'lat' / Double,
    'lon' / Double,
    'course' / Short,
    'geoid_height' / Short,
    'elevation' / Short,
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
        yield dict(element)

from construct import (
    Struct, BitStruct, Bit, BitsInteger,
    Int32ub, Int16ub, Int24ub, Int8ub)
from decimal import Decimal


# Custom float representing latitude and longitude
CustomFloat32sb = BitStruct(
    'sign' / Bit,
    'exp' / BitsInteger(3),
    'digits' / BitsInteger(28)
)

# A recording line
RecordingLine = Struct(
    'timestamp' / Int32ub,
    'lat' / CustomFloat32sb,
    'lon' / CustomFloat32sb,
    'course' / Int16ub,
    'geoid_height' / Int16ub,
    'elevation' / Int16ub,
    'fix' / Int8ub,
    'satellites' / Int8ub,
    'hdop' / Int16ub,
    'vdop' / Int16ub,
    'pdop' / Int16ub,
    'tdop' / Int16ub,
    'speed' / Int32ub,
    'acc_x' / Int16ub,
    'acc_y' / Int16ub,
    'acc_z' / Int16ub,
    'barometer' / Int24ub,
    'giroscope_x' / Int16ub,
    'giroscope_y' / Int16ub,
    'giroscope_z' / Int16ub,
    'magnetometer_x' / Int16ub,
    'magnetometer_y' / Int16ub,
    'magnetometer_z' / Int16ub,
    'temperature' / Int16ub,
)


def _frexp10(number):
    """
    Takes a float and returns it in the form of (sign, exponent, digits)
    """
    # Casting number to string to avoid floating point representation errors
    sign, digits, exp = Decimal('%s' % number).as_tuple()
    mantissa = int(''.join(map(str, digits)))
    # Returning the absolute value of the exponent, as we know it will
    # always be negative, therefore it is stored in our struct as unsigned int
    # Next calculations account this fact.
    return sign, abs(exp), mantissa


def _make_float(sign=0, exp=0, digits=0):
    """
    Takes a tuple of (sign, exp, digits) and returns a float
    """
    # Takes a number `digits`, convert it into a tuple of integers,
    # pass it to Decimal with sign and -exponent to build the float we want
    return float(Decimal((sign, tuple(map(int, str(digits))), -exp)))


def build(timestamp, lat, lon, course, geoid_height, elevation, fix,
          satellites, hdop, vdop, pdop, tdop, speed, acc_x, acc_y, acc_z,
          barometer, giroscope_x, giroscope_y, giroscope_z, magnetometer_x,
          magnetometer_y, magnetometer_z, temperature):
    """
    Builds the binary representation given the data
    """
    # First transform lat and lon into two dictionaries with sign,
    # exponent and mantissa
    lat, lon = map(
        lambda n: {'sign': n[0], 'exp': n[1], 'digits': n[2]},
        map(_frexp10, (lat, lon)))
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
        element = dict(element)
        element['lon'] = _make_float(**dict(element['lon']))
        element['lat'] = _make_float(**dict(element['lat']))
        yield element

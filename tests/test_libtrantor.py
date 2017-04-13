from trantor.format import _make_float, _frexp10
from trantor import parse, build


def test_split_float():
    assert _frexp10(0) == (0, 0, 0)
    assert _frexp10(1.2) == (0, 1, 12)
    assert _frexp10(10.23) == (0, 2, 1023)
    assert _frexp10(42.4242) == (0, 4, 424242)
    assert _frexp10(-90.234143) == (1, 6, 90234143)
    assert _frexp10(-0.232434143) == (1, 9, 232434143)


def test_make_float():
    assert _make_float(0, 0, 0) == 0
    assert _make_float(0, 1, 12) == 1.2
    assert _make_float(1, 1, 123) == -12.3
    assert _make_float(1, 4, 4124) == -0.4124
    assert _make_float(0, 0, 42424) == 42424


def test_make_float_frexp():
    number = -12.423456
    repr = (1, 6, 12423456)
    assert number == _make_float(*repr)
    assert repr == _frexp10(number)


def test_parse():
    binary_data = b'\x01\x00\x01\x00\xa0\x00\x00\x01\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'\
                  b'\x00\x01\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x01\x00\x01\x00\x01\x00\x01\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x01\x00\x01\x00\x01'
    expected_data_1 = {
        'acc_x': 0, 'acc_y': 1, 'acc_z': 1, 'barometer': 256, 'course': 0,
        'elevation': 0, 'fix': 0, 'geoid_height': 0, 'giroscope_x': 256,
        'giroscope_y': 0, 'giroscope_z': 0, 'hdop': 0, 'lat': -0.01,
        'lon': 0.0, 'magnetometer_x': 0, 'magnetometer_y': 0, 'magnetometer_z': 0,
        'pdop': 0, 'satellites': 0, 'speed': 0, 'tdop': 0, 'temperature': 0,
        'timestamp': 16777472, 'vdop': 0}
    expected_data_2 = {
        'acc_x': 0, 'acc_y': 0, 'acc_z': 0, 'barometer': 0, 'course': 0,
        'elevation': 1, 'fix': 0, 'geoid_height': 1, 'giroscope_x': 0,
        'giroscope_y': 0, 'giroscope_z': 0, 'hdop': 1, 'lat': 0.00, 'lon': 0.0,
        'magnetometer_x': 0, 'magnetometer_y': 1, 'magnetometer_z': 1, 'pdop': 0,
        'satellites': 1, 'speed': 0, 'tdop': 0, 'temperature': 1,
        'timestamp': 0, 'vdop': 0}
    parsed = list(parse(binary_data))
    assert len(parsed) == 2
    assert parsed[0] == expected_data_1
    assert parsed[1] == expected_data_2


def test_build():
    data = {
        'acc_x': 0, 'acc_y': 1, 'acc_z': 1, 'barometer': 256, 'course': 0,
        'elevation': 0, 'fix': 0, 'geoid_height': 0, 'giroscope_x': 256,
        'giroscope_y': 0, 'giroscope_z': 0, 'hdop': 0, 'lat': -0.1,
        'lon': 0.0, 'magnetometer_x': 0, 'magnetometer_y': 0,
        'magnetometer_z': 0, 'pdop': 0, 'satellites': 0, 'speed': 0,
        'tdop': 0, 'temperature': 0, 'timestamp': 16777472, 'vdop': 0}
    built = build(**data)
    binary_data = b'\x01\x00\x01\x00\x90\x00\x00\x01\x10\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'\
                  b'\x00\x01\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00'
    assert built == binary_data


def test_both():
    data = {
        'acc_x': 12, 'acc_y': 13, 'acc_z': 1, 'barometer': 25, 'course': 243,
        'elevation': 43, 'fix': 0, 'geoid_height': 12, 'giroscope_x': 256,
        'giroscope_y': 1, 'giroscope_z': 5, 'hdop': 12, 'lat': -12.134243,
        'lon': 43.123432, 'magnetometer_x': 4, 'magnetometer_y': 3,
        'magnetometer_z': 12, 'pdop': 3, 'satellites': 6, 'speed': 2,
        'tdop': 45, 'temperature': 12, 'timestamp': 16777472, 'vdop': 2}
    binary = build(**data)
    assert data == list(parse(binary))[0]

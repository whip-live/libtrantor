from trantor import parse, build


def test_parse():
    """
    Test parsing real world examples of binary data
    """
    binary_data = b'\n\x00\n\x00\xc0(C\xc9\xee\xcb\xfb\x16@E\xa9'\
                  b'\x99\x99\x99\x99\x9a\x00\x00\x00\x01\x00\x00'\
                  b'\x00\x02\x00\x00\x00\x0c\x01\x06\x00\x02\x00'\
                  b'\x02\x00\x01\x00\x01\x00\x00\x00{\x00\x01\x00'\
                  b'\x02\x00\x03\x00\x01\x00\x01\x00\x00\x08\x00'\
                  b'\x04\x00\x02\x00\x04\x00\x01\x00\x04'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00'\
                  b'\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00'\
                  b'\x01\x00\x01'
    expected_data_1 = {
        'acc_x': 1, 'acc_y': 2, 'acc_z': 3, 'barometer': 256, 'course': 1,
        'elevation': 12, 'fix': 1, 'geoid_height': 2, 'giroscope_x': 256,
        'giroscope_y': 8, 'giroscope_z': 4, 'hdop': 2, 'lat': -12.1324,
        'lon': 43.325, 'magnetometer_x': 2, 'magnetometer_y': 4,
        'magnetometer_z': 1, 'pdop': 1, 'satellites': 6, 'speed': 123,
        'tdop': 1, 'temperature': 4, 'timestamp': 16777472, 'vdop': 2}
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
    """
    Test building real world examples of binary data
    """
    data = {
        'acc_x': 1, 'acc_y': 2, 'acc_z': 3, 'barometer': 256, 'course': 1,
        'elevation': 12, 'fix': 1, 'geoid_height': 2, 'giroscope_x': 256,
        'giroscope_y': 8, 'giroscope_z': 4, 'hdop': 2, 'lat': -12.1324,
        'lon': 43.325, 'magnetometer_x': 2, 'magnetometer_y': 4,
        'magnetometer_z': 1, 'pdop': 1, 'satellites': 6, 'speed': 123,
        'tdop': 1, 'temperature': 4, 'timestamp': 16777472, 'vdop': 2}
    built = build(**data)
    print(built)
    binary_data = b'\n\x00\n\x00\xc0(C\xc9\xee\xcb\xfb\x16@E\xa9'\
                  b'\x99\x99\x99\x99\x9a\x00\x00\x00\x01\x00\x00'\
                  b'\x00\x02\x00\x00\x00\x0c\x01\x06\x00\x02\x00'\
                  b'\x02\x00\x01\x00\x01\x00\x00\x00{\x00\x01\x00'\
                  b'\x02\x00\x03\x00\x01\x00\x01\x00\x00\x08\x00'\
                  b'\x04\x00\x02\x00\x04\x00\x01\x00\x04'
    assert built == binary_data


def test_both():
    """
    Test that parsed built data returns the original value
    """
    data = {
        'acc_x': 12, 'acc_y': 13, 'acc_z': 1, 'barometer': 25, 'course': 243,
        'elevation': 43, 'fix': 0, 'geoid_height': 12, 'giroscope_x': 256,
        'giroscope_y': 1, 'giroscope_z': 5, 'hdop': 12, 'lat': -12.134243,
        'lon': 43.123432, 'magnetometer_x': 4, 'magnetometer_y': 3,
        'magnetometer_z': 12, 'pdop': 3, 'satellites': 6, 'speed': 2,
        'tdop': 45, 'temperature': 12, 'timestamp': 1677747.2, 'vdop': 2}
    binary = build(**data)
    assert data == list(parse(binary))[0]

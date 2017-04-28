from trantor import parse, build
from datetime import datetime, timedelta, timezone


def test_parse():
    """
    Test parsing real world examples of binary data
    """
    binary_data = b'Y\x02\x17X\x0cd,\x8d\x0f\xa6@w\xa5\\^>\xda=BZY'\
                  b'\x02\x17X\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00N \xc0(C\xc9\xee\xcb\xfb\x16@E\xa9'\
                  b'\x99\x99\x99\x99\x9a\x00\x00\x00\x01'\
                  b'\x00\x00\x00\x02\x00\x00\x00\x0c\x01\x06'\
                  b'\x00\x02\x00\x02\x00\x01\x00\x01\x00\x00'\
                  b'\x00{\x00\x01\x00\x02\x00\x03\x00\x01\x00'\
                  b'\x01\x00\x00\x08\x00\x04\x00\x02\x00\x04'\
                  b'\x00\x01\x00\x04\x00\x00\x01'\
                  b'\x00\x00u0\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00'\
                  b'\x01\x00\x01\x00\x01\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x01\x00\x01\x00\x01\x00\x00'\
                  b'\x02'
    expected_data_1 = {
        'acc_x': 1, 'acc_y': 2, 'acc_z': 3, 'barometer': 256, 'course': 1,
        'elevation': 12, 'fix': 1, 'geoid_height': 2, 'giroscope_x': 256,
        'giroscope_y': 8, 'giroscope_z': 4, 'hdop': 0.02, 'lat': -12.1324,
        'lon': 43.325, 'magnetometer_x': 2, 'magnetometer_y': 4,
        'magnetometer_z': 1, 'pdop': 0.01, 'satellites': 6, 'speed': 123,
        'timestamp': datetime(2017, 4, 27, 16, 8, 12, tzinfo=timezone.utc),
        'tdop': 1, 'temperature': 4, 'vdop': 0.02, 'sequence_id': 1}
    expected_data_2 = {
        'acc_x': 0, 'acc_y': 0, 'acc_z': 0, 'barometer': 0, 'course': 0,
        'elevation': 1, 'fix': 0, 'geoid_height': 1, 'giroscope_x': 0,
        'giroscope_y': 0, 'giroscope_z': 0, 'hdop': 0.01, 'lat': 0.00, 'lon': 0.0,
        'magnetometer_x': 0, 'magnetometer_y': 1, 'magnetometer_z': 1, 'pdop': 0,
        'satellites': 1, 'speed': 0, 'tdop': 0, 'temperature': 1,
        'timestamp': datetime(2017, 4, 27, 16, 8, 22, tzinfo=timezone.utc),
        'vdop': 0, 'sequence_id': 2}
    parsed = parse(binary_data)
    assert parsed['timestamp'] == datetime(2017, 4, 27, 16, 7, 52, tzinfo=timezone.utc)
    assert parsed['gps_timestamp'] == datetime(2017, 4, 27, 16, 7, 52, tzinfo=timezone.utc)
    assert parsed['configuration'] == 0
    assert parsed['segment_id'] == '0c642c8d-0fa6-4077-a55c-5e3eda3d425a'
    assert len(parsed['points']) == 2
    assert parsed['points'][0] == expected_data_1
    assert parsed['points'][1] == expected_data_2


def test_build():
    """
    Test building real world examples of binary data
    """
    time1 = datetime(2016, 1, 1, tzinfo=timezone.utc)
    time2 = time1 + timedelta(milliseconds=1231241)
    data = {
        'timestamp': time1, 'gps_timestamp': time1,
        'segment_id': '7940793d-227b-4247-b8f2-663846f3aa01', 'configuration': 0,
        'points': [
            {
                'acc_x': 1, 'acc_y': 2, 'acc_z': 3, 'barometer': 256, 'course': 1,
                'elevation': 12, 'fix': 1, 'geoid_height': 2, 'giroscope_x': 256,
                'giroscope_y': 8, 'giroscope_z': 4, 'hdop': 0.02, 'lat': -12.1324,
                'lon': 43.325, 'magnetometer_x': 2, 'magnetometer_y': 4,
                'magnetometer_z': 1, 'pdop': 0.01, 'satellites': 6, 'speed': 123,
                'tdop': 1, 'temperature': 4, 'timestamp': time2,
                'vdop': 0.02, 'sequence_id': 1}]}
    built = build(**data)
    binary_data = b'V\x85\xc1\x80y@y="{BG\xb8\xf2f8F\xf3\xaa\x01V\x85\xc1\x80'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                  b'\x00\x00\x00\x00\x00\x12\xc9\x89\xc0(C\xc9'\
                  b'\xee\xcb\xfb\x16@E\xa9\x99\x99\x99\x99\x9a'\
                  b'\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00'\
                  b'\x00\x0c\x01\x06\x00\x02\x00\x02\x00\x01'\
                  b'\x00\x01\x00\x00\x00{\x00\x01\x00\x02\x00'\
                  b'\x03\x00\x01\x00\x01\x00\x00\x08\x00\x04'\
                  b'\x00\x02\x00\x04\x00\x01\x00\x04\x00\x00\x01'
    assert built == binary_data


def test_both():
    """
    Test that parsed built data returns the original value
    """
    time1 = datetime(2016, 1, 1, tzinfo=timezone.utc)
    time2 = time1 + timedelta(milliseconds=1231241)
    data = {
        'timestamp': time1, 'gps_timestamp': time1,
        'segment_id': '7940793d-227b-4247-b8f2-663846f3aa01', 'configuration': 0,
        'points': [
            {
                'acc_x': 12, 'acc_y': 13, 'acc_z': 1, 'barometer': 25, 'course': 243,
                'elevation': 43, 'fix': 0, 'geoid_height': 12, 'giroscope_x': 256,
                'giroscope_y': 1, 'giroscope_z': 5, 'hdop': 12, 'lat': -12.134243,
                'lon': 43.123432, 'magnetometer_x': 4, 'magnetometer_y': 3,
                'magnetometer_z': 12, 'pdop': 3, 'satellites': 6, 'speed': 2,
                'tdop': 45, 'temperature': 12, 'timestamp': time2,
                'vdop': 2, 'sequence_id': 1}]}
    # Make a deep copy of the data dict to avoid changing it
    binary = build(**data)
    assert data == parse(binary)

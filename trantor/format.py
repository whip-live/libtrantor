import copy
import uuid

from construct import Struct, Int, Short, Int24ub, Byte, Double, BytesInteger
from datetime import datetime, timedelta


# Metadata structure
MetaData = Struct(
    'timestamp' / Int,
    'segment_id' / BytesInteger(16),
    'gps_timestamp' / Int,
    'configuration' / BytesInteger(104),
)

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
    'sequence_id' / Int24ub,
)


def build(timestamp, gps_timestamp, segment_id, configuration, points):
    """
    Builds the binary representation given the data
    """
    metadata = MetaData.build(dict(
        timestamp=int(timestamp.timestamp()),
        gps_timestamp=int(gps_timestamp.timestamp()),
        segment_id=uuid.UUID(segment_id).int, configuration=configuration))

    recording_lines = b''
    points = copy.deepcopy(points)
    for point in points:
        # Timestamp should be a datetime object
        point['timestamp'] = int((point['timestamp'] - timestamp).total_seconds() * 1000)
        recording_lines += RecordingLine.build(point)
    return metadata + recording_lines


def parse(binary_data):
    """
    Takes a binary string as input, parse it, and yields one result at a time
    """
    metadata, recording_lines = binary_data[:128], binary_data[128:]

    parsed_metadata = MetaData.parse(metadata)
    start_time = datetime.fromtimestamp(parsed_metadata['timestamp'])

    # Elaborate parsed_metadata
    parsed_metadata['timestamp'] = datetime.fromtimestamp(parsed_metadata['timestamp'])
    parsed_metadata['gps_timestamp'] = datetime.fromtimestamp(parsed_metadata['gps_timestamp'])
    parsed_metadata['segment_id'] = '%s' % uuid.UUID(int=parsed_metadata['segment_id'])

    parsed_recording_lines = RecordingLine[:].parse(recording_lines)
    points = []
    for i, element in enumerate(parsed_recording_lines, 1):
        row = dict(element)
        row['timestamp'] = start_time + timedelta(milliseconds=row['timestamp'])
        # Add a sequence id, starting from 1
        row['sequence_id'] = i
        points.append(row)

    return {**parsed_metadata, 'points': points}

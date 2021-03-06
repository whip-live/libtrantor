import copy
import uuid

from construct import Struct, Int, Short, Int24ub, Byte, Double, BytesInteger
from datetime import datetime, timedelta, timezone
from decimal import Decimal


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
        # TODO: Maybe use some decimal method to cast to int
        point['hdop'] = int((Decimal(point['hdop']) * 100).to_integral_value())
        point['pdop'] = int((Decimal(point['pdop']) * 100).to_integral_value())
        point['vdop'] = int((Decimal(point['vdop']) * 100).to_integral_value())
        point['elevation'] = int((Decimal(point['elevation']) * 10).to_integral_value())
        point['course'] = int((Decimal(point['course']) * 10).to_integral_value())
        point['geoid_height'] = int((Decimal(point['geoid_height']) * 10).to_integral_value())
        point['speed'] = int((Decimal(point['speed']) * 10).to_integral_value())
        recording_lines += RecordingLine.build(point)
    return metadata + recording_lines


def parse(binary_data):
    """
    Takes a binary string as input, parse it, and yields one result at a time
    """
    metadata, recording_lines = binary_data[:128], binary_data[128:]

    parsed_metadata = MetaData.parse(metadata)
    start_time = datetime.fromtimestamp(parsed_metadata['timestamp'], timezone.utc)

    # Elaborate parsed_metadata
    parsed_metadata['timestamp'] = datetime.fromtimestamp(parsed_metadata['timestamp'], timezone.utc)
    parsed_metadata['gps_timestamp'] = datetime.fromtimestamp(parsed_metadata['gps_timestamp'], timezone.utc)
    parsed_metadata['segment_id'] = '%s' % uuid.UUID(int=parsed_metadata['segment_id'])

    parsed_recording_lines = RecordingLine[:].parse(recording_lines)
    points = []
    for i, element in enumerate(parsed_recording_lines, 1):
        row = dict(element)
        row['timestamp'] = start_time + timedelta(milliseconds=row['timestamp'])
        # Add a sequence id, starting from 1
        row['sequence_id'] = i
        # Convert to float
        row['hdop'] /= 100
        row['pdop'] /= 100
        row['vdop'] /= 100
        row['elevation'] /= 10
        row['course'] /= 10
        row['geoid_height'] /= 10
        row['speed'] /= 10
        points.append(row)

    return {**parsed_metadata, 'points': points}

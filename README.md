# libtrantor
A library to parse and build the binary format coming from LIVEX

# Installation

Through Pip:

```bash
    $ pip install -e git+git@github.com:whip-live/libtrantor.git#egg=libtrantor
```

Or clone the repo and install it:

```bash
    $ git clone git@github.com:whip-live/libtrantor.git
    $ pip install ./libtrantor/
```

# Usage

## Parse

```python
    from trantor import parse
    print(list(parse(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                     b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                     b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                     b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
                     b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')))
```

## Build
```python
    from trantor import build
    data = {
        'acc_x': 0, 'acc_y': 0, 'acc_z': 0, 'barometer': 0, 'course': 0,
        'elevation': 0, 'fix': 0, 'geoid_height': 0, 'giroscope_x': 0,
        'giroscope_y': 0, 'giroscope_z': 0, 'hdop': 0, 'lat': 0.0,
        'lon': 0.0, 'magnetometer_x': 0, 'magnetometer_y': 0,
        'magnetometer_z': 0, 'pdop': 0, 'satellites': 0, 'speed': 0,
        'tdop': 0, 'temperature': 0, 'timestamp': 0, 'vdop': 0}
    print(build(**data))
```

# Data format

A single record is composed of a total of 55bytes divided like this:

| field            | type                             |
| ---------------- | -------------------------------- |
| `timestamp`      | 32 bits unsigned integer         |
| `lat`            | 32 bits custom float (see below) |
| `lon`            | 32 bits custom float (see below) |
| `course`         | 16 bits unsigned integer         |
| `geoid_height`   | 16 bits unsigned integer         |
| `elevation`      | 16 bits unsigned integer         |
| `fix`            | 8 bits unsigned integer          |
| `satellites`     | 8 bits unsigned integer          |
| `hdop`           | 16 bits unsigned integer         |
| `vdop`           | 16 bits unsigned integer         |
| `pdop`           | 16 bits unsigned integer         |
| `tdop`           | 16 bits unsigned integer         |
| `speed`          | 32 bits unsigned integer         |
| `acc_x`          | 16 bits unsigned integer         |
| `acc_y`          | 16 bits unsigned integer         |
| `acc_z`          | 16 bits unsigned integer         |
| `barometer`      | 24 bits unsigned integer         |
| `giroscope_x`    | 16 bits unsigned integer         |
| `giroscope_y`    | 16 bits unsigned integer         |
| `giroscope_z`    | 16 bits unsigned integer         |
| `magnetometer_x` | 16 bits unsigned integer         |
| `magnetometer_y` | 16 bits unsigned integer         |
| `magnetometer_x` | 16 bits unsigned integer         |
| `temperature`    | 16 bits unsigned integer         |

The custom float structure is used to represent latitude and longitude,
and it is defined as following:

| field     | type           |
| --------- | -------------- |
| `sign`    | single bit     |
| `exp`     | 3 bits integer |
| `digits`  | 28 bits integer|

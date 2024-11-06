# Camera Provider

This package contains the necessary classes and functions to receive camera frames from a Netgear sender.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Classes](#classes)
- [Functions](#functions)

## Installation

To install the package, use the following command:

```bash
pip install camera-provider
```

## Usage

Import the package and use the provided classes and functions to receive camera frames:

```python
from camera_provider import CameraReceiver

receiver = CameraReceiver()
receiver.start_receiving()
```

## Classes

### `CameraReceiver`

- **Description**: Class to handle receiving camera frames.
- **Methods**:
    - `start_receiving()`: Starts receiving frames.
    - `stop_receiving()`: Stops receiving frames.

## Functions

- **`process_frame(frame)`**: Processes a received frame.
    - **Parameters**: `frame` - The frame to process.
    - **Returns**: Processed frame data.


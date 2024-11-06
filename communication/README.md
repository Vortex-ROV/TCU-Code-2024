# Communication Provider for TCUevo ROV

This package contains the necessary classes and functions to send control commands to the Pixhawk using MAVProxy on the ROV.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Classes](#classes)
- [Functions](#functions)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install the package, clone the repository and install the dependencies:

```bash
git clone https://github.com/your-repo/TCUevo-Code.git
cd TCUevo-Code/src/app/provider/communication
pip install -r requirements.txt
```

## Usage

Import the necessary classes and functions in your project:

```python
from communication import PixhawkController

# Initialize the controller
controller = PixhawkController()

# Send a control command
controller.send_command('command')
```

## Classes

### `PixhawkController`

- **Description**: Handles the communication with the Pixhawk using MAVProxy.
- **Methods**:
    - `__init__()`: Initializes the controller.
    - `send_command(command: str)`: Sends a control command to the Pixhawk.

## Functions

- **`connect_to_pixhawk()`**: Establishes a connection to the Pixhawk.
- **`disconnect_from_pixhawk()`**: Closes the connection to the Pixhawk.

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) first.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
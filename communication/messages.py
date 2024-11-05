import unittest
import struct


class Message:
    """
    Class for abstracting the message sent from the TCU to the ROV companion computer
    """

    def __init__(self, msg=b"") -> None:
        # default message
        self.__msg = {
            "throttle": 1500,
            "yaw": 1500,
            "forward": 1500,
            "lateral": 1500,
            "gripper_1": False,
            "gripper_2": False,
            "light": "0",
            "rotating_gripper": "O",
            "armed": False,
            "flight_mode": "M",
            "joystick_connect": False,
        }

        self.recreate_msg(msg)
    
    def recreate_msg(self, msg: bytes) -> None:
        # recreate dictionary using provided bytes of message
        if msg != b"":
            index = 0
            for key in self.__msg.keys():
                if isinstance(self.__msg[key], int):
                    self.__msg[key] = int.from_bytes(msg[index : index + 4], "big")
                    index += 4
                elif isinstance(self.__msg[key], float):
                    self.__msg[key] = struct.unpack("d", msg[index : index + 8])[0]
                    index += 8
                elif isinstance(self.__msg[key], str):
                    self.__msg[key] = "".join(
                        map(chr, msg[index : index + len(self.__msg[key])])
                    )
                    index += len(self.__msg[key])
                elif isinstance(self.__msg[key], bool):
                    self.__msg[key] = bool.from_bytes(msg[index], "big")
                    index += 1
                else:
                    raise Exception("Unrecognised data type")

    def bytes(self) -> bytes:
        """
        Get the bytes representation of the message to be sent through the socket
        """
        b = b""
        for key in self.__msg.keys():
            if isinstance(self.__msg[key], int):
                b += self.__msg[key].to_bytes(4, "big")
            elif isinstance(self.__msg[key], float):
                b += struct.pack("d", self.__msg[key])
            elif isinstance(self.__msg[key], str):
                b += self.__msg[key].encode()
            elif isinstance(self.__msg[key], bool):
                b += self.__msg[key].to_bytes(1, "big")
            else:
                raise Exception("Unrecognised data type")
        return b

    def get_value(self, key):
        """
        Get the value of a key from the message dictionary
        """
        return self.__msg[key]

    def set_value(self, key, value) -> None:
        """
        Set the value of a key in the message dictionary

        ### Notes:
            - Can not create new keys in the dictionary
            - Can only override message values with values of the same type
            - Can only override string type message values with those of the same length
        """
        if (
            key in self.__msg
            and type(self.__msg[key]) == type(value)
            and (
                type(value) == str
                and len(value) == len(self.__msg[key])
                or type(value) != str
            )
        ):
            self.__msg[key] = value
        else:
            raise ValueError()

    def __eq__(self, value) -> bool:
        return self.__msg == value.__msg

    def __str__(self) -> str:
        return str(self.__msg)
    

class SensorMessage(Message):
    def __init__(self, msg=b"") -> None:
        self._msg = {
            "pressure": 0.0,
            "temperature": 0.0,
            "depth": 0.0,
            "heading": 0
        }

        self.recreate_msg(msg)


class Test(unittest.TestCase):
    def test_msg(self):
        encoded_msg = Message()

        encoded_msg.set_value("throttle", 1600)
        encoded_msg.set_value("yaw", 1600)
        encoded_msg.set_value("forward", 1400)
        encoded_msg.set_value("lateral", 1200)

        encoded_msg.set_value("gripper_1", True)
        encoded_msg.set_value("gripper_2", False)
        encoded_msg.set_value("light", "H")
        encoded_msg.set_value("rotating_gripper", "L")

        encoded_msg.set_value("armed", True)
        encoded_msg.set_value("flight_mode", "S")
        encoded_msg.set_value("joystick_connect", True)

        decoded_msg = Message(encoded_msg.bytes())
        self.assertEqual(decoded_msg, encoded_msg)


if __name__ == "__main__":
    unittest.main()

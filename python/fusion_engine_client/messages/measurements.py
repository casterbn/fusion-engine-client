import numpy as np

from .defs import *


class IMUMeasurement:
    """!
    @brief IMU sensor measurement data.
    """
    MESSAGE_TYPE = MessageType.IMU_MEASUREMENT

    _FORMAT = '<3d 3d 3d 3d'
    _SIZE: int = struct.calcsize(_FORMAT)

    def __init__(self):
        self.p1_time = Timestamp()

        self.accel_mps2 = np.full((3,), np.nan)
        self.accel_std_mps2 = np.full((3,), np.nan)

        self.gyro_rps = np.full((3,), np.nan)
        self.gyro_std_rps = np.full((3,), np.nan)

    def pack(self, buffer: bytes = None, offset: int = 0, return_buffer: bool = True) -> (bytes, int):
        if buffer is None:
            buffer = bytes(self.calcsize())

        initial_offset = offset

        offset += self.p1_time.pack(buffer, offset, return_buffer=False)

        struct.pack_into(IMUMeasurement._FORMAT, buffer, offset,
                         *self.accel_mps2,
                         *self.accel_std_mps2.flat,
                         *self.gyro_rps,
                         *self.gyro_std_rps)
        offset += IMUMeasurement._SIZE

        if return_buffer:
            return buffer
        else:
            return offset - initial_offset

    def unpack(self, buffer: bytes, offset: int = 0) -> int:
        initial_offset = offset

        offset += self.p1_time.unpack(buffer, offset)

        MessageHeader.unpack_values(IMUMeasurement._FORMAT, buffer, offset,
                                    self.accel_mps2,
                                    self.accel_std_mps2,
                                    self.gyro_rps,
                                    self.gyro_std_rps)
        offset += IMUMeasurement._SIZE

        return offset - initial_offset

    @classmethod
    def calcsize(cls) -> int:
        return Timestamp.calcsize() + IMUMeasurement._SIZE

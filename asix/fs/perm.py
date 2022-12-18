from enum import IntFlag


__all__ = ["FSPerm"]


class FSPerm(IntFlag):
    NONE = 0b000
    R = 0b100
    W = 0b010
    X = 0b001
    RW = 0b110
    RX = 0b101
    WX = 0b011
    RWX = 0b111

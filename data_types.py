import struct
from pygame.math import Vector2 as vec2
# H - uint16, h - int16, I - uint32, i - int32, B - uint8, b - int8, c - char

class Thing:
    # 10 bytes
    __slots__= [
        'pos', # pos.x, pos.y - 4h
        'angle', # 2h
        'type', # 2H
        'flags', # 2H
    ]

    @classmethod
    def from_bytes(cls, data):
        x, y, angle, type_, flags = struct.unpack('<3h2H', data)
        obj = cls()
        obj.pos = vec2(x, y)
        obj.angle = angle
        obj.type = type_
        obj.flags = flags
        return obj

class Segment:
    # 12 bytes = 2h x 6
    __slots__ = [
        'start_vertex_id',
        'end_vertex_id',
        'angle',
        'linedef_id',
        'direction',
        'offset',
    ]
    __slots__ += ['start_vertex', 'end_vertex', 'linedef']

    @classmethod
    def from_bytes(cls, data):
        # 2h x 6 = 12 bytes
        fields = struct.unpack('6h', data)
        obj = cls()
        (
            obj.start_vertex_id,
            obj.end_vertex_id,
            obj.angle,
            obj.linedef_id,
            obj.direction,
            obj.offset,
        ) = fields
        return obj

class SubSector:
    # 4 bytes = 2h + 2h
    __slots__ = [
        'seg_count',
        'first_seg_id',
    ]

    @classmethod
    def from_bytes(cls, data):
        # 2h + 2h = 4 bytes
        fields = struct.unpack('2h', data)
        obj = cls()
        (
            obj.seg_count,
            obj.first_seg_id,
        ) = fields
        return obj

class Node:
    # 28 bytes = 2h x 12 + 2H x 2
    class BBox:
        __slots__ = ['top', 'bottom', 'left', 'right']

    __slots__ = [
        'x_partition',
        'y_partition',
        'dx_partition',
        'dy_partition',
        'bbox', # 8h
        'front_child_id',
        'back_child_id',
    ]
    def __init__(self):
        self.bbox = {'front': self.BBox(), 'back': self.BBox()}

    @classmethod
    def from_bytes(cls, data):
        # 4h (partition) + 8h (bbox) + 2H (child ids) = 28 bytes
        fields = struct.unpack('4h8h2H', data)
        obj = cls()
        (
            obj.x_partition,
            obj.y_partition,
            obj.dx_partition,
            obj.dy_partition,
            front_top, front_bottom, front_left, front_right,
            back_top, back_bottom, back_left, back_right,
            obj.front_child_id,
            obj.back_child_id,
        ) = fields
        obj.bbox['front'].top = front_top
        obj.bbox['front'].bottom = front_bottom
        obj.bbox['front'].left = front_left
        obj.bbox['front'].right = front_right
        obj.bbox['back'].top = back_top
        obj.bbox['back'].bottom = back_bottom
        obj.bbox['back'].left = back_left
        obj.bbox['back'].right = back_right
        return obj

class Linedef:
    #14 bytes = 2H X 7
    __slots__ = [
        'start_vertex_id',
        'end_vertex_id',
        'flags',
        'line_type',
        'sector_tag',
        'front_sidedef_id',
        'back_sidedef_id',
    ]

    @classmethod
    def from_bytes(cls, data):
        import struct
        fields = struct.unpack('7H', data)
        obj = cls()
        (
            obj.start_vertex_id,
            obj.end_vertex_id,
            obj.flags,
            obj.line_type,
            obj.sector_tag,
            obj.front_sidedef_id,
            obj.back_sidedef_id,
        ) = fields
        return obj
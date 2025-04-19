import struct
from data_types import *
from pygame.math import Vector2 as vec2

class WADReader:
    def __init__(self, wad_path):
        self.wad_file = open(wad_path, 'rb')
        self.header = self.read_header()
        self.directory = self.read_directory()

    def read_thing(self, offset):
        # 10 bytes = 2h x 5
        self.wad_file.seek(offset)
        data_bytes = self.wad_file.read(10)
        return Thing.from_bytes(data_bytes)

    def read_segment(self, offset):
        # 12 bytes = 2h x 6
        self.wad_file.seek(offset)
        data_bytes = self.wad_file.read(12)
        return Segment.from_bytes(data_bytes)
    
    def read_sector(self, offset):
        # 26 bytes = 2h + 2h + 8c + 8c + 2H x 3
        self.wad_file.seek(offset)
        data_bytes = self.wad_file.read(26)
        return Sector.from_bytes(data_bytes)

    def read_sub_sector(self, offset):
        # 4 bytes = 2h + 2h
        self.wad_file.seek(offset)
        data_bytes = self.wad_file.read(4)
        return SubSector.from_bytes(data_bytes)
    
    def read_sidedef(self, offset):
        # 30 bytes = 2h + 2h + 8c + 8c + 8c + 2H
        self.wad_file.seek(offset)
        data_bytes = self.wad_file.read(30)
        return Sidedef.from_bytes(data_bytes)

    def read_nodes(self, offset):
        # 28 bytes = 2h x 12 + 2H x 2
        self.wad_file.seek(offset)
        data_bytes = self.wad_file.read(28)
        return Node.from_bytes(data_bytes)
    
    def read_linedef(self, offset):
        # 14 bytes = 2H X 7
        self.wad_file.seek(offset)
        data_bytes = self.wad_file.read(14)
        return Linedef.from_bytes(data_bytes)

    def read_vertex(self, offset):
        # 4 bytes = 2h, 2h
        x = self.read_2_bytes(offset=offset, byte_format='h')
        y = self.read_2_bytes(offset=offset + 2, byte_format='h')
        return vec2(x, y)

    def read_directory(self):
        directory = []
        for i in range(self.header['lump_count']):
            offset = self.header['init_offset'] + i * 16
            lump_info = {
                'lump_offset': self.read_4_bytes(offset=offset),
                'lump_size': self.read_4_bytes(offset=offset + 4),
                'lump_name': self.read_string(offset=offset + 8, num_bytes=8),
            }
            directory.append(lump_info)
        return directory
            
    def read_header(self):
        return {
            'wad_type': self.read_string(offset=0, num_bytes=4),
            'lump_count': self.read_4_bytes(offset=4),
            'init_offset': self.read_4_bytes(offset=8),
        }
    
    def read_1_byte(self, offset, byte_format='B'):
        # B - uint8, b - int8
        return self.read_bytes(offset=offset, num_bytes=1, byte_format=byte_format)[0]
    
    def read_2_bytes(self, offset, byte_format):
        # H - uint16, h - int16
        return self.read_bytes(offset=offset, num_bytes=2, byte_format=byte_format)[0]

    def read_4_bytes(self, offset, byte_format='i'):
        # I - uint32, i - int32
        return self.read_bytes(offset=offset, num_bytes=4, byte_format=byte_format)[0]
    
    def read_string(self, offset, num_bytes):
        # c - char
        return ''.join(b.decode('ascii') for b in 
                       self.read_bytes(offset, num_bytes, byte_format='c' * num_bytes)
                       if ord(b) != 0).upper()

    def read_bytes(self, offset, num_bytes, byte_format):
        self.wad_file.seek(offset)
        buffer = self.wad_file.read(num_bytes)
        return struct.unpack(byte_format, buffer)
    
    def close(self):
        self.wad_file.close()
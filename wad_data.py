from wad_reader import WADReader

class WADData:
    LUMP_INDICES = {
        'THINGS': 1,
        'LINEDEFS': 2,
        'SIDEDEFS': 3,
        'VERTICES': 4,
        'SEGS': 5,
        'SSECTORS': 6,
        'NODES': 7,
        'SECTORS': 8,
        'REJECT': 9,
        'BLOCKMAP': 10
    }

    def __init__(self, engine, map_name='E1M1'):
        self.reader = WADReader(engine.wad_path)
        self.map_index = self.get_lump_index(lump_name=map_name)

        self.vertices = self.get_lump_data(
            reader_func=self.reader.read_vertex,
            lump_index=self.map_index + self.LUMP_INDICES['VERTICES'],
            num_bytes=4
        )
        self.linedefs = self.get_lump_data(
            reader_func=self.reader.read_linedef,
            lump_index=self.map_index + self.LUMP_INDICES['LINEDEFS'],
            num_bytes=14
        )
        self.nodes = self.get_lump_data(
            reader_func=self.reader.read_nodes,
            lump_index=self.map_index + self.LUMP_INDICES['NODES'],
            num_bytes=28
        )
        self.sub_sectors = self.get_lump_data(
            reader_func=self.reader.read_sub_sector,
            lump_index=self.map_index + self.LUMP_INDICES['SSECTORS'],
            num_bytes=4
        )
        self.segments = self.get_lump_data(
            reader_func=self.reader.read_segment,
            lump_index=self.map_index + self.LUMP_INDICES['SEGS'],
            num_bytes=12
        )
        self.things = self.get_lump_data(
            reader_func=self.reader.read_thing,
            lump_index=self.map_index + self.LUMP_INDICES['THINGS'],
            num_bytes=10
        )

        self.update_data()
        self.reader.close()

    def update_data(self):
        self.update_segs()

    def update_segs(self):
        for seg in self.segments:
            seg.start_vertex = self.vertices[seg.start_vertex_id]
            seg.end_vertex = self.vertices[seg.end_vertex_id]
            seg.linedef = self.linedefs[seg.linedef_id]

            # convert angles from BAMS to degrees
            seg.angle = (seg.angle << 16) * 8.38190317e-8
            seg.angle = seg.angle + 370 if seg.angle < 0 else seg.angle

    @staticmethod
    def print_attrs(obj):
        print()
        for attr in obj.__slots__:
            print(eval(f'obj.{attr}'), end=' ')


    def get_lump_data(self, reader_func, lump_index, num_bytes, header_length=0):
        lump_info = self.reader.directory[lump_index]
        count = lump_info['lump_size'] // num_bytes
        data = []
        for i in range(count):
            offset = lump_info['lump_offset'] + i * num_bytes + header_length
            data.append(reader_func(offset))
        return data
    
    def get_lump_index(self, lump_name):
        for idx, lump in enumerate(self.reader.directory):
            if lump['lump_name'] == lump_name:
                return idx
        raise ValueError(f"Lump '{lump_name}' not found in WAD file.")
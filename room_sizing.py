# room calculator to find the total number of pieces to build a cuboid, and the total internal volume
# use this to plan out materials needed to build a room to fit a machine
# or to figure out materials for whatever cuboid room you want to build


def room_calculation(width: int, length: int, height: int):
    top_and_bottom = 2 * (width * length)
    left_and_right = 2 * (length * height)
    front_and_back = 2 * (width * height)
    length_edges = 4 * length
    width_edges = 4 * width
    height_edges = 4 * height
    corners = 8
    pieces = sum(
        [
            top_and_bottom,
            left_and_right,
            front_and_back,
            length_edges,
            width_edges,
            height_edges,
            corners,
        ]
    )
    volume = width * length * height
    print(
        f"{width}x{length}x{height} gives {volume}m3 using {pieces} blocks. {volume/pieces:.2f} m3/p"
    )
    return volume, pieces


# extends room calculator to a multi-floor building
def building_calculation(floors: int, width: int, length: int, height: int):
    # start with calcs for each floor
    floor_volume, floor_pieces = room_calculation(width, length, height)
    # total volume is just the sum of all volumes
    total_volume = floor_volume * floors
    # pieces has to account for ceiling/floor overlap
    area = width * length
    overlaps = floors - 1
    overlap_pieces = overlaps * area
    total_pieces = floor_pieces * floors - overlap_pieces
    print(
        f"{width}x{length}x{height}x{floors} gives {total_volume}m3 using {total_pieces} blocks. {total_volume/total_pieces:.2f} m3/p"
    )


### How I was using this when playing...

_ = room_calculation(3, 3, 2)

building_calculation(1, 18, 18, 3)  # 0.95
building_calculation(2, 18, 18, 3)  # 1.12
building_calculation(3, 18, 18, 3)  # 1.20
building_calculation(4, 18, 18, 3)  # 1.24

building_calculation(1, 13, 13, 3)  # 0.85
building_calculation(2, 13, 13, 3)  # 0.99
building_calculation(3, 13, 13, 3)  # 1.05
building_calculation(4, 13, 13, 3)  # 1.08

building_calculation(1, 8, 8, 3)  # 0.62
building_calculation(2, 8, 8, 3)  # 0.70
building_calculation(3, 8, 8, 3)  # 0.72
building_calculation(4, 8, 8, 3)  # 0.74

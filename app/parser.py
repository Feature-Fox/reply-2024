def parse_file(filename):
    with open(filename, 'r', encoding='utf-8-sig') as file:
        lines = file.readlines()

    # Extracting the first line which contains the grid info and point/tile counts
    grid_info = list(map(int, lines[0].split()))
    W, H, GN, SM, TL = grid_info

    # Initializing variables to store the parsed data
    golden_points = []
    silver_points = []
    tiles = []

    # Parsing Golden Points
    for i in range(1, 1 + GN):
        x, y = map(int, lines[i].split())
        golden_points.append((x, y))

    # Parsing Silver Points
    for i in range(1 + GN, 1 + GN + SM):
        x, y, score = map(int, lines[i].split())
        silver_points.append((x, y, score))

    # Parsing Tile information
    for i in range(1 + GN + SM, 1 + GN + SM + TL):
        tile_id, tile_cost, num_tiles = lines[i].split()
        tiles.append((tile_id, int(tile_cost), int(num_tiles)))

    grid = {
        'grid_width': W,
        'grid_height': H,
        'golden_points': golden_points,
        'silver_points': silver_points,
        'tiles': tiles,
    }

    return grid

def visualize_grid(parsed_data, path=None):
    width, height = parsed_data['grid_width'], parsed_data['grid_height']
    golden_points = parsed_data['golden_points']
    silver_points = {tuple(point[:2]): point[2] for point in parsed_data['silver_points']}

    grid = [['.' for _ in range(width)] for _ in range(height)]

    for x, y in golden_points:
        grid[y][x] = 'G'

    for (x, y), score in silver_points.items():
        grid[y][x] = 'S'

    if path:
        for tile_id, x, y in path:
            grid[y][x] = 'T'

    for row in grid:
        print(' '.join(row))

from typing import List, Union

from TilingLib import workspace_init, initializer, PATHS
from PIL import Image
from random import randint


def composer(files: List[str], tile_count: int, border_color, border_thickness: int) -> None:
    width_count, height_count = tile_count, tile_count
    workspace, image_is_square, image_width, image_height, border_color = workspace_init(files[0], border_color,
                                                                                         tile_count, border_thickness,
                                                                                         0)

    previous_tile_identificators: List[Union[str, int]] = ["", -1]
    current_tile_identificators: List[Union[str, int]] = ["", -1]
    previous_col_identificators: List[List[Union[str, int]]] = [["", -1] for _ in range(height_count)]

    for i in range(width_count):
        for j in range(height_count):
            try_count: int = 0
            while True:
                try_count += 1
                random_file_name: str = files[randint(0, len(files) - 1)]
                current_tile_identificators[0] = random_file_name

                if image_is_square:
                    rotation_value: int = randint(0, 3) * 90
                else:
                    rotation_value: int = randint(0, 1) * 180
                current_tile_identificators[1] = rotation_value

                if try_count < 8 and (current_tile_identificators == previous_tile_identificators or
                                      current_tile_identificators == previous_col_identificators[j]):
                    continue

                with Image.open(PATHS["input_path"] + random_file_name) as image:
                    image = image.rotate(rotation_value)
                    workspace.paste(image, (i * (image_width + border_thickness) + border_thickness,
                                            j * (image_height + border_thickness) + border_thickness))
                    previous_tile_identificators = current_tile_identificators.copy()
                    previous_col_identificators[j] = current_tile_identificators.copy()
                    break

    workspace.save(PATHS["output_path"] + "RANDTILED_" + files[0])


if __name__ == "__main__":
    initializer(composer)

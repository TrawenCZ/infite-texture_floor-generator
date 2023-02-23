from typing import List, Tuple, Union

from TilingLib import workspace_init, initializer, PATHS
from PIL import Image
from random import randint


def composer(files: List[str], tile_count: int, border_color: Tuple[int, int, int], border_thickness: int) -> None:
    width_count, height_count = tile_count, tile_count
    workspace, image_is_square, image_width, image_height, border_color = workspace_init(files[0], border_color,
                                                                                         tile_count, border_thickness,
                                                                                         border_thickness)

    previous_tile_identificators: List[Union[str, int]] = ["", -1]
    current_tile_identificators: List[Union[str, int]] = ["", -1]

    current_shift_value: int = 0
    previous_shift_value: int = 0
    min_shift_value: int = round(0.2 * image_width)

    for i in range(height_count):
        while abs(current_shift_value - previous_shift_value) < min_shift_value:
            current_shift_value = randint(0, image_width - 1)
        previous_shift_value = current_shift_value
        first_image_name: str = ""
        first_image_rotation: int = 0

        for j in range(width_count + 1):
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

                if try_count < 8 and current_tile_identificators == previous_tile_identificators:
                    continue

                if j == width_count:
                    random_file_name = first_image_name
                    rotation_value = first_image_rotation

                with Image.open(PATHS["input_path"] + random_file_name) as image:
                    if j == 0:
                        first_image_name = random_file_name
                        first_image_rotation = rotation_value
                    image = image.rotate(rotation_value)
                    workspace.paste(image,
                                    (j * (image_width + border_thickness) + border_thickness - current_shift_value,
                                     i * (image_height + border_thickness) + border_thickness))
                    previous_tile_identificators = current_tile_identificators.copy()
                    break

    crop_right, crop_bottom = workspace.size
    workspace = workspace.crop((border_thickness, border_thickness, crop_right, crop_bottom))

    workspace.save(PATHS["output_path"] + "FLOORED_" + files[0])


if __name__ == "__main__":
    initializer(composer)

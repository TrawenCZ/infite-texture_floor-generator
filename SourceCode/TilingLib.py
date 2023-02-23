from typing import Tuple, List, Union, Dict, Callable

import os
from PIL import Image
from time import sleep
from Messages import EN_MSGS, CZ_MSGS

POSITIVE_STATEMENTS: List[str] = ["yes", "yep", "y", "ano", "jo", "true", "1"]

PATHS: Dict[str, str] = {"input_path": "Input/", "output_path": "Output/",
                         "done_path": "Done/"}
MESSAGES: Dict[str, str] = EN_MSGS
CUSTOM_COLOR: Tuple[int, int, int] = (-1, -1, -1)


def workspace_init(input_file: str, border_color: Tuple[int, int, int], tile_count: int,
                   border_thickness: int, workspace_adder: int) -> \
        Tuple[Image, bool, int, int, Tuple[int, int, int]]:
    image_is_square: bool = False
    with Image.open(PATHS["input_path"] + input_file) as image:
        image_width, image_height = image.size
        if image_width == image_height:
            image_is_square = True
        width_count, height_count = tile_count, tile_count

        if border_color == CUSTOM_COLOR:
            border_color = average_color(image)

        workspace = Image.new("RGB",
                              (width_count * (image_width + border_thickness) + workspace_adder,
                               height_count * (image_height + border_thickness) + workspace_adder),
                              color=border_color)
        return workspace, image_is_square, image_width, image_height, border_color


def average_color(image: Image) -> Tuple[int, int, int]:
    column_rgb_values: List[Tuple[int, int, int]] = []

    for y in range(image.height):
        red_row_total_value: int = 0
        green_row_total_value: int = 0
        blue_row_total_value: int = 0
        for x in range(image.width):
            pixel_rgb_value: Tuple[int, int, int] = image.getpixel((x, y))
            red_row_total_value += pixel_rgb_value[0]
            green_row_total_value += pixel_rgb_value[1]
            blue_row_total_value += pixel_rgb_value[2]
        column_rgb_values.append((round(red_row_total_value / image.width), round(green_row_total_value / image.width),
                                  round(blue_row_total_value / image.width)))

    red_total_value: int = 0
    green_total_value: int = 0
    blue_total_value: int = 0
    for column_rgb_value in column_rgb_values:
        red_total_value += column_rgb_value[0]
        green_total_value += column_rgb_value[1]
        blue_total_value += column_rgb_value[2]

    return round(red_total_value / image.height), round(green_total_value / image.height), \
        round(blue_total_value / image.height)


def loader(tile_count: int, border_color, border_thickness: int, composer: Callable) -> None:
    files: List[str] = []
    fst_image_size: int

    input_folder_content: List[str] = os.listdir(PATHS["input_path"])
    if len(input_folder_content) == 0:
        print(f"'{PATHS['input_path']}'" + MESSAGES["empty_input_folder"])
        return

    for file in input_folder_content:
        try:
            tester = Image.open(PATHS["input_path"] + file)
            tester.close()
            files.append(file)
        except:
            print(f"'{file}'" + MESSAGES["not_valid_image"])
    if len(files) == 0:
        print(MESSAGES["no_valid_imgs_found"])
        return

    composer(files, tile_count, border_color, border_thickness)

    for file in files:
        try:
            os.rename(PATHS["input_path"] + file, PATHS["done_path"] + file)
        except:
            print(f"'{file}'" + MESSAGES["cannot_move_to_folder"] + PATHS["done_path"])
            continue

    print(MESSAGES["successful_create"] + f"'{files}'.")


def define_border_thickness() -> int:
    image_width_millimetres: int = 1
    border_thickness_millimetres: int = 0
    while True:
        try:
            image_width_millimetres = int(input(MESSAGES["tile_width"]))
            if image_width_millimetres < 1:
                print(MESSAGES["mm_above_1"])
                continue
            border_thickness_millimetres = int(input(MESSAGES["border_size"]))
            if border_thickness_millimetres < 0:
                print(MESSAGES["mm_above_0"])
                continue
            break
        except:
            print(MESSAGES["incorrect_number_format"])
            continue

    files = os.listdir(PATHS["input_path"])
    if len(files) < 1:
        print(f"'{PATHS['input_path']}'" + MESSAGES["empty_input_folder"])
        return -1

    try:
        with Image.open(PATHS["input_path"] + files[0]) as image:
            pixels_per_millimeter = image.width / image_width_millimetres
            return round(border_thickness_millimetres * pixels_per_millimeter)
    except:
        print(f"'{files[0]}'" + MESSAGES["not_valid_image"])
        return -1


def test_rgb_range(number: int) -> bool:
    return 255 >= number >= 0


def define_border_color() -> Tuple[int, int, int]:
    border_color: Union[Tuple[int, int, int], str] = (255, 255, 255) if input(MESSAGES["white_borders"]).lower() in \
                                                                        POSITIVE_STATEMENTS else CUSTOM_COLOR
    if border_color == CUSTOM_COLOR:
        while input(MESSAGES["custom_color_borders"]).lower() in POSITIVE_STATEMENTS:
            color_format = input(MESSAGES["color_format"])
            if color_format == "1":
                try:
                    red = int(input(MESSAGES["RGB_red"]))
                    green = int(input(MESSAGES["RGB_green"]))
                    blue = int(input(MESSAGES["RGB_blue"]))
                    if not test_rgb_range(red) or not test_rgb_range(green) or not test_rgb_range(blue):
                        print(MESSAGES["RGB_out_of_range"])
                        continue
                    border_color = (red, green, blue)
                    break
                except:
                    print(MESSAGES["wrong_input_format"])
                    continue
            elif color_format == "2":
                hex_border_color = input(MESSAGES["hex_input"])
                hex_border_color = hex_border_color.lstrip("#")
                if len(hex_border_color) != 6:
                    print(MESSAGES["hex_invalid_length"])
                    continue
                border_color = tuple(int(hex_border_color[i:i + 2], 16) for i in (0, 2, 4))
                if not test_rgb_range(border_color[0]) or not test_rgb_range(border_color[1]) or not test_rgb_range(
                        border_color[2]):
                    print(MESSAGES["hex_invalid_format"])
                    continue
                break
            else:
                print(MESSAGES["incorrect_number_format"])
                continue
    return border_color


def define_tile_count() -> int:
    while True:
        try:
            tile_count: int = int(input(MESSAGES["image_count"]))
            if tile_count > 30:
                print(MESSAGES["too_big_number"])
                continue
            elif tile_count < 0:
                print(MESSAGES["try_positive_number"])
                continue
            elif tile_count == 0:
                print(MESSAGES["try_non_zero"])
                continue
            return tile_count
        except:
            print(MESSAGES["incorrect_number_format"])
            continue


def rotate_and_resize_if_needed() -> bool:
    first_image_params_set: bool = False
    should_ignore_different_ratios: bool = False
    first_image_ratio: float = 0
    first_image_size: Tuple[int, int] = (0, 0)
    ratio_tolerance_const: float = 0.1

    for file in os.listdir(PATHS["input_path"]):
        try:
            image: Image = Image.open(PATHS["input_path"] + file)
            if image.width < image.height:
                image = image.transpose(Image.ROTATE_90)
                image.save(PATHS["input_path"] + "rotated_" + file)
                os.remove(PATHS["input_path"] + file)
                file = "rotated_" + file

            if not first_image_params_set:
                first_image_ratio = image.size[0] / image.size[1]
                first_image_size = image.size
                first_image_params_set = True
                image.close()
                continue

            curr_size_ratio: float = image.size[0] / image.size[1]
            if not should_ignore_different_ratios \
                    and (curr_size_ratio > first_image_ratio + ratio_tolerance_const
                         or curr_size_ratio < first_image_ratio - ratio_tolerance_const):
                if input(MESSAGES["image_differs"]).lower() not in POSITIVE_STATEMENTS:
                    image.close()
                    return False
                else:
                    should_ignore_different_ratios = True

            if image.size != first_image_size:
                image = image.resize(first_image_size)
                image.save(PATHS["input_path"] + "resized_" + file)
                image.close()
                os.remove(PATHS["input_path"] + file)
            else:
                image.close()
        except:
            continue
    return True


def save_config(dirs: Dict[str, str], language: str) -> None:
    with open(".config/config.txt", "w") as config_file:
        config_file.write(f"lang={language}\n")
        config_file.write(f"input_path={dirs['input_name']}\n")
        config_file.write(f"output_path={dirs['output_name']}\n")
        config_file.write(f"done_path={dirs['done_name']}")


def dir_init() -> None:
    if not os.path.exists(PATHS["input_path"]):
        os.makedirs(PATHS["input_path"])
    if not os.path.exists(PATHS["output_path"]):
        os.makedirs(PATHS["output_path"])
    if not os.path.exists(PATHS["done_path"]):
        os.makedirs(PATHS["done_path"])


def first_start_init() -> None:
    print(EN_MSGS["welcome_msg"] + " / " + CZ_MSGS["welcome_msg"] + "\n")
    lang_input: str
    while True:
        lang_input = input("Please choose a language (type 'en' for English or 'cz' for Czech) / "
                           "Prosím zvolte si jazyk (napište 'en' pro angličtinu nebo 'cz' pro češtinu:\n")
        if lang_input.lower() not in ["en", "cz"]:
            print("Invalid language input, please try again. / "
                  "Byla zadána neplatná hodnota pro jazyk, zkuste to prosím znovu.\n")
            continue
        break

    en_dirs: Dict[str, str] = {
        "input_name": "Input/",
        "output_name": "Output/",
        "done_name": "Done/"
    }
    cz_dirs: Dict[str, str] = {
        "input_name": "Vstup/",
        "output_name": "Vystup/",
        "done_name": "Hotovo/"
    }
    dir_names: Dict[str, str] = en_dirs if lang_input == "en" else cz_dirs
    save_config(dir_names, lang_input)


def remove_quotes(input_string: str) -> str:
    return input_string.strip().replace("\"", "").replace("'", "")


def check_config_existence() -> Tuple[bool, str]:
    first_start: bool = False
    config_folder: str = "./.config/"
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)
    config_file: str = ""
    for file in os.listdir(config_folder):
        if file.lower().find("config") == -1:
            continue
        config_file = config_folder + file
        break
    if config_file == "":
        f = open(config_folder + "config.txt", "w")
        f.close()
        config_file = config_folder + "config.txt"
        first_start = True
    return first_start, config_file


def load_config() -> None:
    global PATHS
    global MESSAGES
    first_start, config_file = check_config_existence()

    if first_start:
        first_start_init()

    with open(config_file, "r") as f:
        for line in f:
            if len(line.strip()) == 0:
                continue
            if line.find("=") == -1:
                print(MESSAGES["wrong_config_format"] +
                      "lang=en\ninput_path=Input/\noutput_path='Output/'\ndone_path=\"Done\"")
                break
            splitted_line: List[str] = line.split("=", 1)
            value_type: str = remove_quotes(splitted_line[0]).lower()
            value: str = remove_quotes(splitted_line[1])
            if len(value) == 0:
                print(MESSAGES["empty_config_value"])
                continue
            if value_type != "lang" and value[len(value) - 1] != "/":
                value += "/"
            if value_type == "input_path":
                PATHS["input_path"] = value
            if value_type == "output_path":
                PATHS["output_path"] = value
            if value_type == "done_path":
                PATHS["done_path"] = value
            if value_type == "lang":
                if value.lower() == "cz":
                    MESSAGES = CZ_MSGS
                elif value.lower() == "en":
                    MESSAGES = EN_MSGS
                else:
                    print("Unsupported language in config file. Using English.\n")

    dir_init()


def initializer(composer: Callable):
    load_config()
    print(MESSAGES["welcome_msg"] + "\n")
    if not rotate_and_resize_if_needed():
        print(MESSAGES["goodbye"])
        sleep(5)
        return

    border_color: Union[Tuple[int, int, int], str] = define_border_color()
    tile_count: int = define_tile_count()

    border_thickness: int = define_border_thickness()
    if border_thickness < 0:
        sleep(5)
        return

    loader(tile_count, border_color, border_thickness, composer)
    print(MESSAGES["goodbye"])
    sleep(5)

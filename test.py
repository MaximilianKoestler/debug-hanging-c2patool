import pathlib
import platform
import subprocess


def c2pa_binary():
    """
    Return the C2PA binary corresponding for the current OS
    """

    system = platform.uname().system.lower()
    binary = pathlib.Path(f"c2patool/c2patool_0.6.2_{system}")
    if system == "windows":
        binary = binary.with_name(binary.name + ".exe")
    ret_code, res = subprocess.getstatusoutput(str(binary))
    if ret_code != 2:
        raise EnvironmentError(f"c2patool not found at {binary}")
    return binary


C2PA_BINARY = c2pa_binary().as_posix()


def call_with_print(cmd):
    """
    Print and execute a command for the c2patool
    """

    cmd = [C2PA_BINARY] + cmd
    print(" ".join(str(c) for c in cmd))
    subprocess.check_call(cmd, stdout=-1)


pathlib.Path("output").mkdir(exist_ok=True)

# create a signed first ingredient
call_with_print(
    [
        "c2pa_sample/image.jpg",
        "-m",
        "c2pa_sample/test.json",
        "-o",
        "output/signed_1.jpg",
        "-f",
    ]
)

# make it an ingredient
call_with_print(
    [
        "--ingredient",
        "output/signed_1.jpg",
        "-o",
        "output/signed_1_ingredient",
        "-f",
    ]
)

# create a signed second ingredient
call_with_print(
    [
        "c2pa_sample/image.jpg",
        "-m",
        "c2pa_sample/test.json",
        "-o",
        "output/signed_2.jpg",
        "-f",
    ]
)

# make it an ingredient as well
call_with_print(
    [
        "--ingredient",
        "output/signed_2.jpg",
        "-o",
        "output/signed_2_ingredient",
        "-f",
    ],
)

# combine both ingredients into a new image
print()
print("The next call will hang indefinitely")
call_with_print(
    [
        "c2pa_sample/image.jpg",
        "-m",
        "test_with_ingredient.json",
        "-o",
        "output/signed_from_ingredients.jpg",
        "-f",
    ]
)

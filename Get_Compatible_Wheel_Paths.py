from pip._internal.models.target_python import TargetPython
from pip._vendor.packaging.tags import Tag
import os, glob

target_python = TargetPython()
pep425tags: list[Tag] = target_python.get_tags()


if not os.path.isdir("dist"):
    raise Exception("No dist folder.")

wheel_paths : list[str] = glob.glob("dist/InterruptibleSleepBinding*.whl")

valid_wheel_paths = [wheel_path for wheel_path in wheel_paths if any([
	str(tag) in wheel_path for tag in pep425tags
])]

[print(valid_wheel_path) for valid_wheel_path in valid_wheel_paths]
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'AzureImage/')


# Output Model File Name
OUTPUT_MODEL_DIR = os.path.join(BASE_DIR, 'model/')
MODEL_FILE_PATH = OUTPUT_MODEL_DIR + 'model.h5'
OUTPUT_MODEL_PLOT_FILE = OUTPUT_MODEL_DIR + "model.png"

CASCADE_FILE_PATH = os.path.join(BASE_DIR, 'haarcascade_frontalface_default.xml')
OUTPUT_IMAGE_DIR = os.path.join(BASE_DIR, "face_image/")
#IMAGE_PATH_PATTERN = os.path.join(BASE_DIR, "jin7/*")
# Test Image Directory
TEST_IMAGE_PATH = os.path.join(BASE_DIR, "test_image")
# Face Image Directory
SCRATCH_IMAGE_PATH_PATTERN = OUTPUT_IMAGE_DIR + "/*"
# Output Directory
SCRATCH_OUTPUT_IMAGE_DIR = os.path.join(BASE_DIR, "face_scratch_image")


def delete_dir(dir_path, is_delete_top_dir=True):
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    if is_delete_top_dir:
        os.rmdir(dir_path)

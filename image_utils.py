import os

def cleanup_images(folder: str):
    """
    Deletes all temporary images.
    """
    for f in os.listdir(folder):
        path = os.path.join(folder, f)
        if os.path.isfile(path):
            os.remove(path)

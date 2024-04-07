from PIL import Image
from PIL.ExifTags import TAGS
import glob


class LocationInfo():
    """
    A class to extract location information from an image's EXIF metadata.

    Attributes:
        image (PIL.Image.Image): The image object containing EXIF metadata.
    """

    def __init__(self, image_path):
        """
        Initializes the LocationInfo object.

        Args:
            image_path (str): The path to the image file.
        """
        super().__init__()
        self.image = Image.open(image_path)


    def extract_location(self):
        """
        Extracts location information from the image's EXIF metadata.

        Returns:
            dict: A dictionary containing location information (latitude, longitude, altitude).
        """
        # Extract EXIF data from the image
        exif_data = self.image._getexif()

        # Check if EXIF data exists
        if exif_data is not None:
            # Extract relevant EXIF tags
            exif = {
                TAGS[k]: v
                for k, v in exif_data.items()
                if k in TAGS
            }
            # Extract GPS information
            loc_info = exif['GPSInfo']

            # Define keys for location information
            keys = ['Latitude', 'Lat_dir', 'Longitude', 'Long_dir', 'Altitude']

            # Construct location dictionary
            location = {
                keys[0]: loc_info[2],   # Latitude
                keys[2]: loc_info[4],   # Longitude
            }
            return location


if __name__ == "__main__":

    # Example usage
    image_paths = glob.glob("images/*.JPG")
    for image_path in image_paths:
        loc = LocationInfo(image_path)
        location = loc.extract_location()
        print("GPS Information:\n", location)

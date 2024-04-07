from metadata import LocationInfo
import cv2
import glob


def image_stitcher(images):
    """
    Stitch multiple images together.

    Parameters:
        images (list of numpy.ndarray): List of images to be stitched.

    Returns:
        numpy.ndarray: Stitched image if successful, None otherwise.
    """
    stitcher = cv2.Stitcher_create()  # Create a stitcher object
    status, stitched_image = stitcher.stitch(images)  # Attempt to stitch images

    if status == cv2.STITCHER_OK:  # If stitching successful
        return stitched_image  # Return the stitched image
    else:
        print("An error occurred in stitching images")  # Print error message if stitching fails


def get_parent_image_boundaries(stitched_image, num_images):
    """
    Determine boundaries of parent images in the stitched image.

    Parameters:
        stitched_image (numpy.ndarray): The stitched image.
        num_images (int): Number of images stitched together.

    Returns:
        list of tuples: List containing tuples of parent image boundaries.
                        Each tuple contains (top, bottom) boundaries.
    """
    boundaries = []  # List to store parent image boundaries
    stitched_image_width = stitched_image.shape[1]  # Get width of stitched image
    parent_width = stitched_image_width // num_images  # Calculate width of each parent image

    for i in range(num_images):  # Iterate over the number of images
        top = i * parent_width  # Calculate top boundary
        bottom = top + parent_width  # Calculate bottom boundary
        boundaries.append((top, bottom))  # Append boundaries to the list

    return boundaries  # Return the list of boundaries


def on_mouse_hover(event, x, y, flags, params):
    """
    Handle mouse hover event.

    Parameters:
        event (int): Type of mouse event.
        x (int): X-coordinate of the mouse cursor.
        y (int): Y-coordinate of the mouse cursor.
        flags (int): Additional flags.
        params (dict): Additional parameters containing 'boundaries' and 'images'.
    """
    if event == cv2.EVENT_MOUSEMOVE:  # If mouse move event
        # Extract clicked coordinates
        clicked_x, clicked_y = x, y

        # Get parent image boundaries and images
        boundaries = params['boundaries']
        images = params['images']

        # Find the corresponding parent image
        for i, (left, right) in enumerate(boundaries):
            if left <= clicked_x < right:
                print(f"Clicked on parent image {i + 1}")  # Print the index of clicked parent image
                # Extract and display the corresponding parent image
                parent_image = images[i]
                cv2.imshow('Parent Image', parent_image)
                break  # Exit loop once parent image is found


def main():
    """
    Main function to load images, stitch them, and handle mouse events.
    """
    image_paths = glob.glob("images/*.jpg")  # Get paths of all JPG images in 'images' directory
    images = []
    locations = []

    for path in image_paths:
        loc = LocationInfo(path) # Get location from metadata
        location = loc.extract_location()
        locations.append(location)
        img = cv2.imread(path)  # Read image
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)  # Rotate image clockwise by 90 degrees
        images.append(img)  # Append rotated image to the list
    print("Image loading complete...")

    num_images = len(images)  # Get the number of images
    stitched_image = image_stitcher(images)  # Stitch the images together
    boundaries = get_parent_image_boundaries(stitched_image, num_images)  # Get parent image boundaries

    # Print Location Information
    # print(locations)

    # Create a window and register mouse callback
    cv2.imwrite('stitched.png', stitched_image)
    cv2.imshow('Stitched Image', stitched_image)
    cv2.setMouseCallback('Stitched Image', on_mouse_hover, {'boundaries': boundaries, 'images': images})
    cv2.waitKey(0)  # Wait for any key press
    cv2.destroyAllWindows()  # Close all OpenCV windows when done


if __name__ == "__main__":
    main()

import face_recognition
import cv2
import os

# Create folders if they don't exist
os.makedirs('output', exist_ok=True)
os.makedirs('failed', exist_ok=True)

def detect_faces(image_path):
    """
    Detects faces in an image and returns the locations of the faces.
    """
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    return face_locations

def draw_rectangles_and_save(image_path, face_locations, output_path):
    """
    Crops around the detected face with margin, but ensures the crop
    covers at least 50% of the original image area, then resizes to 512x512.
    """
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    orig_area = height * width

    if face_locations:
        top, right, bottom, left = face_locations[0]

        face_width = right - left
        face_height = bottom - top

        # Margin: 50% of face size
        margin_x = int(face_width * 0.5)
        margin_y = int(face_height * 0.5)

        # Initial crop coords with margin
        new_left = max(0, left - margin_x)
        new_top = max(0, top - margin_y)
        new_right = min(width, right + margin_x)
        new_bottom = min(height, bottom + margin_y)

        crop_width = new_right - new_left
        crop_height = new_bottom - new_top
        crop_area = crop_width * crop_height

        # Minimum crop area to be at least 50% of original image
        min_area = orig_area * 0.5

        # If crop area too small, expand the crop centered on current crop
        if crop_area < min_area:
            target_area = min_area
            target_side = int(target_area ** 0.5)  # square approx

            center_x = new_left + crop_width // 2
            center_y = new_top + crop_height // 2

            half_side = target_side // 2
            new_left = max(0, center_x - half_side)
            new_top = max(0, center_y - half_side)
            new_right = min(width, center_x + half_side)
            new_bottom = min(height, center_y + half_side)

            if new_right - new_left < target_side:
                new_left = max(0, new_right - target_side)
            if new_bottom - new_top < target_side:
                new_top = max(0, new_bottom - target_side)

        cropped = image[new_top:new_bottom, new_left:new_right]

    else:
        # No faces: center crop at least 50% of image area
        min_area = orig_area * 0.5
        target_side = int(min_area ** 0.5)
        target_side = min(target_side, height, width)

        center_y, center_x = height // 2, width // 2
        new_top = max(0, center_y - target_side // 2)
        new_left = max(0, center_x - target_side // 2)
        new_bottom = min(height, new_top + target_side)
        new_right = min(width, new_left + target_side)

        cropped = image[new_top:new_bottom, new_left:new_right]

    # Resize to 512x512
    output_image = cv2.resize(cropped, (512, 512))
    cv2.imwrite(output_path, output_image)



def main():
    load_folder = 'load'
    output_folder = 'output'
    failed_folder = 'failed'

    for filename in os.listdir(load_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(load_folder, filename)
            print(f"Processing: {filename}")

            face_locations = detect_faces(image_path)

            if face_locations:
                output_path = os.path.join(output_folder, filename)
                print(f"✅ Faces detected in {filename} ({len(face_locations)} face(s))")
            else:
                output_path = os.path.join(failed_folder, filename)
                print(f"❌ No faces detected in {filename}")

            draw_rectangles_and_save(image_path, face_locations, output_path)

if __name__ == "__main__":
    main()

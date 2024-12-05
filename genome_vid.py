from PIL import Image
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import os

# Path to the folder containing genome images
image_folder = "genome_pics"
output_video = "genome_evolution.mp4"
fps = 2  # Frames per second

def preprocess_images(image_folder, target_size):
    """Resize all images in the folder to the target size."""
    resized_folder = os.path.join(image_folder, "resized")
    os.makedirs(resized_folder, exist_ok=True)

    for file in os.listdir(image_folder):
        if file.endswith(".png"):
            filepath = os.path.join(image_folder, file)
            try:
                with Image.open(filepath) as img:
                    resized_img = img.resize(target_size, Image.Resampling.LANCZOS)
                    resized_img.save(os.path.join(resized_folder, file))
                    print(f"Resized {file} to {resized_img.size}")  # Log image size
            except Exception as e:
                print(f"Error processing {file}: {e}")

    return resized_folder


def generate_video(image_folder, output_video, fps=5):
    # Preprocess images to ensure consistent size
    target_size = (640, 480)  # Specify the desired size
    resized_folder = preprocess_images(image_folder, target_size)

    # Get all PNG files from the resized folder, sorted numerically by generation number
    image_files = sorted(
        [os.path.join(resized_folder, f) for f in os.listdir(resized_folder) if f.endswith(".png")],
        key=lambda x: int(os.path.basename(x).split("_")[-1].split(".")[0])  # Extract numeric part
    )

    if not image_files:
        print("No images found in the folder. Please ensure the folder contains .png files.")
        return

    # Create a video from the images
    print(f"Creating video with {len(image_files)} frames at {fps} FPS...")
    clip = ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile(output_video, codec="libx264")

    print(f"Video saved as {output_video}.")


# Call the function
if __name__ == "__main__":
    generate_video(image_folder, output_video, fps)

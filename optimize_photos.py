import os
import subprocess
import glob

def main():
    img_dir = "images/tmp_hcdp"
    
    # Grab all image files
    extensions = ('*.jpeg', '*.jpg', '*.png', '*.webp', '*.avif')
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(img_dir, ext)))
        
    print(f"Found {len(files)} photos to compress for 3D WebGL...")
    
    for idx, f in enumerate(files):
        # sips -Z 1024 downscales the image so the longest edge is 1024, preserving aspect ratio.
        # It operates in-place!
        try:
            subprocess.run(['sips', '-Z', '1024', f], check=True, capture_output=True)
            if idx % 10 == 0:
                print(f"Compressed {idx}/{len(files)}")
        except Exception as e:
            print(f"Failed to compress {f}: {e}")
            
    print("Optimization Complete! All 3D textures are now Web-Safe.")

if __name__ == '__main__':
    main()

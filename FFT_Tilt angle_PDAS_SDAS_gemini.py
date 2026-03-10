import cv2
import numpy as np
import matplotlib.pyplot as plt


def auto_calculate_pdas_sdas_zeromean(image_path, physical_pixel_size=1.0):
    # 1. Load the image and apply Hanning window
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: Could not load the image '{image_path}'.")
        return

    h, w = img.shape
    window_y = np.hanning(h)
    window_x = np.hanning(w)
    window_2d = np.outer(window_y, window_x)
    img_windowed = img * window_2d

    # Subtract the mean to eliminate the DC component (Red Dot)
    img_windowed = img_windowed - np.mean(img_windowed)

    # 2. Perform 2D FFT and shift to center
    f_transform = np.fft.fft2(img_windowed)
    f_shift = np.fft.fftshift(f_transform)
    magnitude_spectrum = 20 * np.log(1 + np.abs(f_shift))

    # 3. Setup coordinates
    cy, cx = h // 2, w // 2
    Y, X = np.ogrid[:h, :w]
    R = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    Theta = np.arctan2(cy - Y, X - cx)

    masked_spectrum = magnitude_spectrum.copy()
    masked_spectrum[R < 2] = 0

    # 4. Find Peak 1 (The Absolute Brightest Peak)
    py1, px1 = np.unravel_index(np.argmax(masked_spectrum), masked_spectrum.shape)
    theta1 = np.arctan2(cy - py1, px1 - cx)

    # 5. Apply the "Pie Slice" Mask to hide Peak 1
    angular_distance = np.abs(np.sin(Theta - theta1))
    masked_spectrum[angular_distance < np.sin(np.radians(30))] = 0

    # 6. Find Peak 2 (The Second Brightest Peak, orthogonal to Peak 1)
    py2, px2 = np.unravel_index(np.argmax(masked_spectrum), masked_spectrum.shape)

    # 7. Calculate Distances and Sort into PDAS vs SDAS
    r1 = np.sqrt((px1 - cx) ** 2 + (cy - py1) ** 2)
    r2 = np.sqrt((px2 - cx) ** 2 + (cy - py2) ** 2)

    if r1 < r2:
        pdas_r, pdas_py, pdas_px = r1, py1, px1
        sdas_r, sdas_py, sdas_px = r2, py2, px2
    else:
        pdas_r, pdas_py, pdas_px = r2, py2, px2
        sdas_r, sdas_py, sdas_px = r1, py1, px1

    # 8. Calculate Final Spacings
    pdas_pixels = w / pdas_r
    pdas_real = pdas_pixels * physical_pixel_size
    sdas_pixels = w / sdas_r
    sdas_real = sdas_pixels * physical_pixel_size

    # Calculate angles (0 to 180 degrees)
    pdas_angle = np.degrees(np.arctan2(cy - pdas_py, pdas_px - cx)) % 180
    sdas_angle = np.degrees(np.arctan2(cy - sdas_py, sdas_px - cx)) % 180

    # 9. Visualization Dashboard
    plt.figure(figsize=(15, 7))

    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original Microstructure')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(magnitude_spectrum, cmap='gray',
               vmin=np.percentile(magnitude_spectrum, 60),
               vmax=np.percentile(magnitude_spectrum, 99.5))

    plt.plot(cx, cy, 'ro', markersize=6, label='Center (DC Component)')
    plt.plot(pdas_px, pdas_py, 'go', markersize=7, label='PDAS Peak')
    plt.plot(cx - (pdas_px - cx), cy + (cy - pdas_py), 'go', markersize=7)
    plt.plot(sdas_px, sdas_py, 'bo', markersize=7, label='SDAS Peak')
    plt.plot(cx - (sdas_px - cx), cy + (cy - sdas_py), 'bo', markersize=7)

    # UPDATED: Explicitly stating "from vertical" for clarity
    title_text = (f"Auto-Detected Spacings\n"
                  f"PDAS: {pdas_pixels:.1f} px ({pdas_real:.2f} units) | Angle: {pdas_angle:.1f}° from vertical\n"
                  f"SDAS: {sdas_pixels:.1f} px ({sdas_real:.2f} units) | Angle: {sdas_angle:.1f}° from vertical")

    plt.title(title_text)
    plt.legend()
    plt.axis('off')

    plt.tight_layout()
    plt.show()


# --- Execution ---
file_name = r'C:\Users\rifat\Downloads\img_0_2_cropped.png'
my_pixel_size = 1/7.2801

auto_calculate_pdas_sdas_zeromean(file_name, physical_pixel_size=my_pixel_size)
import cv2
import numpy as np
import struct
import cry

def create_frame(data: bytes, pxl_size=20) -> np.ndarray:
    h, w = 1080, 1920
    frame = np.zeros((h, w, 3), dtype=np.uint8)
    
    block_h = block_w = pxl_size
    
    idx = 0
    for y in range(0, h, block_h):
        for x in range(0, w, block_w):
            if idx >= len(data):
                return frame
            r = data[idx]   if idx   < len(data) else 0
            g = data[idx+1] if idx+1 < len(data) else 0
            b = data[idx+2] if idx+2 < len(data) else 0
            frame[y:y+block_h, x:x+block_w] = [b, g, r]   # BGR
            idx += 3
    return frame


def encode_file(input_path: str, output_path: str, fps=5, key="secret", pxl_size=20):
    with open(input_path, 'rb') as f:
        file_bytes = f.read()
        file_bytes = cry.encrypt_data(file_bytes, key.encode())

    # Добавляем в начало 4 байта с длиной исходного файла (little‑endian)
    header = struct.pack('<I', len(file_bytes))
    data_with_header = header + file_bytes

    bytes_per_frame = (1920 * 1080 * 3) // (pxl_size * pxl_size)  # 15552 байта на кадр
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    out = cv2.VideoWriter(output_path, fourcc, fps, (1920, 1080))

    for i in range(0, len(data_with_header), bytes_per_frame):
        chunk = data_with_header[i : i + bytes_per_frame]
        frame = create_frame(chunk, pxl_size)
        out.write(frame)

    out.release()
    print("Готово")


if __name__ == "__main__":
    encode_file('img.jpg', 'video.avi', fps=5, pxl_size=2)
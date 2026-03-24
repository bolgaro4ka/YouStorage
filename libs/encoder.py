import cv2
import numpy as np
import struct
import cry
import config
import consts

def create_frame(data: bytes, pxl_size=20, video_width: int = 1920, video_height: int = 1080) -> np.ndarray:
    h, w = video_height, video_width
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

def create_first_frame(out: cv2.VideoWriter, pxl_size: int, video_width: int, video_height: int, fps: int, file_path: str = "",
                       show_file_name: bool = False, show_file_format: bool = False):
    card = np.zeros((video_height, video_width, 3), dtype=np.uint8)

    card[:] = (40, 40, 40)

    text = f"Video Encoded by YouStorage (https://github.com/bolgaro4ka/youstorage)\n\nPixel Size: {pxl_size}x{pxl_size}\nResolution: {video_height}x{video_width}\nFPS: {fps}\n\nBytes per frame: {(video_width * video_height * 3) // (pxl_size * pxl_size)}\nMegabytes per second: {round(((((video_width * video_height * 3) // (pxl_size * pxl_size)) * fps) / 1024) / 1024, 3)}\n\nVersion: {consts.VERSION}"
    add_name = f"File Name: {file_path}" if show_file_name else ""
    add_format = f"File Format: {file_path.split('.')[-1]}" if show_file_format and '.' in file_path else ""

    text = text + "\n\n" + add_name + "\n" + add_format

    lines = text.split("\n")

    y = 100
    for line in lines:
        (w, h), _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)

        cv2.putText(card, line, (50, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA)

        y += h + 10  # высота строки + отступ

    square_size = 20
    margin = 0

    h, w, _ = card.shape

    # левый верх
    cv2.rectangle(card,
                (margin, margin),
                (margin + square_size, margin + square_size),
                (255, 255, 255),
                -1)

    # правый верх
    cv2.rectangle(card,
                (w - margin - square_size, margin),
                (w - margin, margin + square_size),
                (255, 255, 255),
                -1)

    # левый низ
    cv2.rectangle(card,
                (margin, h - margin - square_size),
                (margin + square_size, h - margin),
                (255, 255, 255),
                -1)
    
    bar_height = 80
    padding = int(80)

    for x in range(w-padding):
        hue = int(180 * x / w)  # OpenCV использует 0–179
        color = np.uint8([[[hue, 255, 255]]])  # HSV
        bgr = cv2.cvtColor(color, cv2.COLOR_HSV2BGR)[0][0]

        cv2.line(card,
                (x + int(padding/2), h - bar_height - int(padding/2)),
                (x + int(padding/2), h - int(padding/2)),
                tuple(int(c) for c in bgr),
                1)

    for x in range(w-padding):
        r = b = g = int(255 * x / w)

        cv2.line(card,
                (x + int(padding/2), h - int(bar_height/2) - int(padding/2) - padding),
                (x + int(padding/2), h - int(padding/2) - padding),
                (b, g, r),
                1)

    out.write(card)

def create_end_frame(out: cv2.VideoWriter, pxl_size: int, video_width: int, video_height: int, file_path: str = "",
                       show_file_name: bool = False, show_file_format: bool = False):
    card = np.zeros((video_height, video_width, 3), dtype=np.uint8)

    card[:] = (40, 40, 40)

    

    text = f"Video Encoded by YouStorage (https://github.com/bolgaro4ka/youstorage)\nPixel Size: {pxl_size}x{pxl_size}\nEnd for file"
    add_name = f"File Name: {file_path}" if show_file_name else ""
    add_format = f"File Format: {file_path.split('.')[-1]}" if show_file_format and '.' in file_path else ""

    text = text + "\n\n" + add_name + "\n" + add_format

    lines = text.split("\n")

    y = 100
    for line in lines:
        (w, h), _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)

        cv2.putText(card, line, (50, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA)

        y += h + 10  # высота строки + отступ

    square_size = 20
    margin = 0

    h, w, _ = card.shape

    # левый верх
    cv2.rectangle(card,
                (margin, margin),
                (margin + square_size, margin + square_size),
                (0, 0, 255),
                -1)

    # правый верх
    cv2.rectangle(card,
                (w - margin - square_size, margin),
                (w - margin, margin + square_size),
                (0, 0, 255),
                -1)

    # левый низ
    cv2.rectangle(card,
                (margin, h - margin - square_size),
                (margin + square_size, h - margin),
                (0, 0, 255),
                -1)

    out.write(card)



def encode_file(input_path: str, output_path: str, fps=5, key="secret", pxl_size=20, video_width=1920, video_height=1080,
                show_first_frame=True, show_file_name=True, show_file_format=True, show_end_frame=True):
    with open(input_path, 'rb') as f:
        file_bytes = f.read()
        file_bytes = cry.encrypt_data(file_bytes, key.encode())

    # Добавляем в начало 4 байта с длиной исходного файла (little‑endian)
    header = struct.pack('<I', len(file_bytes))
    data_with_header = header + file_bytes

    bytes_per_frame = (video_width * video_height * 3) // (pxl_size * pxl_size)  # 15552 байта на кадр
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    out = cv2.VideoWriter(output_path, fourcc, fps, (video_width, video_height))

    if show_first_frame:
        create_first_frame(out, pxl_size, video_width, video_height, fps, file_path=input_path, show_file_name=show_file_name, show_file_format=show_file_format)

    for i in range(0, len(data_with_header), bytes_per_frame):
        chunk = data_with_header[i : i + bytes_per_frame]
        frame = create_frame(chunk, pxl_size, video_width, video_height)
        out.write(frame)

    if show_end_frame:
        create_end_frame(out, pxl_size, video_width, video_height, file_path=input_path, show_file_name=show_file_name, show_file_format=show_file_format)
    
    out.release()
    print("Готово")


if __name__ == "__main__":
    encode_file(config.ENCODE_FILE_PATH, config.ENCODE_ENCRYPTED_FILE_NAME, fps=config.FPS, pxl_size=config.PIXEL_SIZE, video_height=config.VIDEO_HEIGHT, video_width=config.VIDEO_WIDTH,
                show_first_frame=config.SHOW_FIRST_FRAME, show_file_name=config.SHOW_FILE_NAME, show_file_format=config.SHOW_FILE_FORMAT, key="secret",
                show_end_frame=config.SHOW_END_FRAME)
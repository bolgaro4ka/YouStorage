import cv2
import struct
import cry

def read_blocks_from_frame(frame, pxl_size):
    blocks = []
    h, w = 1080, 1920
    block_h = block_w = pxl_size

    for y in range(0, h, block_h):
        for x in range(0, w, block_w):
            pixel = frame[y, x]
            blocks.extend([pixel[2], pixel[1], pixel[0]])
    return blocks


def decode(video_path, pxl_size, save_as="file.docx", key="secret"):
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        raise IOError(f"Не удалось открыть видео: {video_path}")

    all_bytes = []

    while True:
        ret, frame = video.read()
        if not ret:
            break
        all_bytes.extend(read_blocks_from_frame(frame, pxl_size))

    video.release()

    # Первые 4 байта – длина исходного файла
    if len(all_bytes) < 4:
        raise ValueError("Видео слишком короткое, нет заголовка длины")

    file_size = struct.unpack('<I', bytes(all_bytes[:4]))[0]
    file_data = cry.decrypt_data(bytes(all_bytes[4:4+file_size]), key.encode())

    with open(save_as, 'wb') as f:
        f.write(bytes(file_data))

    print(f"Восстановлено {len(file_data)} байт")

if __name__ == "__main__":
    decode('video.avi', 2, save_as='cat.jpg', key="secret")
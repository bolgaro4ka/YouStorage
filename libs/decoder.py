import cv2
import struct
import libs.cry as cry
import config
from tqdm import tqdm

from cv2.typing import MatLike

def read_blocks_from_frame(frame : MatLike, pxl_size):
    blocks = []
    h, w = frame.shape[0], frame.shape[1]
    block_h = block_w = pxl_size

    for y in range(0, h, block_h):
        for x in range(0, w, block_w):
            pixel = frame[y, x]
            blocks.extend([pixel[2], pixel[1], pixel[0]])
    return blocks


def decode(video_path, pxl_size : int, save_as="file.docx", key="secret", skip_first_frame=config.SKIP_FIRST_FRAME, skip_end_frame=config.SKIP_END_FRAME):
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        raise IOError(f"Не удалось открыть видео: {video_path}")
    

    all_bytes = []
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    for idx in tqdm(range(1, total_frames), desc="Decoding", ncols=100):
        ret, frame = video.read()
        if not ret:
            break

        if (idx == 1) and (skip_first_frame):
            continue

        if (idx == total_frames) and (skip_end_frame):
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
    pass
# main.py
import argparse
import os
from libs.encoder import encode_file
from libs.decoder import decode
import config


def main():
    parser = argparse.ArgumentParser(description="Хранение данных в видео на YouTube")
    subparsers = parser.add_subparsers(dest="command", help="Команды")

    # Команда encode
    encode_parser = subparsers.add_parser("encode", help="Закодировать файл в видео")
    encode_parser.add_argument("input", help="Входной файл")
    encode_parser.add_argument("output", help="Выходное видео (MP4)")
    encode_parser.add_argument("--key", required=True, help="Ключ шифрования (строка)")
    encode_parser.add_argument("--pixel-size", type=int, default=config.PIXEL_SIZE)
    encode_parser.add_argument("--width", type=int, default=config.VIDEO_WIDTH)
    encode_parser.add_argument("--height", type=int, default=config.VIDEO_HEIGHT)
    encode_parser.add_argument("--fps", type=int, default=config.FPS)

    encode_parser.add_argument("--show-first-frame", type=bool, default=config.SHOW_FIRST_FRAME, help="Показать первый кадр с информацией о файле")
    encode_parser.add_argument("--show-file-name", type=bool, default=config.SHOW_FILE_NAME, help="Показать имя файла на первом кадре")
    encode_parser.add_argument("--show-file-format", type=bool, default=config.SHOW_FILE_FORMAT, help="Показать формат файла на первом кадре")
    encode_parser.add_argument("--show-end-frame", type=bool, default=config.SHOW_END_FRAME, help="Показать последний кадр с информацией о файле")



    # Команда decode
    decode_parser = subparsers.add_parser("decode", help="Декодировать видео в файл")
    decode_parser.add_argument("input_video", help="Входное видео (MP4)")
    decode_parser.add_argument("output", help="Выходной файл")
    decode_parser.add_argument("--key", required=True, help="Ключ шифрования (строка)")
    decode_parser.add_argument("--pixel-size", type=int, default=config.PIXEL_SIZE)
    decode_parser.add_argument("--skip-first-frame", type=bool, default=config.SKIP_FIRST_FRAME, help="Пропустить первый кадр при декодировании")
    decode_parser.add_argument("--skip-end-frame", type=bool, default=config.SKIP_END_FRAME, help="Пропустить последний кадр при декодировании")


    args = parser.parse_args()

    if args.command == "encode":
        print(args.key)
        encode_file(args.input, args.output, fps=args.fps, pxl_size=args.pixel_size, video_height=args.height, video_width=args.width,
                show_first_frame=args.show_first_frame, show_file_name=args.show_file_name, show_file_format=args.show_file_format, key=args.key,
                show_end_frame=args.show_end_frame)

    elif args.command == "decode":
        print(args.key)
        decode(args.input_video, save_as=args.output, pxl_size=args.pixel_size,
                skip_first_frame=args.skip_first_frame, key=args.key,
                skip_end_frame=args.skip_end_frame)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
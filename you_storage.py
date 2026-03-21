# # main.py
# import argparse
# import os
# from libs.endoder import encode_file
# from libs.decoder import decode
# from libs.uploader import upload_video
# from libs.downloader import download_video
# import cfg as config


# def main():
#     parser = argparse.ArgumentParser(description="Хранение данных в видео на YouTube")
#     subparsers = parser.add_subparsers(dest="command", help="Команды")

#     # Команда encode
#     encode_parser = subparsers.add_parser("encode", help="Закодировать файл в видео")
#     encode_parser.add_argument("input", help="Входной файл")
#     encode_parser.add_argument("output", help="Выходное видео (MP4)")
#     encode_parser.add_argument("--key", required=True, help="Ключ шифрования (строка)")
#     encode_parser.add_argument("--block-size", type=int, default=config.DEFAULT_BLOCK_SIZE)
#     encode_parser.add_argument("--ecc-symbols", type=int, default=config.DEFAULT_ECC_SYMBOLS)
#     encode_parser.add_argument("--width", type=int, default=config.DEFAULT_RESOLUTION[0])
#     encode_parser.add_argument("--height", type=int, default=config.DEFAULT_RESOLUTION[1])
#     encode_parser.add_argument("--fps", type=int, default=config.DEFAULT_FPS)
#     encode_parser.add_argument("--brightness-levels", type=int, default=config.DEFAULT_BRIGHTNESS_LEVELS)

#     # Команда decode
#     decode_parser = subparsers.add_parser("decode", help="Декодировать видео в файл")
#     decode_parser.add_argument("input_video", help="Входное видео (MP4)")
#     decode_parser.add_argument("output", help="Выходной файл")
#     decode_parser.add_argument("--key", required=True, help="Ключ шифрования (строка)")
#     decode_parser.add_argument("--block-size", type=int, default=config.DEFAULT_BLOCK_SIZE)
#     decode_parser.add_argument("--ecc-symbols", type=int, default=config.DEFAULT_ECC_SYMBOLS)
#     decode_parser.add_argument("--brightness-levels", type=int, default=config.DEFAULT_BRIGHTNESS_LEVELS)

#     # Команда upload
#     upload_parser = subparsers.add_parser("upload", help="Загрузить видео на YouTube")
#     upload_parser.add_argument("video", help="Видеофайл")
#     upload_parser.add_argument("--title", required=True, help="Название видео")
#     upload_parser.add_argument("--description", default="", help="Описание")
#     upload_parser.add_argument("--privacy", default="private", choices=["private", "unlisted", "public"])

#     # Команда download
#     download_parser = subparsers.add_parser("download", help="Скачать видео с YouTube")
#     download_parser.add_argument("url", help="URL видео")
#     download_parser.add_argument("--output", default="downloaded_video.mp4", help="Выходной файл")

#     args = parser.parse_args()

#     if args.command == "encode":
#         encode_file

#     elif args.command == "decode":
#         decode

#     else:
#         parser.print_help()

# if __name__ == "__main__":
#     main()

"""

Пока что запуск только через файлы библиотек. В будущем можно будет добавить интерфейс командной строки, который будет вызывать эти функции с нужными параметрами.

"""
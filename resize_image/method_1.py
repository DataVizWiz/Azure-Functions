import io
import logging
import azure.functions as func
from PIL import Image


def img_stream_to_blob(blobin: func.InputStream, blobout: func.Out[bytes]) -> None:
    output_stream = io.BytesIO()

    with Image.open(blobin) as img:
        img.thumbnail((128, 128))
        img.save(output_stream, format="PNG")

    output_stream.seek(0)
    blobout.set(output_stream.read())


def img_file_to_blob(blobin: func.InputStream, blobout: func.Out[bytes]) -> None:
    output_image = "output.jpg"

    with Image.open(blobin) as img:
        img.thumbnail((128, 128))
        img.save(output_image)

    with open(output_image, mode="rb") as file:
        blobout.set(file.read())


def main(blobin: func.InputStream, blobout: func.Out[bytes]) -> None:
    logging.info("----- Processing image: %s\n", blobin.name)

    img_stream_to_blob(blobin, blobout)

    logging.info("----- Resizing to thumbnail successful")

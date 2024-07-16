import azure.functions as func
import logging
from PIL import Image
import io

STORAGE_ACC = "<storage_acount>_STORAGE"

app = func.FunctionApp()


@app.function_name(name="ImageToThumbnail")
@app.blob_trigger(
    arg_name="myblob", path="landing/images/{name}", connection=STORAGE_ACC
)
@app.blob_output(
    arg_name="outputblob",
    path="transformed/thumbnails/{name}",
    connection=STORAGE_ACC,
)
def blob_trigger(myblob: func.InputStream, outputblob: func.Out[str]):
    logging.info(f"\nBlob Name: {myblob.name}")

    output_stream = io.BytesIO()

    with Image.open(myblob) as img:
        img.thumbnail((128, 128))
        img.save(output_stream, format="PNG")

    output_stream.seek(0)
    outputblob.set(output_stream.read())

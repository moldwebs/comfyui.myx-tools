import base64
from PIL import Image
import torch
import numpy as np
import io


class MyxBase64ImageInput:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "base64_image": ("STRING", {"multiline": False, "default": ""}),
            },
        }

    RETURN_TYPES = ("IMAGE",)

    FUNCTION = "process_input"

    CATEGORY = "Myx-Tools"

    def process_input(self, base64_image):
        if base64_image:
            image_bytes = base64.b64decode(base64_image)

            # Open the image from bytes
            image = Image.open(io.BytesIO(image_bytes))
            image = image.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]

            return (image,)

class MyxBase64Output:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "items": ("ANY",),
            },
        }

    RETURN_TYPES = ()

    FUNCTION = "process_output"

    OUTPUT_NODE = True

    CATEGORY = "Myx-Tools"

    def process_item(self, item):

        with open(item, 'rb') as binary_file:
            binary_file_data = binary_file.read()
            base64_encoded_data = base64.b64encode(binary_file_data)
            base64_output = base64_encoded_data.decode('utf-8')

        return base64_output

    def process_output(self, items: list[torch.Tensor]):
        return {"ui": {"base64_output": [self.process_item(item) for item in items]}}

NODE_CLASS_MAPPINGS = {
    "MyxBase64ImageInput": MyxBase64ImageInput,
    "MyxBase64Output": MyxBase64Output
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "MyxBase64ImageInput": "MyxBase64ImageInput Node",
    "MyxBase64Output": "MyxBase64Output Node"
}

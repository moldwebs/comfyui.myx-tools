import base64
from PIL import Image
import torch
import numpy as np
import io
import folder_paths

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

class MyxBase64ImageOutput:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "field_tag": ("STRING", {
                    "multiline": False,
                    "default": "base64_output"
                }),
            },
        }

    RETURN_TYPES = ()

    FUNCTION = "process_image_output"

    OUTPUT_NODE = True

    CATEGORY = "Myx-Tools"

    def process_image(self, image):
        i = 255.0 * image.cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

        buffered = io.BytesIO()
        img.save(buffered, optimize=False, format="png", compress_level=4)

        base64_image = base64.b64encode(buffered.getvalue()).decode()
        return base64_image

    def process_image_output(self, images: list[torch.Tensor], field_tag):
        if hasattr(images, "__len__"):
            return {"ui": {str(field_tag): [self.process_image(image) for image in images]}}
        else:
            return {"ui": {str(field_tag): [self.process_image(images)]}}


class MyxBase64AudioOutput:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio": ("AUDIO",),
                "field_tag": ("STRING", {
                    "multiline": False,
                    "default": "base64_output"
                }),
            },
        }

    RETURN_TYPES = ()

    FUNCTION = "process_audio_output"

    OUTPUT_NODE = True

    CATEGORY = "Myx-Tools"

    def process_audio(self, audio):

        with open(folder_paths.get_output_directory() + "/" + audio["filename"], 'rb') as binary_file:
            binary_file_data = binary_file.read()
            base64_encoded_data = base64.b64encode(binary_file_data)
            base64_output = base64_encoded_data.decode('utf-8')

        return base64_output

    def process_audio_output(self, audio, field_tag):
        return {"ui": {str(field_tag): [self.process_audio(audio)]}}


class MyxAlwaysEqualProxy(str):
    def __eq__(self, _):
        return True

    def __ne__(self, _):
        return False

class MyxBase64Output:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "ANY": (MyxAlwaysEqualProxy("*"),),
                "field_tag": ("STRING", {
                    "multiline": False,
                    "default": "base64_output"
                }),
            },
        }

    RETURN_TYPES = ()

    FUNCTION = "process_output"

    OUTPUT_NODE = True

    CATEGORY = "Myx-Tools"

    def process_output(self, ANY, field_tag):
        return {"ui": {str(field_tag): ANY}}

NODE_CLASS_MAPPINGS = {
    "MyxBase64ImageInput": MyxBase64ImageInput,
    "MyxBase64ImageOutput": MyxBase64ImageOutput,
    "MyxBase64AudioOutput": MyxBase64AudioOutput,
    "MyxBase64Output": MyxBase64Output
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "MyxBase64ImageInput": "MyxBase64ImageInput Node",
    "MyxBase64ImageOutput": "MyxBase64ImageOutput Node",
    "MyxBase64AudioOutput": "MyxBase64AudioOutput Node",
    "MyxBase64Output": "MyxBase64Output Node"
}

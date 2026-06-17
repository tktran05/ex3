"""
MODULE 2 — Image Captioning  (BLIP / transformers)
--------------------------------------------------
Generates a natural-language description of a football image, e.g.
    "a soccer player celebrating a goal in a stadium"
This caption is fed (with the CV detection) to the text generator.
"""
from __future__ import annotations
from PIL import Image
import config


class CaptionModule:
    def __init__(self, model_name: str | None = None):
        import torch
        from transformers import BlipProcessor, BlipForConditionalGeneration
        name = model_name or config.BLIP_MODEL
        self.device = config.DEVICE
        self.dtype = torch.float16 if self.device == "cuda" else torch.float32
        self.processor = BlipProcessor.from_pretrained(name)
        self.model = BlipForConditionalGeneration.from_pretrained(
            name, torch_dtype=self.dtype
        ).to(self.device)

    def caption(self, image_path, prompt: str | None = None) -> str:
        import torch
        img = Image.open(image_path).convert("RGB")
        if prompt:  # conditional captioning
            inputs = self.processor(img, prompt, return_tensors="pt")
        else:
            inputs = self.processor(img, return_tensors="pt")
        inputs = {k: v.to(self.device, self.dtype if v.is_floating_point() else None)
                  for k, v in inputs.items()}
        with torch.no_grad():
            out = self.model.generate(**inputs, max_new_tokens=40, num_beams=3)
        text = self.processor.decode(out[0], skip_special_tokens=True).strip()
        return text[0].upper() + text[1:] if text else "A football scene."


if __name__ == "__main__":
    import sys
    cm = CaptionModule()
    for p in sys.argv[1:]:
        print(p, "->", cm.caption(p))

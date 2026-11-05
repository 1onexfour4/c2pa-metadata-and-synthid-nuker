import os
import sys
import torch
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline

G, Y, R, C, X = "\033[92m", "\033[93m", "\033[91m", "\033[96m", "\033[0m"

_pipe = None

def get_pipeline():
    global _pipe
    if not _pipe:
        print(f"{Y}[*] loading model into memory...{X}")
        dev = "cuda" if torch.cuda.is_available() else "cpu"
        dt = torch.float16 if dev == "cuda" else torch.float32
        
        _pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            "stabilityai/sd-turbo", dtype=dt, use_safetensors=True, low_cpu_mem_usage=True
        ).to(dev)
        
        _pipe.vae.enable_tiling()
        
        if dev == "cuda":
            torch.backends.cudnn.benchmark = True
            _pipe.unet.to(memory_format=torch.channels_last)
        else:
            print(f"{C}[!] cpu mode, maxing threads{X}")
            torch.set_num_threads(os.cpu_count())
            
    return _pipe

def main():
    if len(sys.argv) < 3:
        print(f"{R}usage: python {sys.argv[0]} <input_file> <output_file>{X}")
        sys.exit(1)

    src, dst = sys.argv[1], sys.argv[2]
    if not os.path.exists(src):
        print(f"{R}err: cant find {src}{X}")
        sys.exit(1)

    print(f"{Y}[*] fixing image dims...{X}")
    img = Image.open(src).convert("RGB")
    w, h = img.size
    nw, nh = (w // 8) * 8, (h // 8) * 8
    if (nw, nh) != (w, h):
        img = img.resize((nw, nh), Image.Resampling.BICUBIC)

    pipe = get_pipeline()

    print(f"{Y}[*] running inference...{X}")
    with torch.inference_mode():
        out = pipe(
            prompt="photorealistic, crisp details",
            image=img,
            strength=0.12,
            guidance_scale=0.0,
            num_inference_steps=10,
        ).images[0]

    out.save(dst, "PNG", compress_level=1)
    print(f"{G}[+] done -> {dst}{X}")

if __name__ == "__main__":
    main()

# c2pa-metadata-and-synthid-nuker

A quick script to strip C2PA metadata and neutralize AI watermarks (like SynthID and C2PA metadata) using a tiny `sd-turbo` diffusion pass. It scrubs the invisible tracking and steganography data while keeping the resultant image looking genuinely near verbatim to the original.

## what it does
- **C2PA Stripping:** Wipes out container headers and content credentials completely.
- **AI Watermark Scrubbing:** Runs a low-strength (`0.12`) `sd-turbo` pass to mess up pixel-level steganographic patterns without trashing your image quality.
- **Low-Memory Friendly:** Uses VAE tiling so it won't crash your CPU or throw OOM errors on restricted containers. (For example, Render.)

## setup

install the requirements:

```bash
pip install -r requirements.txt
```
## usage
run it from your terminal:
```bash
python main.py <input_file> <output_file>
```
## example
```bash
python main.py input.png output.png
```
### supported file extensions: 
 * .bmp
 * .dib
 * .eps
 * .gif
 * .icns
 * .ico
 * .im
 * .jpg
 * .jpeg
 * .msp
 * .pcx
 * .png
 * .ppm
 * .sgi
 * .spider
 * .tga
 * .tiff
 * .webp
 * .xbm
 * .cur
 * .dcx
 * .fits
 * .fli
 * .flc
 * .fpx
 * .gbr
 * .gd
 * .imt
 * .mic
 * .mpo
 * .pcd
 * .pixar
 * .psd
 * .qoi
 * .sun
 * .wal
 * .xpm
 * .avif
 * .blp

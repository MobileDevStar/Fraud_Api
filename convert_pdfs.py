from pdf2image import convert_from_path
import os

def pdfs_to_images(src_dir, dst_dir, size=(224,224)):
    os.makedirs(dst_dir, exist_ok=True)
    for fn in os.listdir(src_dir):
        if not fn.lower().endswith(".pdf"): continue
        pdf_path = os.path.join(src_dir, fn)
        # Convert first page only:
        imgs = convert_from_path(pdf_path, size=size, fmt="png")
        # Save
        img_path = os.path.join(dst_dir, fn.replace(".pdf", ".png"))
        imgs[0].save(img_path, "PNG")

if __name__ == "__main__":
    # Genuine
    pdfs_to_images("data/synth/pdfs/genuine", "data/synth/images/genuine")
    # Fraud
    pdfs_to_images("data/synth/pdfs/fraud",   "data/synth/images/fraud")
    print("PDF → image conversion done.")

import subprocess

""" embed pic wm into pic """

def embed_pic2pic():
    r = subprocess.call([
        "python", "-m", "blind_watermark.cli_tools",
        "--embed",
        "-p", "1x1",
        "../../data/ori_img/ori_img.jpg",
        "../../data/wm_img/watermark.png",
        "../../data/embed_img/embedded.png"])

def extract_pic2pic():
    r = subprocess.call([
        "python", "-m", "blind_watermark.cli_tools",
        "--extract",
        "-p", "1x1",
        "--wm_shape", "128x128",
        "../../data/embed_img/embedded.png",
        "../../data/output/extraction.png"])

def embed_str2pic():
    r = subprocess.call([
        "python", "-m", "blind_watermark.cli_tools",
        "--embed",
        "-s",
        "-p", "1x1",
        "../../data/ori_img/ori_img.jpg",
        "Hello,World.新年快乐！",
        "../../data/embed_img/embedded_str2pic.png"])

def extract_str2pic():
    length = input("\nPlease input the watermark_shape: ")
    r = subprocess.call([
        "python", "-m", "blind_watermark.cli_tools",
        "--extract",
        "-s",
        "-p", "1x1",
        "--wm_shape", length,
        "../../data/embed_img/embedded_str2pic.png",
        "../../data/output/extraction.txt"])

def main():
    # embed_pic2pic()
    # extract_pic2pic()

    embed_str2pic()
    extract_str2pic()

if __name__ == '__main__':
    main()

import cv2
from PIL import Image
def plus(str):
    # 返回指定长度的字符串，原字符串右对齐，前面填充0。
    return str.zfill(8)
def getCode( img):
    str = ""
    # 获取到水印的宽和高进行遍历
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            # 获取水印的每个像素值
            rgb = img.getpixel((i, j))
            # 将像素值转为二进制后保存
            str = str + plus(bin(rgb[0]).replace('0b', ''))
            str = str + plus(bin(rgb[1]).replace('0b', ''))
            str = str + plus(bin(rgb[2]).replace('0b', ''))
    return str

def encry(img, code, embed_pos):
    # 计数器
    count = 0
    # 二进制像素值的长度，可以认为要写入图像的文本长度，提取（解密）时也需要此变量
    codeLen = len(code)

    # 获取到图像的宽、高进行遍历
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            # 获取到图片的每个像素值
            data = img.getpixel((i, j))

            # 如果计数器等于长度，代表水印写入完成
            if count == codeLen:
                break

            # 将获取到的RGB数值分别保存
            r = data[0]
            g = data[1]
            b = data[2]

            """
            下面的是像素值替换，通过取模2得到最后一位像素值（0或1），
            然后减去最后一位像素值，在将code的值添加过来
            """

            r = (r - r % 2) + int(code[count])
            count += 1
            if count == codeLen:
                img.putpixel((i, j), (r, g, b))
                break

            g = (g - g % 2) + int(code[count])
            count += 1
            if count == codeLen:
                img.putpixel((i, j), (r, g, b))
                break

            b = (b - b % 2) + int(code[count])
            count += 1
            if count == codeLen:
                img.putpixel((i, j), (r, g, b))
                break

            # 每3次循环表示一组RGB值被替换完毕，可以进行写入
            if count % 3 == 0:
                img.putpixel((i, j), (r, g, b))
    img.save(embed_pos)


# 获取图像对象
def encry2(ori_pos, left_pos,emb_pos):#总体开始加密，不是实际加密过程
    img1 = Image.open(ori_pos)
    img2 = Image.open(left_pos)

    # 将图像转换为RGB通道，才能分别获取R,G,B的值
    rgb_im1 = img1.convert('RGB')
    rgb_im2 = img2.convert('RGB')

    # 将水印的像素值转为文本
    code = getCode(rgb_im2)

    # 将水印写入图像
    encry(rgb_im1, code,emb_pos)


def deEncry(img, length):
    # 获取图片的宽和高
    width = img.size[0]
    height = img.size[1]

    # 计数器
    count = 0
    # 结果文本，从图片中提取到的附加值（加密时附加在每个RGB通道后的二进制数值）
    wt = ""

    # 遍历图片
    for i in range(width):
        for j in range(height):
            # 获取像素点的值
            rgb = img.getpixel((i, j))

            # 提取R通道的附加值
            if count % 3 == 0:
                count += 1
                wt = wt + str(rgb[0] % 2)
                if count == length:
                    break

            # 提取G通道的附加值
            if count % 3 == 1:
                count += 1
                wt = wt + str(rgb[1] % 2)
                if count == length:
                    break

            # 提取B通道的附加值
            if count % 3 == 2:
                count += 1
                wt = wt + str(rgb[2] % 2)
                if count == length:
                    break
        if count == length:
            break
    return wt


def showImage( wt, img_width, img_height, extract_pos):
    str1 = []
    for i in range(0, len(wt), 8):
        # 以每8位为一组二进制，转换为十进制
        str1.append(int(wt[i:i + 8], 2))
    # 图片大于水印图片1个像素，便于对比
    img_out = Image.new("RGB", (img_width + 1, img_height + 1))
    flag = 0

    for m in range(0, img_width):
        for n in range(0, img_height):
            if flag >= len(str1):
                break
            img_out.putpixel((m, n), (str1[flag], str1[flag + 1], str1[flag + 2]))
            flag += 3
        if flag >= len(str1):
            break
    img_out.save(extract_pos)
    img_out.show()

class st_watermark:
    def __init__(self,abp):
        self.abp = abp

    def cut(self,wm_pos,left_pos,right_pos):
        img = cv2.imread(wm_pos)
        temp = img.shape
        cropped = img[0:int(temp[0]), 0:int(temp[1] / 2)]  # 裁剪坐标为[y0:y1, x0:x1]
        cropped_right = img[0:int(temp[0]), int(temp[1] / 2):]
        cv2.imwrite(left_pos, cropped)
        cv2.imwrite(right_pos, cropped_right)

    def embed(self,ori_pos,left_pos,embed_pos):
        # 获取一下水印图片的宽和高，也就是解密的密钥
        encry2(ori_pos,left_pos,embed_pos)

    def extract(self, embed_pos, ext_pos, image_width=64, image_height=128):
        length = image_width * image_height * 24

        # 获取图片
        img1 = Image.open(embed_pos)
        rgb_im1 = img1.convert('RGB')

        wt = deEncry(rgb_im1, length)
        showImage(wt, image_width, image_height, ext_pos)

# tmp = st_watermark("/Users/alexhan/blind_watermark")
# ori_pos = tmp.abp+"/examples/pic/ori_img.jpg"
# wm_pos = tmp.abp+"/examples/pic/watermark.png"
# left_wm_pos = tmp.abp+"/examples/output/left_wm.png"
# right_wm_pos = tmp.abp+"/examples/output/right_wm.png"
# left_emb_pos = tmp.abp+"/examples/output/left_emb.png"
# left_ext = tmp.abp +"/examples/output/left_ext.png"
# tmp.embed(ori_pos,wm_pos,left_wm_pos,right_wm_pos,left_emb_pos)
# tmp.extract(left_emb_pos,left_ext)
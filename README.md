# blind-watermark

Supports inserting blind watermarks into pictures.

Add support for inserting blind watermarks into text and audio.

Add support for inserting string watermarks in bash.

Add unit tests.

Add test data.

# install
To Users：
```bash
pip install blind-watermark
```

To Developers:
```bach
git clone git@github.com:guofei9987/blind_watermark.git
cd blind_watermark
pip install .
```

## How to use

### Use in bash
```bash
cd examples
# embed watermark into image:
blind_watermark --embed -p 1x1 pic/ori_img.jpg pic/watermark.png output/embedded.png
# extract watermark from image:
blind_watermark --extract -p 1x1 --wm_shape 128x128 output/embedded.png output/wm_extract.png
```

### Use in Python
How to embed watermark:
```python
from blind_watermark import WaterMark

bwm1 = WaterMark(password_wm=1, password_img=1)
# read original image
bwm1.read_img('pic/ori_img.jpg')
# read watermark
bwm1.read_wm('pic/watermark.png')
# embed
bwm1.embed('output/embedded.png')
```


How to extract watermark
```python
bwm1 = WaterMark(password_wm=1, password_img=1)
# notice that wm_shape is necessary
bwm1.extract(filename='output/embedded.png', wm_shape=(128, 128), out_wm_name='output/extracted.png', )
```

## demos:

|origin image|watermark|
|--|--|
|![origin_image](docs/原图.jpg)|![watermark](docs/水印.png)|

|image embedded with watermark|extracted watermark|
|--|--|
|![打上水印的图](docs/打上水印的图.jpg)|![提取的水印](docs/解出的水印.png)|



### Attack on the embedded image


|attack method|image after attack|extracted watermark|
|--|--|--|
|Rotate 45 Degrees<br>[旋转攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/旋转攻击.py)|![旋转攻击](docs/旋转攻击.jpg)|![](docs/旋转攻击_提取水印.png)|
|Many Coverage<br>[多遮挡攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/多遮挡攻击.py)| ![多遮挡攻击](docs/多遮挡攻击.jpg) |![多遮挡_提取水印](docs/多遮挡攻击_提取水印.png)|
|50% Horizontal Crop<br>[横向裁剪攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/横向裁剪攻击.py)|![横向裁剪攻击](docs/横向裁剪攻击.jpg)|![](docs/横向裁剪攻击_提取水印.png)|
|50% Vertical Crop<br>[纵向裁剪攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/纵向裁剪攻击.py)|![纵向裁剪攻击](docs/纵向裁剪攻击.jpg)|![纵向裁剪](docs/纵向裁剪攻击_提取水印.png)|
|Resize（1200X1920->600X800）<br>[缩放攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/缩放攻击.py)|![缩放攻击](docs/缩放攻击.jpg)|![](docs/缩放攻击_提取水印.png)|
|Pepper Noise<br>[椒盐击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/椒盐攻击.py)|![椒盐攻击](docs/椒盐攻击.jpg)|![](docs/椒盐攻击_提取水印.png)|
|Brightness 10% Up<br>[亮度调高攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/亮度调高攻击.py)|![亮度调高攻击](docs/亮度调高攻击.jpg)|![](docs/亮度调高攻击_提取水印.png)|
|Brightness 10% Down<br>[亮度调暗攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/亮度调低攻击.py)|![亮度调低攻击](docs/亮度调低攻击.jpg)|![](docs/亮度调低攻击_提取水印.png)|


### embed string
Embed:
```python
from blind_watermark import WaterMark

bwm1 = WaterMark(password_img=1, password_wm=1)
bwm1.read_img('pic/ori_img.jpg')
wm = '开源万岁！'
bwm1.read_wm(wm, mode='str')
bwm1.embed('output/embedded.png')
len_wm = len(bwm1.wm_bit)
print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))
```

Extract:
```python
bwm1 = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm1.extract('output/embedded.png', wm_shape=len_wm, mode='str')
print(wm_extract)
```
Output:
>开源万岁！

### embed array of bits

As demo, we embed 6 bytes data:
```python
wm = [True, False, True, True, True, False]
```

Embed:
```python
from blind_watermark import WaterMark

bwm1 = WaterMark(password_img=1, password_wm=1)
bwm1.read_ori_img('pic/ori_img.jpg')
bwm1.read_wm([True, False, True, True, True, False], mode='bit')
bwm1.embed('output/embedded.png')
```

Extract:
```python
bwm1 = WaterMark(password_img=1, password_wm=1, wm_shape=6)
wm_extract = bwm1.extract('output/打上水印的图.png', mode='bit')
print(wm_extract)
```
Notice that `wm_shape` (shape of watermark) is necessary

The output `wm_extract` is an array of float. set a threshold such as 0.5.

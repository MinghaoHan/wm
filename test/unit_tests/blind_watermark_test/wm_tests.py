from blind_watermark import WaterMark


def embed_str2pic():
    bwm1 = WaterMark(password_img=1, password_wm=1)
    bwm1.read_img('../../data/ori_img/ori_img.jpg')
    wm = '@NJUSE 开源万岁！'
    bwm1.read_wm(wm, mode='str')
    bwm1.embed('../../data/embed_img/embedded_str2pic.png')
    len_wm = len(bwm1.wm_bit)
    print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))
    return len_wm


def extract_str2pic(len_wm):
    bwm1 = WaterMark(password_img=1, password_wm=1)
    wm_extract = bwm1.extract('../../data/embed_img/embedded_str2pic.png', wm_shape=len_wm, mode='str')
    print(wm_extract)


def embed_pic2pic():
    bwm1 = WaterMark(password_wm=1, password_img=1)
    bwm1.read_img('../../data/ori_img/ori_img.jpg')
    bwm1.read_wm('../../data/wm_img/watermark.png')
    bwm1.embed('../../data/embed_img/embedded.png')
    print("Embedding successfully!")


def extract_pic2pic():
    bwm1 = WaterMark(password_wm=1, password_img=1)
    # notice that wm_shape is necessary
    bwm1.extract(filename='../../data/embed_img/embedded.png', wm_shape=(128, 128), out_wm_name='../../data/output'
                                                                                                '/extracted.png', )
    print("Extraction successfully!")


def main():
    """ test picture blind watermark"""
    embed_pic2pic()
    extract_pic2pic()

    """ test string blind watermark"""
    len_wm = embed_str2pic()
    extract_str2pic(len_wm)


if __name__ == '__main__':
    main()

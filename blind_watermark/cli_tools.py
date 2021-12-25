from optparse import OptionParser
from .blind_watermark import WaterMark
from .text_watermark import TextMark
from .audio_watermark import lsb_watermark, recover_embedded_file
import sys

usage1 = 'blind_watermark --embed -s -p [pwd1]x[pwd2] image.jpg watermark.png(abcd) embed.png'
usage2 = 'blind_watermark --extract -s -p [pwd1]x[pwd2] --wm_shape 128x128 embed.png wm_extract.png(.txt)'
usage3 = 'blind_watermark --embed --text watermark password origin_sentence'
usage4 = 'blind_watermark --extract --text password sentence'
usage5 = 'blind_watermark --embed --audio message inputAudio outputAudio'
usage6 = 'blind_watermark --extract --audio outputAudio'
optParser = OptionParser(usage=usage1 + '\n' + usage2)

optParser.add_option('--embed', dest='work_mode', action='store_const', const='embed'
                     , help='Embed watermark into images')
optParser.add_option('--extract', dest='work_mode', action='store_const', const='extract'
                     , help='Extract watermark from images')

optParser.add_option('--text', dest='text_wm', action='store_true', help='text watermark')
optParser.add_option('--audio', dest='audio_wm', action='store_true', help='audio watermark')
optParser.add_option('-s', '--str', dest='str_wm', action='store_true', help='Watermark is a string')
optParser.add_option('-p', '--pwd', dest='password', help='2 passwords, like 1x1')
optParser.add_option('--wm_shape', dest='wm_shape', help='Watermark shape, like 128x128 or the length of string')
(opts, args) = optParser.parse_args()


def write_file(wm_content, des):
    f = open(des, 'a')
    f.write('\n' + wm_content)
    f.close()


def main():
    if opts.text_wm is False:
        print(opts)
        print(args)
        p1, p2 = opts.password.split('x')
        bwm1 = WaterMark(password_wm=int(p1), password_img=int(p2))

    if opts.work_mode == 'embed':
        if opts.text_wm is True and opts.audio_wm is True:
            print('Error! Usage: ')
            print(usage1)
            print(usage3)
            print(usage5)
            return

        if opts.audio_wm is True:
            cover_audio = args[1]
            output = args[2]
            message = args[0]
            lsb_watermark(cover_audio, message, output)
            print("Embedded successfully. To file: ", output)

        elif opts.text_wm is True:
            sentence = args[2]
            sentence = sentence * 32
            sentence_embed = TextMark.embed(sentence, args[0], args[1])
            print("Embedded successfully.\n" + sentence_embed)
            write_file(sentence_embed, 'examples/output/txt_extract.txt')

        elif not len(args) == 3:
            print('Error! Usage: ')
            print(usage1)
            print(usage3)
            print(usage5)
            return
        elif not opts.str_wm:
            bwm1.read_img(args[0])
            bwm1.read_wm(args[1])
            bwm1.embed(args[2])
            print('Embed succeed! to file ', args[2])
        elif opts.str_wm:
            bwm1.read_img(args[0])
            bwm1.read_wm(args[1], mode='str')
            bwm1.embed(args[2])
            print('Embed succeed! to file ', args[2])
            print('Note! Please Remember the length of wm bit:', len(bwm1.wm_bit))

    if opts.work_mode == 'extract':
        if opts.text_wm is True and opts.audio_wm is True:
            print('Error! Usage: ')
            print(usage2)
            print(usage4)
            print(usage6)
            return

        if opts.text_wm is True:
            print(args[1])
            print(args[0])
            wm_extract = TextMark.extract(args[1], int(args[0]))
            print("Extract successfully.\n" + wm_extract)

        elif opts.audio_wm is True:
            wm = recover_embedded_file(args[0], "")
            print('Extract successfully! Watermark is: ', wm)

        elif not (opts.text_wm is False and len(args) == 2):
            print('Error! Usage: ')
            print(usage2)
            print(usage4)
            print(usage6)
            return

        elif not opts.str_wm:
            shape1, shape2 = opts.wm_shape.split('x')
            bwm1.extract(filename=args[0], wm_shape=(int(shape1), int(shape2)), out_wm_name=args[1])
            print('Extract successfully! to file ', args[1])

        elif opts.str_wm:
            length = opts.wm_shape
            wm = bwm1.extract(filename=args[0], wm_shape=int(length), mode='str')
            write_file(wm, args[1])
            print('Extract successfully! Watermark is  %s, to file %s' % (wm, args[1]))


if __name__ == '__main__':
    main()

'''
python -m blind_watermark.cli_tools --embed -p 1x1 examples/pic/ori_img.jpg examples/pic/watermark.png examples/output/embedded.png
python -m blind_watermark.cli_tools --extract -p 1x1 --wm_shape 128x128 examples/output/embedded.png examples/output/wm_extract.png

python -m blind_watermark.cli_tools --embed -s -p 1x1 examples/pic/ori_img.jpg Hello,World examples/output/embedded.png
python -m blind_watermark.cli_tools --extract -s -p 1x1 --wm_shape 11 examples/output/embedded.png examples/output/wm_extract.png

python -m blind_watermark.cli_tools --embed --text 绝密：今晚9点老地方见 20190808 这句话有水印，你能提取出来吗？
python -m blind_watermark.cli_tools --extract --text 20211216

python -m blind_watermark.cli_tools --embed --audio copyright:alexhan examples/audio/ori.wav examples/output/embedded.wav
python -m blind_watermark.cli_tools --extract --audio examples/output/embedded.wav

cd examples
blind_watermark --embed -p 1x1 pic/ori_img.jpg pic/watermark.png output/embedded.png
blind_watermark --extract -p 1x1 --wm_shape 128x128 output/embedded.png output/wm_extract.png
'''

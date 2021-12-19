import unittest
from blind_watermark import att


class MyTestCase(unittest.TestCase):
    input_filename = "../../examples/output/embedded.png"
    output_file_name = "./output/"

    def test_cut_height(self, ratio=0.8):
        att.cut_att_height(self.input_filename, self.output_file_name + "test_cut_height.png", ratio)

    def test_cut_width(self, ratio=0.8):
        att.cut_att_width(self.input_filename, self.output_file_name + "test_cut_width.png", ratio)

    def test_rot(self, angle=45):
        att.rot_att(self.input_filename, self.output_file_name + "test_rot.png", angle)

    def test_salt_pepper(self, ratio=0.01):
        att.salt_pepper_att(self.input_filename, self.output_file_name + "test_salt_pepper.png", ratio)

    def test_shelter(self, ratio=0.1, n=3):
        att.shelter_att(self.input_filename, self.output_file_name + "test_shelter.png", ratio, n)

    def test_bright(self, ratio=0.8):
        att.bright_att(self.input_filename, self.output_file_name + "test_bright.png", ratio)

    def test_resize(self, out_shape=(500, 500)):
        att.resize_att(self.input_filename, self.output_file_name + "test_resize.png", out_shape)

    def test_anti_cut(self, origin_shape=[500,500]):
        att.anti_cut_att(self.input_filename, self.output_file_name + "test_anti_cut.png", origin_shape)


if __name__ == '__main__':
    unittest.main()

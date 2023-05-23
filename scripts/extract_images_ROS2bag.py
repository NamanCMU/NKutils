import rclpy
import rclpy.node
import sys
import os

import cv2
import cv_bridge

from sensor_msgs.msg import Image

class ExtractImages(rclpy.node.Node):
    def __init__(self):
        super().__init__('extract_images')

        self.get_logger().info("Initializing")

        # Number of the image
        self.seq = 0

        # Filename format
        self.fname_fmt = 'frame%04i_%i.jpg'

        # Parameters
        # self.declare_parameter('do_dynamic_scaling', False)
        self.declare_parameter('img_topic', '')
        self.declare_parameter('id', 1)
        self.declare_parameter('output_dir', './')

        # Getting user parameters
        # self.do_dynamic_scaling = self.get_parameter('do_dynamic_scaling').get_parameter_value().bool_value
        img_topic = self.get_parameter('img_topic').get_parameter_value().string_value
        self.id = self.get_parameter('id').get_parameter_value().integer_value
        self.output_dir = self.get_parameter('output_dir').get_parameter_value().string_value

        # Checking the validity of image topic
        if not img_topic:
            self.get_logger().fatal("Image topic is empty or invalid")
            sys.exit(1)
        
        # Image subscriber
        self.image_subscriber = self.create_subscription(Image, img_topic, self.save, 10)

    def save(self, imgmsg):
        seq = self.seq
        bridge = cv_bridge.CvBridge()

        # Convert from sensor_msgs Image to cv2 image
        img = bridge.imgmsg_to_cv2(imgmsg, desired_encoding='bgr8')

        # channels = imgmsg.shape[2] if imgmsg.ndim == 3 else 1
        # encoding_in = bridge.dtype_with_channels_to_cvtype2(
        #              img.dtype, channels)

        # img = cv_bridge.cvtColorForDisplay(img, encoding_in=encoding_in, encoding_out='bgr8',
        #                                   do_dynamic_scaling=self.do_dynamic_scaling)
                                    
        # Saving the image
        fname = self.fname_fmt % (seq, self.id)
        self.get_logger().info(f'Save Image as {fname}')
        cv2.imwrite(os.path.join(self.output_dir, fname), img)

        self.seq = seq + 1

def main():
    rclpy.init()
    node = ExtractImages()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()

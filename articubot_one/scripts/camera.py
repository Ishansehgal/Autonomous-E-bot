#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import cv2

class WebcamPublisher(Node):
    def __init__(self):
        super().__init__('webcam_publisher')
        self.publisher_ = self.create_publisher(CompressedImage, 'image_topic/compressed', 10)
        self.timer_ = self.create_timer(0.1, self.publish_image)
        self.bridge = CvBridge()
        self.cap = cv2.VideoCapture(2)  # Assuming USB webcam is assigned index 1

    def publish_image(self):
        ret, frame = self.cap.read()
        if ret:
            # Compress the image
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]  # Adjust quality as needed
            _, compressed_img = cv2.imencode('.jpg', frame, encode_param)
            
            # Create the CompressedImage message
            img_msg = CompressedImage()
            img_msg.format = 'jpeg'
            img_msg.data = compressed_img.tobytes()
            
            self.publisher_.publish(img_msg)

def main(args=None):
    rclpy.init(args=args)
    webcam_publisher = WebcamPublisher()
    rclpy.spin(webcam_publisher)
    webcam_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

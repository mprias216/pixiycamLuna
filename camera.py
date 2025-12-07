#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

# PixyCam library
import pixy
from pixy import BlockArray

def main():
    # Start ROS node
    rospy.init_node("pixycam_node")

    # Publisher: sends messages to /pixycam/blocks
    pub = rospy.Publisher("/pixycam/blocks", String, queue_size=10)

    # Had to revive this!
    # Initialize Pixy camera
    pixy.init()
    pixy.change_prog("color_connected_components")

    rospy.loginfo("PixyCam is running...")

    rate = rospy.Rate(10)  # 10 times per second

    while not rospy.is_shutdown():
        # Create an array to store detected objects (blocks)
        blocks = BlockArray(64)

        # Ask PixyCam for detected blocks
        count = pixy.ccc_get_blocks(64, blocks)

        if count > 0:
            # Build a simple text message listing the blocks
            msg = ""
            for i in range(count):
                block = blocks[i]
                msg += f"Block {i}: sig={block.signature}, x={block.x}, y={block.y}\n"
        else:
            msg = "No objects detected"

        # Publish the message
        pub.publish(msg)

        rate.sleep()


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass

import csv
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose as TPose
from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion
from collections import deque
from math import atan2

MAX_DIFF = 0.1


class Pose(TPose):
    def __init__(self, x=0.0, y=0.0, theta=0.0):
        super().__init__(x=x, y=y, theta=theta)
        
    def __repr__(self):
        return f"(x={self.x:.2f}, y={self.y:.2f}, theta={self.theta:.2f})"
    
    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        self.theta += other.theta
        return self
    
    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.theta -= other.theta
        return self
    
    def __eq__(self, other):
        return (
            abs(self.x - other.x) < MAX_DIFF
            and abs(self.y - other.y) < MAX_DIFF
            and abs(self.theta - other.theta) < MAX_DIFF
        )


class MissionControl(deque):
    def __init__(self, csv_file="/home/gustavo/files/pontos.csv"):
        super().__init__()
        with open(csv_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                new_pose = Pose()
                new_pose.x, new_pose.y, new_pose.theta = [float(x) for x in row]
                self.append(new_pose)
                print(len(self))

    def enqueue(self, x):
        super().append(x)

    def dequeue(self):
        return super().popleft()



class TurtleController(Node):
    def __init__(self, mission_control, control_period=0.02):
        super().__init__('turtle_controller')
        self.pose = Pose(x=-40.0)
        self.setpoint = Pose(x=-40.0)
        self.mission_control = mission_control
        self.publisher = self.create_publisher(
            msg_type=Twist,
            topic="/cmd_vel",
            qos_profile=10
        )
        self.subscription = self.create_subscription(
            msg_type=Odometry,
            topic="/odom",
            callback=self.pose_callback,
            qos_profile=10
        )
        self.control_timer = self.create_timer(
                timer_period_sec=control_period,
                callback=self.control_callback
        )

    def control_callback(self):
        if self.pose.x == -40.0:
            self.get_logger().info("Aguardando primeira pose...")
            return

        msg = Twist()
        x_diff = self.setpoint.x - self.pose.x
        y_diff = self.setpoint.y - self.pose.y
        angle = atan2(y_diff, x_diff)
        z_diff = angle - self.pose.theta

        if abs(x_diff) <= MAX_DIFF and abs(z_diff) <= MAX_DIFF:
            msg.linear.x, msg.angular.z = 0.0, 0.0
            self.update_setpoint()
        else:
            if abs(angle-self.pose.theta) <= MAX_DIFF:
                msg.linear.x = 0.5 
            else:
                msg.angular.z = 0.3 if (z_diff) > 0 else -0.3
                
        self.publisher.publish(msg)



    def update_setpoint(self):
        try:
            next_pose = self.mission_control.dequeue()
            self.setpoint.x = next_pose.x
            self.setpoint.y = next_pose.y
            self.get_logger().info(f"Tortugas chegou em {self.pose}, \
                                   andando para {self.setpoint}")
        except IndexError:
            self.get_logger().info(f"Fim da jornada!")
            exit()

    def pose_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        z = msg.pose.pose.position.z
        ang = msg.pose.pose.orientation
        _, _, theta = euler_from_quaternion([ang.x, ang.y, ang.z, ang.w])
        ##self.get_logger().info(f"x={x}, y={y}, theta={theta}")

        self.pose = Pose(x=x, y=y, theta=theta)
        if self.setpoint.x == -40.0:
            self.update_setpoint()


def main(args=None):
    rclpy.init(args=args)
    mc = MissionControl()
    tc = TurtleController(mc)
    rclpy.spin(tc)
    tc.destroy_node()
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()
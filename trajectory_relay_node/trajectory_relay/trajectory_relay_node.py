import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from autoware_planning_msgs.msg import Trajectory

class TrajectoryRelayNode(Node):
    def __init__(self):
        super().__init__('trajectory_relay_node')

        # 1. パラメータの宣言
        self.declare_parameter('input_selector', 0)

        # 2. パラメータ変更時のコールバックを登録
        self.add_on_set_parameters_callback(self.on_parameter_change)

        # トピックパラメータの宣言
        self.declare_parameter('out_topic', '/planning/trajectory')
        self.declare_parameter('in_topic_1', '/planning/trajectory/planning_validator')
        self.declare_parameter('in_topic_2', '/planning/trajectory/diffusion_planner')

        # 出力トピック
        out_topic = self.get_parameter('out_topic').get_parameter_value().string_value
        self.publisher_ = self.create_publisher(Trajectory, out_topic, 1)
        self.get_logger().info(f'[DEBUG] Publishing to topic: {out_topic}')

        # 入力トピック
        in_topic_1 = self.get_parameter('in_topic_1').get_parameter_value().string_value
        in_topic_2 = self.get_parameter('in_topic_2').get_parameter_value().string_value
        self.get_logger().info(f'[DEBUG] Subscribing to topic 1: {in_topic_1}')
        self.get_logger().info(f'[DEBUG] Subscribing to topic 2: {in_topic_2}')

        self.sub_input_1 = self.create_subscription(
            Trajectory, in_topic_1, self.callback_input_1, 1)
        self.sub_input_2 = self.create_subscription(
            Trajectory, in_topic_2, self.callback_input_2, 1)

        self.get_logger().info('Trajectory Relay Node started. Mode: 0 (Disabled)')

    def on_parameter_change(self, params):
        """パラメータが変更されたときに呼ばれるコールバック"""
        for param in params:
            if param.name == 'input_selector':
                val = param.value
                
                # ログ出力用のメッセージ作成
                mode_map = {0: "Disabled", 1: "Planning Validator", 2: "Diffusion Planner"}
                mode_name = mode_map.get(val, f"Unknown({val})")
                
                self.get_logger().info(f'--- Input Selector Switched to: {mode_name} ---')
                
                # バリデーション（0, 1, 2以外は却下する）
                if val not in [0, 1, 2]:
                    self.get_logger().warn(f'Invalid value {val} set to input_selector!')
                    return SetParametersResult(successful=False, reason="Value must be 0, 1, or 2")

        return SetParametersResult(successful=True)

    def get_selector_val(self):
        val = self.get_parameter('input_selector').get_parameter_value().integer_value
        self.get_logger().debug(f'[DEBUG] get_selector_val called, returning: {val}')
        return val

    def callback_input_1(self, msg):
        self.get_logger().debug('[DEBUG] Received message in callback_input_1')
        if self.get_selector_val() == 1:
            self.get_logger().debug('[DEBUG] Publishing message from callback_input_1')
            self.publisher_.publish(msg)

    def callback_input_2(self, msg):
        self.get_logger().debug('[DEBUG] Received message in callback_input_2')
        if self.get_selector_val() == 2:
            self.get_logger().debug('[DEBUG] Publishing message from callback_input_2')
            self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryRelayNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

#include "relay_control_panel.hpp"
#include <QButtonGroup> // 必須：不完全型エラーを防ぐ
#include <rcl_interfaces/srv/set_parameters.hpp>

namespace trajectory_relay_rviz_plugin {

RelayControlPanel::RelayControlPanel(QWidget* parent) : rviz_common::Panel(parent) {
  QVBoxLayout* layout = new QVBoxLayout;
  button_group_ = new QButtonGroup(this);
  button_group_->setExclusive(true);

  // ボタンの見た目を固定するためのスタイルシート
  // Checked（押し込まれた）状態のときは背景色を濃く（あるいはAutowareカラーのオレンジ等に）固定します
  QString button_style = 
    "QPushButton {"
    "  padding: 8px;"
    "  border: 1px solid #555;"
    "  border-radius: 4px;"
    "  background-color: #f0f0f0;" // 通常時
    "}"
    "QPushButton:checked {"
    "  background-color: #ff9d00;" // 押し込まれた時（オレンジ）
    "  color: white;"
    "  border: 2px solid #ff7700;"
    "}"
    "QPushButton:hover {"
    "  background-color: #e0e0e0;" // ホバー時
    "}";

  auto create_relay_button = [&](QString name, int id) {
    QPushButton* btn = new QPushButton(name);
    btn->setCheckable(true);
    btn->setStyleSheet(button_style); // スタイルを適用
    button_group_->addButton(btn, id);
    layout->addWidget(btn);
  };

  create_relay_button("0: Disable", 0);
  create_relay_button("1: Validator", 1);
  create_relay_button("2: Diffusion", 2);

  setLayout(layout);

  connect(button_group_, static_cast<void(QButtonGroup::*)(int)>(&QButtonGroup::idClicked),
          this, &RelayControlPanel::setSelector);
}
void RelayControlPanel::onInitialize() {
  client_node_ = std::make_shared<rclcpp::Node>("relay_plugin_client");
}

void RelayControlPanel::setSelector(int value) {
  // メインのサービス (/trajectory_relay_node)
  auto client = client_node_->create_client<rcl_interfaces::srv::SetParameters>(
      "/trajectory_relay_node/set_parameters");

  // フォールバックサービス (/planning/trajectory_relay_node)
  auto fallback_client = client_node_->create_client<rcl_interfaces::srv::SetParameters>(
      "/planning/trajectory_relay_node/set_parameters");

  // メインサービス待機
  bool main_available = client->wait_for_service(std::chrono::milliseconds(300));

  // フォールバックサービス待機
  bool fallback_available = false;
  if (!main_available) {
    fallback_available = fallback_client->wait_for_service(std::chrono::milliseconds(300));
  }

  if (!main_available && !fallback_available) {
    RCLCPP_WARN(client_node_->get_logger(), "Parameter services not found!");
    return;
  }

  auto request = std::make_shared<rcl_interfaces::srv::SetParameters::Request>();
  rcl_interfaces::msg::Parameter p;
  p.name = "input_selector";
  p.value.type = rcl_interfaces::msg::ParameterType::PARAMETER_INTEGER;
  p.value.integer_value = value;
  request->parameters.push_back(p);

  if (main_available) {
    client->async_send_request(request);
  } else {
    fallback_client->async_send_request(request);
  }
}

} // namespace trajectory_relay_rviz_plugin

#include <pluginlib/class_list_macros.hpp>
PLUGINLIB_EXPORT_CLASS(trajectory_relay_rviz_plugin::RelayControlPanel, rviz_common::Panel)

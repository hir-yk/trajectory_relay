#ifndef RELAY_CONTROL_PANEL_HPP
#define RELAY_CONTROL_PANEL_HPP

#include <rviz_common/panel.hpp>
#include <rclcpp/rclcpp.hpp>
#include <QPushButton>
#include <QVBoxLayout>
#include <QButtonGroup>

namespace trajectory_relay_rviz_plugin {

class RelayControlPanel : public rviz_common::Panel {
  Q_OBJECT
public:
  RelayControlPanel(QWidget* parent = nullptr);
  virtual void onInitialize() override;

protected Q_SLOTS:
  void setSelector(int value);

protected:
  rclcpp::Node::SharedPtr client_node_;
  QButtonGroup* button_group_;
};

} // namespace trajectory_relay_rviz_plugin
#endif

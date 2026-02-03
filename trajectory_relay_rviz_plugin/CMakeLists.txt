cmake_minimum_required(VERSION 3.8)
project(trajectory_relay_rviz_plugin)

# 1. コンパイルオプションの設定
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 2. 依存パッケージのロード
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rviz_common REQUIRED)
find_package(pluginlib REQUIRED)
find_package(rcl_interfaces REQUIRED)

# Qtのロード (ROS 2 Humble以降なら Qt5 または Qt6)
find_package(Qt5 REQUIRED COMPONENTS Widgets)
set(QT_LIBRARIES Qt5::Widgets)

# 3. Qtのメタオブジェクトコンパイル (MOC) の有効化
set(CMAKE_AUTOMOC ON)

# 4. ライブラリの作成
add_library(${PROJECT_NAME} SHARED
  src/relay_control_panel.cpp
  src/relay_control_panel.hpp
)

# インクルードディレクトリの指定
target_include_directories(${PROJECT_NAME} PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)

# リンクするライブラリの指定
target_link_libraries(${PROJECT_NAME}
  ${QT_LIBRARIES}
  rviz_common::rviz_common
  rclcpp::rclcpp
  pluginlib::pluginlib
)

# 5. プラグインの登録
# plugins.description.xml をインストール
pluginlib_export_plugin_description_file(rviz_common plugins.description.xml)

# 6. インストール設定
install(TARGETS ${PROJECT_NAME}
  EXPORT export_${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

install(DIRECTORY include/
  DESTINATION include
)

ament_package()

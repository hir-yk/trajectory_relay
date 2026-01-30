# trajectory_relay

A ROS 2 utility package for **Autoware** that allows dynamic switching between multiple trajectory sources. 

This node acts as a selector/multiplexer, subscribing to different trajectory topics (e.g., from a standard validator and a diffusion-based planner) and relaying the selected one to the main `/planning/trajectory` topic based on a runtime parameter.



## Features

- **Dynamic Switching**: Change the active planner in real-time without restarting the stack.
- **Parameter-driven**: Simple integer-based selection via `input_selector`.
- **Validation**: Rejects invalid parameter values and logs every change with descriptive info.
- **Minimal Latency**: Straightforward relay logic with configurable QoS.

## Prerequisites

- **ROS 2**: Humble / Galactic
- **Autoware**: [autowarefoundation/autoware](https://github.com/autowarefoundation/autoware)
- **Message Types**: `autoware_planning_msgs`

## Installation

1. Clone this repository into your Autoware workspace:
   ```bash
   cd ~/autoware/src/universe/ # or any other src folder
   git clone [https://github.com/hir-yk/trajectory_relay.git](https://github.com/hir-yk/trajectory_relay.git)
      
2. Build the package:Bashcd ~/autoware

   ```bash
   colcon build --symlink-install --packages-select trajectory_relay
   source install/setup.bash


## Usage

1. Launching the Node


Run the relay node with the default configuration (Mode 0: Disabled):

 ```bash
ros2 launch trajectory_relay trajectory_relay.launch.py

```
To start with a specific planner selected (e.g., Diffusion Planner):

```bash
ros2 launch trajectory_relay trajectory_relay.launch.py input_selector:=2
```
   
2. Switching at Runtime

You can switch the input source on the fly using the ROS 2 parameter CLI:

   ```bash
   # Switch to Planning Validator
   ros2 param set /trajectory_relay_node input_selector 1

   # Switch to Diffusion Planner
   ros2 param set /trajectory_relay_node input_selector 2

   # Disable output
   ros2 param set /trajectory_relay_node input_selector 0
   ```

## Configuration

### Parameters

|Name|Type|Default|Description|
|----|----|-------|-----------|
|input_selector|int|0|0: Disabled<BR>1: Planning Validator<BR>2: Diffusion Planner | 

### Topics

|Name|Type|Direction|Description|
|----|----|:-------:|-----------|
|/planning/trajectory/planning_validator|autoware_planning_msgs/msg/Trajectory|Input|Source 1|
|/planning/trajectory/diffusion_planner|autoware_planning_msgs/msg/Trajectory|Input|Source 2|
|/planning/trajectory|autoware_planning_msgs/msg/Trajectory|Output|The relayed trajectory|

## License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.

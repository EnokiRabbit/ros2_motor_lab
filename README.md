# ROS 2 Motor Lab

一个面向入门学习的 ROS 2 电机闭环控制项目。目前不依赖真实硬件：控制器通过 ROS 2 topic 向电机仿真器发送电压，仿真器返回电机转速。

## 你会练到什么

- ROS 2 工作空间、Python package、节点、topic、参数和 launch
- PI 速度闭环控制、限幅与积分抗饱和
- 电机命令和反馈之间的通信边界
- Git 的基本开发流程
- 后续将仿真器替换成 UART、RS-485/Modbus 或 CAN 驱动

## 数据流

```text
/motor/target_velocity (rad/s)
           |
           v
  motor_controller  <--- /motor/measured_velocity (rad/s)
           |
           v
/motor/command_voltage (V)
           |
           v
    motor_simulator
```

## 构建

```bash
cd ~/Documents/Codex/2026-09-29/ni-2/outputs/ros2_motor_lab
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
```

每次修改 Python 代码后，因为使用了 `--symlink-install`，通常无需重新构建；修改 package 元数据或 launch/config 文件后建议重新构建。

## 运行

终端 1：

```bash
source /opt/ros/jazzy/setup.bash
cd ~/Documents/Codex/2026-09-29/ni-2/outputs/ros2_motor_lab
source install/setup.bash
ros2 launch motor_control_demo motor_lab.launch.py
```

终端 2，发送目标转速 20 rad/s：

```bash
source /opt/ros/jazzy/setup.bash
cd ~/Documents/Codex/2026-09-29/ni-2/outputs/ros2_motor_lab
source install/setup.bash
ros2 topic pub --once /motor/target_velocity std_msgs/msg/Float64 '{data: 20.0}'
```

观察反馈：

```bash
ros2 topic echo /motor/measured_velocity
ros2 topic echo /motor/command_voltage
```

也可以检查通信图和参数：

```bash
ros2 node list
ros2 topic list -t
ros2 node info /motor_controller
ros2 param list /motor_controller
```

如果看到 `Unable to connect to a Zenoh router`，请在另一个终端启动当前系统配置所需的路由器：

```bash
source /opt/ros/jazzy/setup.bash
ros2 run rmw_zenoh_cpp rmw_zenohd
```

停止电机：

```bash
ros2 topic pub --once /motor/target_velocity std_msgs/msg/Float64 '{data: 0.0}'
```

## 调参实验

参数位于 `src/motor_control_demo/config/motor_lab.yaml`。

1. 先将 `ki` 设为 `0.0`，观察只有比例控制时的稳态误差。
2. 恢复 `ki`，观察积分项如何消除误差。
3. 增大 `kp`，观察响应加快以及可能出现的振荡。
4. 修改仿真器的 `time_constant`，模拟惯量不同的电机。
5. 将目标转速设得很高，观察 12 V 电压限幅。

运行测试：

```bash
source /opt/ros/jazzy/setup.bash
colcon test --event-handlers console_direct+
colcon test-result --verbose
```

## 建议学习路线

1. **当前阶段：ROS 2 + 闭环基础** — 跑通工程，使用 `ros2 topic` 和参数调节 PI。
2. **串口通信** — 新增 driver 节点，使用 USB-UART 发送目标值并读取编码器；先设计帧头、长度、命令、数据、CRC。
3. **RS-485/Modbus** — 学习差分信号、半双工、站号、寄存器和超时重试。
4. **CAN 总线** — 学习仲裁 ID、数据帧、波特率、终端电阻、SocketCAN；让 driver 节点把 ROS 2 topic 转换成 CAN 帧。
5. **真实控制器** — 加入编码器换算、控制周期监测、失联停机、过流/过温保护和急停。
6. **ros2_control** — 理解 hardware interface、controller manager 和标准速度控制器后，再将当前 demo 迁移过去。

> 接真电机前请先架空轮子或卸载负载，设置低电流/低电压限制，并准备物理急停。软件停止不能替代硬件保护。

## Git 练习

仓库已初始化并有首个提交。推荐每次只完成一个小实验：

```bash
git status
git switch -c experiment/tune-pi
git add src/motor_control_demo/config/motor_lab.yaml
git commit -m "experiment: tune PI gains"
git log --oneline --graph --decorate
```

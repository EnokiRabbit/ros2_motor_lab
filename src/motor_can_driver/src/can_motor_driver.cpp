#include <memory>
#include <functional>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64.hpp"
using namespace std;

class CanMotorDriver: public rclcpp::Node
{
    private:
    rclcpp::Subscription<std_msgs::msg::Float64>::SharedPtr
        voltage_subscription_;
    public:
    //"Functions without declarations are defaulted "private""
    CanMotorDriver():Node("can_motor_driver")
    {
        voltage_subscription_ =
            this->create_subscription<std_msgs::msg::Float64>(
                "/motor/command_voltage",
                10,
                std::bind(
                    &CanMotorDriver::voltage_callback,
                    this,
                    std::placeholders::_1));

    }

    void voltage_callback(std_msgs::msg::Float64::ConstSharedPtr msg)
    {
        const double voltgate = msg->data;
        RCLCPP_INFO(this->get_logger(),"receive voltgate : %.3f V",voltgate);
    }
};



int main(int argc,char * argv[])
{
    rclcpp::init(argc,argv);
    auto motor_driver_node = std::make_shared<CanMotorDriver>();
    rclcpp::spin(motor_driver_node);
    rclcpp::shutdown();
}

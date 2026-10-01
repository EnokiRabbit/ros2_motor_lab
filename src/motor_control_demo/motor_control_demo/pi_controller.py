class PIController:
    """PI controller with output saturation and simple anti-windup."""

    def __init__(self, kp: float, ki: float, output_limit: float) -> None:
        if output_limit <= 0.0:
            raise ValueError('output_limit must be positive')
        self.kp = kp
        self.ki = ki
        self.output_limit = output_limit
        self.integral = 0.0

    def reset(self) -> None:
        self.integral = 0.0

    def update(self, error: float, dt: float) -> float:
        if dt <= 0.0:
            raise ValueError('dt must be positive')
        #累计误差 = 原累计误差 + 当前误差 × 时间间隔
        #输出电压 = Kp × 当前误差 + Ki × 累计误差
        candidate_integral = self.integral + error * dt
        candidate_output = self.kp * error + self.ki * candidate_integral
        saturated_output = max(
            -self.output_limit, 
            min(self.output_limit, candidate_output),
        )
    
        # Only integrate when unsaturated, or when the error drives the output
        # back toward the permitted range.
        is_unsaturated = candidate_output == saturated_output  #积分抗饱和
        drives_back = (
            candidate_output > self.output_limit and error < 0.0
        ) or (
            candidate_output < -self.output_limit and error > 0.0
        )
        if is_unsaturated or drives_back:
            self.integral = candidate_integral

        return saturated_output


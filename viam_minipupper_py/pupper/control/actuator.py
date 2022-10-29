class ActuatorControl:

    actuator_names = {
        1: "pwm1",
        2: "pwm2",
        3: "pwm3",
    }

    def __init__(self, pwm_number):
        self.pwm_number = pwm_number
        self.actuator_name = self.actuator_names[pwm_number]

    def updateDutyCycle(self, angle: float) -> int:
        return int((1.11 * angle + 50) * 10000)

    def updateActuatorAngle(self, angle):
        duty_cycle = self.updateDutyCycle(angle)
        file_node = f"/sys/class/pwm/pwmchip0/{self.actuator_name}/duty_cycle"
        with open(file_node, "w") as f:
            f.write(str(duty_cycle))

class DeviceController:
    def execute(self, device_id, command):
        print(f"Executing command for device {device_id}: {command}")
        print("MQTT simulation: publishing to topic iot/{deviceId}/command")

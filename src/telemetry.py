class TelemetryStorage:
    def __init__(self):
        self.data = []

    def save(self, packet):
        print("Saving telemetry:", packet)
        self.data.append(packet)

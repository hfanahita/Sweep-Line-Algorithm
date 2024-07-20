class Event:
    def __init__(self, x, y, event_type, is_processed, index, s1_index=None, s2_index=None):
        self.x = x
        self.y = y
        self.event_type = event_type  # "Start", "End", or "Intersection"
        self.is_processed = is_processed
        self.index = index  # Index of the segment for "Start" and "End" events
        self.s1_index = s1_index  # Index of the first segment for "Intersection" events
        self.s2_index = s2_index  # Index of the second segment for "Intersection" events

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def __repr__(self):
        return f"Event(x={self.x}, y={self.y}, type={self.event_type}, index={self.index}, s1_index={self.s1_index}, s2_index={self.s2_index})"

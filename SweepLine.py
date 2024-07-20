from collections import namedtuple
import heapq
from Event import Event
from AVLTree import AVLTree
from Segment import *
from Point import *


def on_segment(p, q, r):
    return (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and
            q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y))


def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2


def do_intersect(s1, s2):
    p1, q1 = s1.start, s1.end
    p2, q2 = s2.start, s2.end

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(p1, p2, q1):
        return True

    if o2 == 0 and on_segment(p1, q2, q1):
        return True

    if o3 == 0 and on_segment(p2, p1, q2):
        return True

    if o4 == 0 and on_segment(p2, q1, q2):
        return True

    return False


def find_intersection(s1, s2):
    p1, q1 = s1.start, s1.end
    p2, q2 = s2.start, s2.end

    A1 = q1.y - p1.y
    B1 = p1.x - q1.x
    C1 = A1 * p1.x + B1 * p1.y

    A2 = q2.y - p2.y
    B2 = p2.x - q2.x
    C2 = A2 * p2.x + B2 * p2.y

    determinant = A1 * B2 - A2 * B1
    if determinant == 0:
        return None  # parallel lines
    else:
        x = (B2 * C1 - B1 * C2) / determinant
        y = (A1 * C2 - A2 * C1) / determinant
        return Point(x, y)


def is_intersect(segments):
    events = []
    for i, seg in enumerate(segments):
        events.append(Event(seg.start.x, seg.start.y, "Start", False, i))
        events.append(Event(seg.end.x, seg.end.y, "End", False, i))

    heapq.heapify(events)

    active_segments = AVLTree()
    intersections = 0
    checked_pairs = set()

    while events:
        event = heapq.heappop(events)
        index = event.index

        if event.event_type == "Start":
            active_segments.insert((event.y, event.x, event.index))

            prev_event = active_segments.predecessor((event.y, event.x, event.index))
            next_event = active_segments.successor((event.y, event.x, event.index))

            if prev_event and do_intersect(segments[prev_event[2]], segments[event.index]):
                pair = (min(prev_event[2], event.index), max(prev_event[2], event.index))
                if pair not in checked_pairs:
                    checked_pairs.add(pair)
                    intersection_point = find_intersection(segments[prev_event[2]], segments[event.index])
                    if intersection_point:
                        print(
                            f"Intersection found between segment {prev_event[2]} and segment {event.index} at {intersection_point}")
                        intersections += 1
                        heapq.heappush(events, Event(intersection_point.x, intersection_point.y, "Intersection", False,
                                                     prev_event[2], event.index))

            if next_event and do_intersect(segments[next_event[2]], segments[event.index]):
                pair = (min(next_event[2], event.index), max(next_event[2], event.index))
                if pair not in checked_pairs:
                    checked_pairs.add(pair)
                    intersection_point = find_intersection(segments[next_event[2]], segments[event.index])
                    if intersection_point:
                        print(
                            f"Intersection found between segment {next_event[2]} and segment {event.index} at {intersection_point}")
                        intersections += 1
                        heapq.heappush(events, Event(intersection_point.x, intersection_point.y, "Intersection", False,
                                                     next_event[2], event.index))

        elif event.event_type == "End":
            active_segments.delete((segments[index].start.y, segments[index].start.x, index))

            prev_event = active_segments.predecessor((segments[index].start.y, segments[index].start.x, index))
            next_event = active_segments.successor((segments[index].start.y, segments[index].start.x, index))

            if prev_event and next_event and do_intersect(segments[prev_event[2]], segments[next_event[2]]):
                pair = (min(prev_event[2], next_event[2]), max(prev_event[2], next_event[2]))
                if pair not in checked_pairs:
                    checked_pairs.add(pair)
                    intersection_point = find_intersection(segments[prev_event[2]], segments[next_event[2]])
                    if intersection_point:
                        print(
                            f"Intersection found between segment {prev_event[2]} and segment {next_event[2]} at {intersection_point}")
                        intersections += 1
                        heapq.heappush(events, Event(intersection_point.x, intersection_point.y, "Intersection", False,
                                                     prev_event[2], next_event[2]))

        elif event.event_type == "Intersection":
            s1_index, s2_index = event.index, event.s1_index

            active_segments.delete((segments[s1_index].start.y, segments[s1_index].start.x, s1_index))
            active_segments.delete((segments[s2_index].start.y, segments[s2_index].start.x, s2_index))

            active_segments.insert((segments[s2_index].start.y, segments[s2_index].start.x, s2_index))
            active_segments.insert((segments[s1_index].start.y, segments[s1_index].start.x, s1_index))

            prev_event = active_segments.predecessor((segments[s2_index].start.y, segments[s2_index].start.x, s2_index))
            next_event = active_segments.successor((segments[s1_index].start.y, segments[s1_index].start.x, s1_index))

            if prev_event and do_intersect(segments[prev_event[2]], segments[s2_index]):
                pair = (min(prev_event[2], s2_index), max(prev_event[2], s2_index))
                if pair not in checked_pairs:
                    checked_pairs.add(pair)
                    intersection_point = find_intersection(segments[prev_event[2]], segments[s2_index])
                    if intersection_point:
                        print(
                            f"Intersection found between segment {prev_event[2]} and segment {s2_index} at {intersection_point}")
                        intersections += 1
                        heapq.heappush(events, Event(intersection_point.x, intersection_point.y, "Intersection", False,
                                                     prev_event[2], s2_index))

            if next_event and do_intersect(segments[next_event[2]], segments[s1_index]):
                pair = (min(next_event[2], s1_index), max(next_event[2], s1_index))
                if pair not in checked_pairs:
                    checked_pairs.add(pair)
                    intersection_point = find_intersection(segments[next_event[2]], segments[s1_index])
                    if intersection_point:
                        print(
                            f"Intersection found between segment {next_event[2]} and segment {s1_index} at {intersection_point}")
                        intersections += 1
                        heapq.heappush(events, Event(intersection_point.x, intersection_point.y, "Intersection", False,
                                                     next_event[2], s1_index))

    # for pair in checked_pairs:
    #     print(f"Line: {pair[0] + 1} {pair[1] + 1}")

    return intersections


# Example usage:
segments = [
    Segment(Point(1, 1), Point(4, 4)),
    Segment(Point(2, 1), Point(3, 5)),
    Segment(Point(1, 7), Point(3, 8)),
    Segment(Point(0, 4), Point(5, 4))
]

print(f"Total intersections: {is_intersect(segments)}")

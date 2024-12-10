from shapely.geometry import Point, Polygon
import math
import shapely


def sector(center, start_angle, end_angle, radius, steps=200):
    def polar_point(origin_point, angle, distance):
        return [origin_point.x + math.cos(math.radians(angle)) * distance,
                origin_point.y - math.sin(math.radians(angle)) * distance]

    if start_angle > end_angle:
        raise Exception("起始角度必须小于结束角度!")
    step_angle_width = (end_angle - start_angle) / steps
    sector_width = (end_angle - start_angle)
    segment_vertices = []

    segment_vertices.append(polar_point(center, 0, 0))
    segment_vertices.append(polar_point(center, start_angle, radius))

    for z in range(1, steps):
        segment_vertices.append((polar_point(center, start_angle + z * step_angle_width, radius)))
    segment_vertices.append(polar_point(center, start_angle + sector_width, radius))
    return Polygon(segment_vertices)


def p_intersection(x0, y0, start_angle0, end_angle0, r0, x1, y1, start_angle1, end_angle1, r1):
    center0 = Point(x0, y0)
    center1 = Point(x1, y1)
    polygon1 = sector(center0, start_angle0, end_angle0, r0)
    polygon2 = sector(center1, start_angle1, end_angle1, r1)
    p2 = shapely.intersection(polygon1, polygon2)
    return p2.area / polygon2.area


if __name__ == '__main__':
    # print(p_intersection(627641.344869, -3758153.5681978385, 196.25, 293.75, 3000, 624673.492832, -3755990.1709158905,
    #                      -180, 180.0, 200))

    print(sector(Point(627641.344869, -3758153.5681978385), 196.25, 293.75, 3000))

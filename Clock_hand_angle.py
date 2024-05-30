



def clock_hands_angle(hours, minutes):
    hours %= 12
    minutes %= 60

    Hour_division_angle = (360/(60 * 12))

    angle_min = (minutes * 6) % 360

    angle_hours = ((hours * 60) + minutes ) * Hour_division_angle

    angle = angle_hours - angle_min

    angle0 = (360 - angle) % 360
    angle1 = (360 - angle0) % 360
    
    return (max(angle0,angle1),min(angle0,angle1))


maxangle,minangle = clock_hands_angle(3, 15)

print(f"Max angle {maxangle}, Min angle {minangle}")



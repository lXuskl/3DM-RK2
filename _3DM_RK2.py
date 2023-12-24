import time
import random

def cohen_sutherland(xmin, ymin, xmax, ymax, num_segments):
    INSIDE = 0  # 0000
    LEFT = 1    # 0001
    RIGHT = 2   # 0010
    BOTTOM = 4  # 0100
    TOP = 8     # 1000

    def compute_outcode(x, y):
        code = INSIDE
        if x < xmin:
            code |= LEFT
        elif x > xmax:
            code |= RIGHT
        if y < ymin:
            code |= BOTTOM
        elif y > ymax:
            code |= TOP
        return code

    def cohen_sutherland_clip(x1, y1, x2, y2):
        code1 = compute_outcode(x1, y1)
        code2 = compute_outcode(x2, y2)
        accept = False

        while True:
            if not (code1 | code2):  # оба отрезка внутри окна
                accept = True
                break
            elif code1 & code2:  # оба отрезка снаружи окна
                break
            else:
                x = 0.0
                y = 0.0
                outcode_out = code1 if code1 > code2 else code2

                if outcode_out & TOP:  # отсекаем верхний край
                    x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                    y = ymax
                elif outcode_out & BOTTOM:  # отсекаем нижний край
                    x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                    y = ymin
                elif outcode_out & RIGHT:  # отсекаем правый край
                    y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                    x = xmax
                elif outcode_out & LEFT:  # отсекаем левый край
                    y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                    x = xmin

                if outcode_out == code1:
                    x1 = x
                    y1 = y
                    code1 = compute_outcode(x1, y1)
                else:
                    x2 = x
                    y2 = y
                    code2 = compute_outcode(x2, y2)

        if accept:
            return True, x1, y1, x2, y2
        else:
            return False, 0, 0, 0, 0

    # Генерация случайных отрезков
    lines = [(random.uniform(-100, 100), random.uniform(-100, 100), random.uniform(-100, 100), random.uniform(-100, 100)) for _ in range(num_segments)]

    start_time = time.time()
    for line in lines:
        x1, y1, x2, y2 = line
        clipped, x1, y1, x2, y2 = cohen_sutherland_clip(x1, y1, x2, y2)
    end_time = time.time()

    execution_time = end_time - start_time
    return execution_time

# Пример использования:
num_segments = 1000000  # или 10000000
xmin, ymin, xmax, ymax = -50, -50, 50, 50  # задаем окно для отсечения

execution_time = cohen_sutherland(xmin, ymin, xmax, ymax, num_segments)
print(f"The speed of the algorithm for {num_segments} segments: {execution_time} seconds")

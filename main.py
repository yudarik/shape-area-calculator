import csv
import abc
import os


class Shape(abc.ABC):
    id: int
    vertices: list[tuple[float, float]]

    def __init__(self, vertices: list[tuple[float, float]]):
        self.id = id(self)
        self.vertices = vertices

    def __str__(self):
        return ';'.join([f'({x},{y})' for x, y in self.vertices])

    def area(self):
        n = len(self.vertices)
        if n < 3:
            raise ValueError("Not enough vertices to calculate area")

        area = 0.0
        i = 0
        while True:
            x0, y0 = self.vertices[i]
            x1, y1 = self.vertices[(i + 1) % n]
            area += x0 * y1 - x1 * y0

            if i == n - 1:
                break
            i += 1

        return abs(area) / 2.0

    def circumference(self):
        n = len(self.vertices)
        if n < 3:
            raise ValueError("Not enough vertices to calculate circumference")

        circumference = 0.0
        i = 0
        while True:
            x0, y0 = self.vertices[i]
            x1, y1 = self.vertices[(i + 1) % n]
            circumference += ((x0 - x1) ** 2 + (y0 - y1) ** 2) ** 0.5

            if i == n - 1:
                break
            i += 1

        return circumference

    def affine_transform(self, transformation_matrix: list[list[float]]):
        # transform vertices using transformation matrix of 3x3 as introduced in the following lecture:
        # https://www.khanacademy.org/math/algebra-home/alg-matrices/alg-matrices-as-transformations/v/matrix-transformation-triangle

        transformed_vertices = []
        for i in range(len(self.vertices)):
            x, y = self.vertices[i]
            transformed_vertices.append((
                transformation_matrix[0][0] * x + transformation_matrix[0][1] * y + transformation_matrix[0][2],
                transformation_matrix[1][0] * x + transformation_matrix[1][1] * y + transformation_matrix[1][2],
            ))

        return Shape(transformed_vertices)


def create_shape(row):
    vertices = []
    for i in range(len(row)):
        pair = row[i].split(';')
        if len(pair) != 2:
            continue
        try:
            x, y = float(pair[0]), float(pair[1])
            vertices.append((x, y))
        except ValueError:
            continue
    return Shape(vertices)


def parse_csv(path: str):
    shapes: list[Shape] = []
    areas: list[tuple[int, float]] = []
    circumferences: list[tuple[int, float]] = []

    try:
        with open(path, newline='') as csvfile:
            # skip header
            next(csvfile)
            reader = csv.reader(csvfile, delimiter=',')

            for row in reader:
                shape = create_shape(row)
                if shape:
                    shapes.append(shape)

            for shape in shapes:
                try:
                    areas.append((shape.id, shape.area()))
                    circumferences.append((shape.id, shape.circumference()))
                except ValueError:
                    continue

            areas = sorted(areas, key=lambda x: x[1], reverse=True)
            circumferences = sorted(circumferences, key=lambda x: x[1], reverse=True)

            # print areas and circumferences
            for i in range(10):
                print(f"{i + 1}) Area: {areas[i][1]:.2f}, Circumference: {circumferences[i][1]:.2f}")
            print('\n\n')
            # transform first shape by the following matrix:
            # [[1, 0, 1],[-1, 1, 2],[0, 0, 1]]
            transformation_matrix = [[4, 0, -3], [-1, 2, 2], [0, 0, 1]]

            # Transform the biggest area shape
            shape_id = areas[0][0]
            for shape in shapes:
                if shape.id == shape_id:
                    transformed_shape = shape.affine_transform(transformation_matrix)
                    print(f"Transformed shape: {transformed_shape}\n")
                    print(f"Transformed shape area: {transformed_shape.area():.2f}")
                    break

            return 0

    except FileNotFoundError:
        print("File not found")
        return 1


if __name__ == '__main__':

    os.close(parse_csv('hw.csv'))

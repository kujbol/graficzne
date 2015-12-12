from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Ellipse


POINT_SIZE = 10
POINT_COLOR = Color(1, 1, 0)


def draw_point(point):
    token = str(hash(point))
    group = InstructionGroup(group=token)
    point.obj.widget.canvas.remove_group(token)
    x, y = point.x, point.y

    if point.texture is not None:
        group.add(
        Ellipse(
            pos=(x - point.size/2, y - point.size/2),
            size=(point.size, point.size),
            texture=point.texture
        )
    )
    else:
        group.add(POINT_COLOR)
        group.add(
            Ellipse(
                pos=(x - point.size/2, y - point.size/2),
                size=(point.size, point.size)
            )
        )

    point.obj.widget.canvas.add(group)

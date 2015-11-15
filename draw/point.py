from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Ellipse


POINT_SIZE = 10
POINT_COLOR = Color(1, 1, 0)


def draw_point(point):
    token = str(hash(point))
    group = InstructionGroup(group=token)
    point.obj.widget.canvas.remove_group(token)

    group.add(POINT_COLOR)
    x, y = point.x, point.y
    group.add(
        Ellipse(
            pos=(x - POINT_SIZE/2, y - POINT_SIZE/2),
            size=(POINT_SIZE, POINT_SIZE)
        )
    )

    point.obj.widget.canvas.add(group)

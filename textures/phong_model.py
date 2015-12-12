from calculations.vec3d import Vec3d


SPECULAR = 850
DIFFUSE = 1200
AMBIENT = 0.2
SHINE = 128

def get_light_phong(x, y, viewer, lights, norm=None):
    return (
        AMBIENT + diffuse_light(x, y, viewer, lights, norm=norm) +
        specular_light(x, y, viewer, lights, norm=norm)
    )


def specular_light(x, y, viewer, lights, norm=None):
    if norm is not None:
        n = norm
    else:
        n = Vec3d(0, 0, 1)
    l = Vec3d(
        lights[0].point.x - x, lights[0].point.y - y, lights[0].settings.height
    )
    dist = l.get_length()
    l = l.normalized()
    return (max(n.dot(l), 0) * SPECULAR) / dist


def diffuse_light(x, y, viewer, lights, norm=None):
    # if norm is not None:
    #     n = norm
    # else:
    n = Vec3d(0, 0, 1)
    l = Vec3d(
        lights[0].point.x - x, lights[0].point.y - y, lights[0].settings.height
    )
    dist = l.get_length()
    l = l.normalized()
    r = 2*(n.dot(l))*n - l
    v = Vec3d(
        viewer.point.x - x, viewer.point.y - y, viewer.settings.height
    )
    v = v.normalized()
    return (max(r.dot(v)**SHINE, 0) * DIFFUSE) / dist

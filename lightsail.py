from vpython import *
import random

# 1. PHYSICAL CONSTANTS
c = 2.998e8                      # Speed of light (m/s) 2.998 x 10^8 
dist_pc_m = 4.01e16              # Earth → Proxima Centauri (m) (giga meters) 
m_sail = 0.002                   # Mass: 2g
laser_power = 1e11              # 100 GW laser
reflectivity = 0.99
a = 2 * laser_power * reflectivity / (m_sail * c)
v_target = 0.2 * c

Lscale = 1e11  # 1 unit = 100 billion meters
def m_to_scene(x): return x / Lscale
dist_pc_su = m_to_scene(dist_pc_m)

scene.title = "Light Sail to Proxima Centauri b"
scene.width = 1200
scene.height = 700
scene.background = color.black
scene.range = 80
scene.forward = vector(-1, -0.2, -0.1)

star_count = 3000  # Densest yet
starfield_range = dist_pc_su + 300
for i in range(star_count):
    star = sphere(
        pos=vector(random.uniform(-100, starfield_range),
                   random.uniform(-150, 150),
                   random.uniform(-150, 150)),
        radius=random.uniform(0.05, 0.13),
        color=vector(random.uniform(0.6, 1),
                     random.uniform(0.6, 1),
                     1),
        emissive=True,
        opacity=random.uniform(0.3, 1)
    )

star_pos = vector(dist_pc_su, 0, 0)
proxima = sphere(pos=star_pos, radius=12,  # ← larger and brighter!
                 color=vector(1, 0.35, 0.35),
                 emissive=True, shininess=1.0)
halo = sphere(pos=star_pos, radius=20,
              color=vector(1, 0.1, 0.1),
              opacity=0.15, emissive=True)

# Proxima Centauri b
orbit_radius = 8
orbit_angle = 0
proxima_b = sphere(pos=proxima.pos + vector(orbit_radius, 0, 0),
                   radius=2.2,
                   color=vector(0.5, 1, 0.5),
                   emissive=True,
                   make_trail=True)
label(pos=proxima_b.pos + vector(0, 3, 0),
      text='Proxima Centauri b', box=False,
      color=color.green)

sail = cone(pos=vector(0, 0, 0), axis=vector(4, 0, 0),
            radius=1.5, color=color.cyan,
            emissive=True, make_trail=True)
payload = sphere(pos=sail.pos + sail.axis,
                 radius=0.7, color=color.white,
                 emissive=True)

laser_src = vector(-10, 0, 0)
laser = cylinder(pos=laser_src,
                 axis=sail.pos - laser_src,
                 radius=0.2, color=color.red,
                 opacity=0.3, emissive=True)

distant_light(direction=vector(-1, 0, 0),
              color=vector(1, 0.2, 0.2))

x_m = 0
v_mps = 0
t = 0
t_laser = 0
dt_real = 1000
laser_on = True


info = label(pos=sail.pos + vector(0, 25, 0),
             text='', height=14, box=False,
             color=color.white, opacity=0)

while m_to_scene(x_m) < dist_pc_su:
    rate(100)

    # Physics
    if laser_on:
	while v_mps + a * dt_real >= v_target:
               dt_real /= 2
        v_mps += a * dt_real
        if v_mps >= v_target:
            laser_on = False
            laser.visible = False
            current_a = 0
        else:
            current_a = a
    else:
        current_a = 0

    x_m += v_mps * dt_real
    t += dt_real

        sail.pos.x = m_to_scene(x_m)
    payload.pos.x = sail.pos.x + sail.axis.x
    laser.axis = sail.pos - laser_src
    scene.center = sail.pos + vector(10, 0, 0)
    info.pos = sail.pos + vector(0, 25, 0)

    # Orbiting planet
    orbit_angle += 0.002
    proxima_b.pos = proxima.pos + vector(
        orbit_radius * cos(orbit_angle),
        0,
        orbit_radius * sin(orbit_angle)
    )

      info.text = (
        "Time: " + str(round(t / 86400, 1)) + " days\n" +
        "Velocity: " + str(round(v_mps / 1000, 2)) + " km/s (" +
        str(round(v_mps / c * 100, 2)) + "% c)\n" +
        "Accel: {:.4e}".format(current_a) + " m/s²\n" +
        "Distance: " + str(round(x_m / 1e9, 1)) + " Gm (" +
        str(round(x_m / dist_pc_m * 100, 4)) + "%)"
    )

info.text += "\n\nARRIVED at Proxima Centauri b"

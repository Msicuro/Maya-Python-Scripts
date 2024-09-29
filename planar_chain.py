import pymel.core as pm
# Save the objects
a = pm.selected()[0]
b = pm.selected()[0]
c = pm.selected()[0]
# Get the vectors in world space
start = a.getTranslation(space="world")
end = b.getTranslation(space="world")
pole = c.getTranslation(space="world")
# Get the vectors from the start to end and pole points
ab = end-start
ac = pole-start
# Grabe the angle between ab and ac in radians, and convert to degrees
angle = pm.dt.degrees(ab.angle(ac))
# Grab the length of vector ac
len = ac.length()
# Create a child joint
pm.select(a)
new = pm.joint()
# Set new rotation on the start joint
old_rotation = a.getRotation()
old_rotation[1]-= angle
a.setRotation(old_rotation)
# Set new translation on the child joint
old_translation = new.getTranslation()
old_translation[0] = len
new.setTranslation(old_translation)

ba = start - end
bc = pole - end
second_angle = pm.dt.degrees(ba.angle(bc))
second_length = cb.length()

# Create a child joint
pm.select(new)
new_child = pm.joint()

# Reset world space rotation on the pole joint
second_old_rotation = new.getRotation(space="world")
second_old_rotation[1] = 0
new.setRotation(second_old_rotation, space = "world")

# Set new rotation on the pole joint
second_old_rotation = new.getRotation()
second_old_rotation[1] += second_angle
new.setRotation(second_old_rotation)
# Set new translation on the child joint
second_old_translation = new_child.getTranslation()
second_old_translation[0] = second_length
new_child.setTranslation(second_old_translation)
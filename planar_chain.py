import pymel.core as pm

# Save the objects
a = pm.selected()[0]
b = pm.selected()[1]
c = pm.selected()[2]

# Get the vectors in world space
start = a.getTranslation(space="world")
end = b.getTranslation(space="world")
pole = c.getTranslation(space="world")

# Get the vectors from the start to end and pole points
a_to_b = end - start
a_to_c = pole - start

# Grab the angle between ab and ac in radians, and convert to degrees
angle_a = pm.dt.degrees(a_to_b.angle(a_to_c))

# Grab the length of vector ac
len_ac = a_to_c.length()

# Create a new pole joint
pm.select(a)
new_c = pm.joint()

# Set new rotation on the start joint
# TODO: Angle needs to be subtracted for legs, and added for arms
old_rotation = a.getRotation()
old_rotation[1]-= angle_a
a.setRotation(old_rotation)

# Set new translation on the child joint
old_translation = new_c.getTranslation()
old_translation[0] = len_ac
new_c.setTranslation(old_translation)

# Get the angle and length between the pole and end point
b_to_a = start - end
b_to_c = pole - end
c_to_b = end - pole
# second_angle = pm.dt.degrees(b_to_a.angle(b_to_c))
second_length = c_to_b.length()

## Create a dummy pole joint to get the proper angle between the end joint
# TODO: Test this step by step
pm.select(c)
dummy_c = pm.joint()
pos_dummy_c = dummy_c.getTranslation()
pos_dummy_c[0] += 20
dummy_c.setTranslation(pos_dummy_c)
# Get the proper angle between the pole joint and the end joint
c_to_dummy_c = dummy_c.getTranslation(space="world") - pole
angle_c = pm.dt.degrees(c_to_b.angle(c_to_dummy_c))
pm.delete(dummy_c)

# Create a new end joint
pm.select(new_c)
new_b = pm.joint()

# Set new rotation on the pole joint
# TODO: Angle needs to be added for legs, and subtracted for arms
second_old_rotation = new_c.getRotation()
second_old_rotation[1] -= angle_c
new_b.setRotation(second_old_rotation)

# Set new translation on the new end joint
second_old_translation = new_b.getTranslation()
second_old_translation[0] = second_length
new_b.setTranslation(second_old_translation)
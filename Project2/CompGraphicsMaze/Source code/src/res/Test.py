import glm

# Check available attributes
print("Available attributes in glm:", dir(glm))

# Test vec3 creation
try:
    position = glm.vec3(1.0, 2.0, 3.0)
    print("vec3 created successfully:", position)
except AttributeError as e:
    print("Error:", e)

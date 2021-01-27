# foxymaps


# this is the first algorithm.
# it makes a query to the database of parks
# it then filters the query to only contain parks within a bounding box
    # this bounding box is calculated from the straight line distance from user's origin to destination (the length) and the "rambling Tolerance": the user's tolerance for going out of their way (the width). the compass bearing from origin to destination and the width are used as inputs to a simple trigonometric function which allows the bounding box to be constructed along any diagonal.
# it then determines the best route by running a modified Dijkstra "homing algorithm"
    # which uses a modified Dijkstra algorithm to construct a graph and find the closest park to the origin (within a set angle along the axis towards the destination), and repeating the calculation from that park to find the next park and so forth
# it returns route information in the format required for the Mapbox-Directions-API call as well as information for frontend display (largest park, etc.)

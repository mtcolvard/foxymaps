import mapbox
help(mapbox.Directions)

Help on class Directions in module mapbox.services.directions:

class Directions(mapbox.services.base.Service)
 |  Directions(access_token=None, host=None, cache=None)
 |
 |  Access to the Directions v5 API.
 |
 |  Method resolution order:
 |      Directions
 |      mapbox.services.base.Service
 |      builtins.object
 |
 |  Methods defined here:
 |
 |  directions(self, features, profile='mapbox/driving', alternatives=None, geometries=None, overview=None, steps=None, continue_straight=None, waypoint_snapping=None, annotations=None, language=None, **kwargs)
 |      Request directions for waypoints encoded as GeoJSON features.
 |
 |      Parameters
 |      ----------
 |      features : iterable
 |          An collection of GeoJSON features
 |      profile : str
 |          Name of a Mapbox profile such as 'mapbox.driving'
 |      alternatives : bool
 |          Whether to try to return alternative routes, default: False
 |      geometries : string
 |          Type of geometry returned (geojson, polyline, polyline6)
 |      overview : string or False
 |          Type of returned overview geometry: 'full', 'simplified',
 |          or False
 |      steps : bool
 |          Whether to return steps and turn-by-turn instructions,
 |          default: False
 |      continue_straight : bool
 |          Direction of travel when departing intermediate waypoints
 |      radiuses : iterable of numbers or 'unlimited'
 |          Must be same length as features
 |      waypoint_snapping : list
 |          Controls snapping of waypoints
 |
 |          The list is zipped with the features collection and must
 |          have the same length. Elements of the list must be one of:
 |
 |          - A number (interpretted as a snapping radius)
 |          - The string 'unlimited' (unlimited snapping radius)
 |          - A 3-element tuple consisting of (radius, angle, range)
 |          - None (no snapping parameters specified for that waypoint)
 |      annotations : str
 |          Whether or not to return additional metadata along the route
 |
 |          Possible values are: 'duration', 'distance', 'speed', and
 |          'congestion'. Several annotations can be used by joining
:

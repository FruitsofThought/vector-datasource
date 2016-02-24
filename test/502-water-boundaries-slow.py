# these are tiles which have water boundaries, but only water-to-water
# boundaries. since we remove these, then we should have more than one water
# polygon, but zero water boundaries actually in the tile.
no_boundary_tiles = [
    [18, 74987, 100321], # Near Washington DC. USA
    [17, 21224, 50506], # Near Rio Vista, CA, USA
    [19, 136460, 180934], # Mouth of the Pic River, ON, CA
]

# these are tiles which do have a boundary, to check that the first condition
# isn't trivially fulfilled by having no boundaries whatsoever.
boundary_tiles = [
    [18, 74986, 100320], # Near Washington DC. USA
    [17, 21224, 50502], # Near Rio Vista, CA, USA
    [19, 136460, 180933], # Mouth of the Pic River, ON, CA
]

for z, x, y in no_boundary_tiles:
    with features_in_tile_layer(z, x, y, 'water') as features:
        num_polygons = 0
        num_boundaries = 0

        for f in features:
            geom_type = f['geometry']['type']
            boundary = f['properties'].get('boundary', 'no')

            if geom_type in ['Polygon', 'MultiPolygon']:
                num_polygons += 1

            elif boundary == 'yes':
                num_boundaries += 1

        if num_polygons < 2:
            raise Exception, "Expected at least 2 polygons in water boundary " \
                "test tile, but found only %d" % num_polygons

        if num_boundaries > 0:
            raise Exception, "Expected an all-water tile with no land " \
                "boundaries, but found %d boundaries." % num_boundaries

for z, x, y in boundary_tiles:
    assert_has_feature(
        z, x, y, 'water',
        {'boundary': 'yes'})

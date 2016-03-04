CREATE INDEX new_planet_osm_polygon_water_geom_index ON planet_osm_polygon USING gist(way) WHERE mz_calculate_is_water("amenity", "landuse", "leisure", "natural", "waterway") = TRUE;

BEGIN;

DROP INDEX planet_osm_polygon_water_geom_index;
ALTER INDEX new_planet_osm_polygon_water_geom_index RENAME TO planet_osm_polygon_water_geom_index;

COMMIT;

UPDATE planet_osm_polygon SET
  mz_poi_min_zoom = mz_calculate_poi_level("aerialway", "aeroway", "amenity",
    "barrier", "craft", "emergency", "highway", "historic", "leisure", "lock",
    "man_made", "natural", "office", "power", "railway", "shop", "tourism",
    "waterway", "tags", way_area)
  WHERE
    "emergency" = 'phone' OR
    "amenity" IN ('social_facility', 'clinic', 'doctors', 'dentist',
      'kindergarten', 'childcare', 'toilets') OR
    "tags"->'healthcare' = 'midwife' OR
    "tourism" IN ('hotel', 'motel') OR
    "shop" IN ('department_store', 'supermarket', 'doityourself',
               'hardware', 'trade');

SELECT 
  ps.partkey, 
  sum(ps.supplycost*ps.availqty) AS value
FROM 
  "partsupp" ps,
  "supplier" s,
  "nation" n
WHERE 
  ps.suppkey = s.suppkey 
  AND s.nationkey = n.nationkey 
  AND n.name = 'GERMANY'
GROUP BY 
  ps.partkey
HAVING 
  sum(ps.supplycost*ps.availqty) > (
    SELECT 
      sum(ps.supplycost*ps.availqty) * 0.0001000000 / ${scale}
    FROM 
      "partsupp" ps,
      "supplier" s,
      "nation" n
    WHERE 
      ps.suppkey = s.suppkey 
      AND s.nationkey = n.nationkey 
      AND n.name = 'GERMANY'
  )
ORDER BY 
  value DESC, 
  -- additional column to assure results stability for larger scale factors; this is a deviation from TPC-H specification
  ps.partkey ASC
;

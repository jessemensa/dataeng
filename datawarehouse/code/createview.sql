/*TASK: BUSINESS USER, WANTS TO KNOW THE TOP TWO REGION IDs ordered by total stations capacity in that region*/

/* PASTE THIS IN BIGQUERY EDITOR */ 
CREATE VIEW `engexamspreparation`.dm_regional_manager.top_2_region_by_capacity AS 
SELECT region_id, SUM(capacity) as total_capacity
FROM `engexamspreparation`.raw_bikesharing.stations
WHERE region_id != ''
GROUP BY region_id 
ORDER BY total_capacity desc 
LIMIT 2; 


/* RUN THIS ALSO IN BIGQUERY EDITOR NEXT */ 
Select * from `engexamspreparation`.dm_regional_manager.top_2_region_by_capacity

-- Query to clean whitespace issues in the ReviewText column
SELECT 

	 ReviewID, 
	 CustomerID, 
	 ProductID, 
	 ReviewDate, 
	 Rating
	,REPLACE(ReviewText, '  ', ' ') as ReviewText

FROM customer_reviews
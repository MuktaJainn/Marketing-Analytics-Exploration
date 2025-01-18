-- SQL statement to join customers with geography to get customer data with geographic information.

SELECT 
	c.CustomerID, 
	c.CustomerName,
	c.Email,
	c.Gender,
	c.Age,
	g.Country,
	g.City


FROM customers as c
LEFT JOIN 
geography as g 
ON c.GeographyID = g.GeographyID
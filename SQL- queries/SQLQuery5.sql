-- Query to remove the duplicates and to handle the null values.
    
SELECT 
    JourneyID,  
    CustomerID,  
    ProductID,  
    VisitDate, 
    Stage,  
    Action,  
    COALESCE(Duration, avg_duration) AS Duration  
FROM 
    (
        SELECT 
            JourneyID,  
            CustomerID,  
            ProductID,  
            VisitDate,  
            UPPER(Stage) AS Stage, 
            Action,  
            Duration,  
            AVG(Duration) OVER (PARTITION BY VisitDate) AS avg_duration, 

            ROW_NUMBER() OVER (
                PARTITION BY CustomerID, ProductID, VisitDate, UPPER(Stage), Action 
                ORDER BY JourneyID  
            ) AS row_num 

        FROM customer_journey  
    ) AS subquery  


WHERE row_num = 1; 

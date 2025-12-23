use DA_Projects;

ALTER TABLE Cleaned_DataAnalystJobsIndia
ADD JobID INT IDENTITY(1,1) PRIMARY KEY;

select * from [dbo].[Cleaned_DataAnalystJobsIndia]


-- Q1: Top 5 Companies with the Highest Average Job Ratings
SELECT TOP 5
    Company,
    ROUND(AVG(Rating), 2) AS Avg_Rating,
    COUNT(*) AS Total_Listings
FROM Cleaned_DataAnalystJobsIndia
WHERE Rating >= 1
GROUP BY Company
ORDER BY Avg_Rating DESC;


-- Q2: CTE to calculate average and maximum salary by location 
WITH SalarySummary AS (
    SELECT
        Location,
        ROUND(AVG(Base_Salary), 0) AS Avg_Base_Salary,
        ROUND(MAX(Max_Salary), 0) AS Max_Salary
    FROM Cleaned_DataAnalystJobsIndia
    WHERE Base_Salary IS NOT NULL AND Base_Salary > 0
    GROUP BY Location
)
SELECT *
FROM SalarySummary
WHERE Avg_Base_Salary > 400000    -- ?? threshold value (can change)
ORDER BY Avg_Base_Salary DESC;


-- Q3: Stored Procedure to Update Min_Exp and Max_Exp Columns
CREATE OR ALTER PROCEDURE UpdateExperience
AS
BEGIN
    SET NOCOUNT ON;

    --consistent pattern like '3-5 Yrs'
    UPDATE Cleaned_DataAnalystJobsIndia
    SET 
        Min_Exp = TRY_CAST(LEFT(Experience, CHARINDEX('-', Experience) - 1) AS FLOAT),
        Max_Exp = TRY_CAST(
            SUBSTRING(
                Experience,
                CHARINDEX('-', Experience) + 1,
                CHARINDEX('Y', Experience) - CHARINDEX('-', Experience) - 1
            ) AS FLOAT);

END;
GO

exec UpdateExperience

select * from Cleaned_DataAnalystJobsIndia

drop procedure UpdateExperience

-- Q4: Trigger to automatically calculate "JobListedDaysAgo" on insert

CREATE OR ALTER TRIGGER trg_UpdateJobListedDays
ON Cleaned_DataAnalystJobsIndia
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE D
    SET D.joblisted_days_ago = DATEDIFF(DAY, D.PostedIn, GETDATE())
    FROM Cleaned_DataAnalystJobsIndia D
    INNER JOIN inserted i ON D.JobID = i.JobID;
END;
GO


-- Q5: View for Complete Salary Listings Only

CREATE OR ALTER VIEW vw_CompleteSalaryInfo
AS
SELECT 
    JobID,
	job_title,
    Company,
    Location,
    Base_Salary,
    Max_Salary,
    Rating,
    Reviews_Count,
    Min_Exp,
    Max_Exp,
    Experience,
    PostedIn
FROM Cleaned_DataAnalystJobsIndia
WHERE 
    Base_Salary IS NOT NULL AND Base_Salary > 0
    AND Max_Salary IS NOT NULL AND Max_Salary > 0;
GO

-- View the results
SELECT * FROM vw_CompleteSalaryInfo;



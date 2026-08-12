-- ==========================================
-- Research Radar Database Validation Queries
-- ==========================================


-- 1. Check table counts
-- ==========================================

SELECT 'Papers' AS table_name,
       COUNT(*) AS total_records
FROM papers

UNION ALL

SELECT 'Authors',
       COUNT(*)
FROM authors

UNION ALL

SELECT 'Topics',
       COUNT(*)
FROM topics

UNION ALL

SELECT 'Paper Authors',
       COUNT(*)
FROM paper_authors

UNION ALL

SELECT 'Paper Topics',
       COUNT(*)
FROM paper_topics;



-- 2. View sample papers
-- ==========================================

SELECT
    id,
    title,
    publication_year,
    cited_by_count,
    doi
FROM papers
ORDER BY id
LIMIT 10;



-- 3. View sample authors
-- ==========================================

SELECT
    id,
    name,
    openalex_id
FROM authors
ORDER BY id
LIMIT 10;



-- 4. View sample topics
-- ==========================================

SELECT
    id,
    name
FROM topics
ORDER BY id
LIMIT 20;



-- 5. Verify Paper -> Author relationship
-- ==========================================

SELECT
    p.id AS paper_id,
    p.title,
    a.name AS author_name
FROM papers p

JOIN paper_authors pa
ON p.id = pa.paper_id

JOIN authors a
ON a.id = pa.author_id

ORDER BY p.id

LIMIT 20;



-- 6. Verify Paper -> Topic relationship
-- ==========================================

SELECT
    p.id AS paper_id,
    p.title,
    t.name AS topic_name

FROM papers p

JOIN paper_topics pt
ON p.id = pt.paper_id

JOIN topics t
ON t.id = pt.topic_id

ORDER BY p.id

LIMIT 20;



-- 7. Find papers by keyword
-- ==========================================

SELECT
    id,
    title,
    publication_year

FROM papers

WHERE LOWER(title)
LIKE '%artificial intelligence%'

ORDER BY publication_year DESC;



-- 8. Latest research papers
-- ==========================================

SELECT
    title,
    publication_year,
    cited_by_count

FROM papers

ORDER BY publication_year DESC,
         cited_by_count DESC

LIMIT 20;



-- 9. Most cited papers
-- ==========================================

SELECT
    title,
    cited_by_count

FROM papers

ORDER BY cited_by_count DESC

LIMIT 20;



-- 10. Authors with most papers
-- ==========================================

SELECT
    a.name,
    COUNT(pa.paper_id) AS paper_count

FROM authors a

JOIN paper_authors pa
ON a.id = pa.author_id

GROUP BY a.name

ORDER BY paper_count DESC

LIMIT 20;



-- 11. Topics with most papers
-- ==========================================

SELECT
    t.name,
    COUNT(pt.paper_id) AS paper_count

FROM topics t

JOIN paper_topics pt
ON t.id = pt.topic_id

GROUP BY t.name

ORDER BY paper_count DESC

LIMIT 20;



-- 12. Check duplicate papers
-- ==========================================

SELECT
    openalex_id,
    COUNT(*)

FROM papers

GROUP BY openalex_id

HAVING COUNT(*) > 1;



-- 13. Check duplicate authors
-- ==========================================

SELECT
    openalex_id,
    COUNT(*)

FROM authors

GROUP BY openalex_id

HAVING COUNT(*) > 1;



-- 14. Full paper details example
-- ==========================================

SELECT

p.id,
p.title,
p.publication_year,

STRING_AGG(
    DISTINCT a.name,
    ', '
) AS authors,

STRING_AGG(
    DISTINCT t.name,
    ', '
) AS topics


FROM papers p


LEFT JOIN paper_authors pa
ON p.id = pa.paper_id


LEFT JOIN authors a
ON a.id = pa.author_id


LEFT JOIN paper_topics pt
ON p.id = pt.paper_id


LEFT JOIN topics t
ON t.id = pt.topic_id


GROUP BY
p.id,
p.title,
p.publication_year


LIMIT 10;
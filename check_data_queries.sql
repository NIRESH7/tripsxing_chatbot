-- ========================================
-- TripsXing Database - Data Verification Queries
-- ========================================
-- Run these queries in PostgreSQL Query Tool (pgAdmin) to verify your data
-- ========================================

-- 1. COUNT COUNTRIES
SELECT COUNT(*) as total_countries, 
       STRING_AGG(name, ', ') as country_names 
FROM "Country" 
WHERE "deletedFlag" = false;

-- 2. COUNT STATES
SELECT COUNT(*) as total_states,
       STRING_AGG(name, ', ') as state_names
FROM "State" 
WHERE "deletedFlag" = false;

-- 3. COUNT CITIES
SELECT COUNT(*) as total_cities,
       STRING_AGG(name, ', ') as city_names
FROM "City" 
WHERE "deletedFlag" = false;

-- 4. VIEW ALL USERS
SELECT id, email, "userName", "firstName", "lastName", type, "authType"
FROM "User"
WHERE "deletedFlag" = false
ORDER BY id;

-- 5. VIEW ALL STAYS (HOTELS)
SELECT s.id, s.name, s.address, s.rating, s.price, 
       c.name as city, st.name as state, co.name as country
FROM "Stay" s
LEFT JOIN "City" c ON s."cityId" = c.id
LEFT JOIN "State" st ON s."stateId" = st.id
LEFT JOIN "Country" co ON s."countryId" = co.id
WHERE s."deletedFlag" = false
ORDER BY s.id;

-- 6. VIEW STAYS WITH THEIR FACILITIES
SELECT s.name as stay_name,
       STRING_AGG(sf.name, ', ') as facilities
FROM "Stay" s
LEFT JOIN "_SpecialFacilityToStay" sf_stay ON s.id = sf_stay."B"
LEFT JOIN "SpecialFacility" sf ON sf_stay."A" = sf.id
WHERE s."deletedFlag" = false
GROUP BY s.id, s.name
ORDER BY s.id;

-- 7. VIEW SUBSCRIPTION PLANS
SELECT id, name, price, validity, status, description
FROM "Plan"
WHERE "deletedFlag" = false
ORDER BY price;

-- 8. VIEW ACTIVE SUBSCRIPTIONS
SELECT s.id, u."userName", u.email, p.name as plan_name, 
       s.status, s."startDate", s."expirationDate"
FROM "Subscription" s
JOIN "User" u ON s."userId" = u.id
JOIN "Plan" p ON s."planId" = p.id
ORDER BY s.id;

-- 9. VIEW COUPONS
SELECT id, code, name, "percentageDiscount", "isClaimed", "expireDate"
FROM "Coupon"
WHERE "deletedFlag" = false
ORDER BY id;

-- 10. VIEW STAY RATINGS
SELECT sr.id, s.name as stay_name, u."userName", sr.rating
FROM "StayRating" sr
JOIN "Stay" s ON sr."stayId" = s.id
JOIN "User" u ON sr."userId" = u.id
ORDER BY sr.id;

-- 11. VIEW STAY REVIEWS
SELECT srv.id, s.name as stay_name, u."userName", 
       LEFT(srv.review, 50) || '...' as review_preview
FROM "StayReview" srv
JOIN "Stay" s ON srv."stayId" = s.id
JOIN "User" u ON srv."userId" = u.id
ORDER BY srv.id;

-- 12. VIEW WISHLIST ENTRIES
SELECT u."userName", s.name as stay_name, s.address
FROM "WishlistStay" ws
JOIN "User" u ON ws."userId" = u.id
JOIN "Stay" s ON ws."stayId" = s.id
ORDER BY u."userName";

-- 13. VIEW BLOG POSTS
SELECT id, title, category, views, status, "datePosted"
FROM "BlogPost"
WHERE "deletedFlag" = false
ORDER BY "datePosted" DESC;

-- 14. VIEW BLOG POSTS WITH TAGS
SELECT bp.title, STRING_AGG(t.name, ', ') as tags
FROM "BlogPost" bp
LEFT JOIN "_BlogPostToTag" bp_tag ON bp.id = bp_tag."A"
LEFT JOIN "Tag" t ON bp_tag."B" = t.id
WHERE bp."deletedFlag" = false
GROUP BY bp.id, bp.title
ORDER BY bp.id;

-- 15. VIEW BLOG COMMENTS
SELECT c.id, bp.title as post_title, u."userName", 
       LEFT(c.content, 50) || '...' as comment_preview
FROM "Comments" c
JOIN "BlogPost" bp ON c."postId" = bp.id
JOIN "User" u ON c."userId" = u.id
ORDER BY c."datePosted" DESC;

-- 16. VIEW SPECIAL FACILITIES
SELECT id, name, description, status
FROM "SpecialFacility"
WHERE "deletedFlag" = false
ORDER BY id;

-- 17. VIEW REFERENCE TYPES AND OPTIONS
SELECT rt.name as reference_type,
       STRING_AGG(ro.name, ', ') as options
FROM "ReferenceType" rt
LEFT JOIN "ReferenceOption" ro ON rt.id = ro."typeId"
WHERE rt."deletedFlag" = false
GROUP BY rt.id, rt.name;

-- 18. VIEW LANDING PAGE MEDIA
SELECT id, url, type, "sequenceId"
FROM "LandingPageMedia"
ORDER BY "sequenceId";

-- 19. VIEW AUDIT LOGS
SELECT id, action, model, "changedItemId", timestamp, description
FROM "AuditLog"
ORDER BY timestamp DESC
LIMIT 10;

-- 20. SUMMARY STATISTICS
SELECT 
    (SELECT COUNT(*) FROM "Country" WHERE "deletedFlag" = false) as total_countries,
    (SELECT COUNT(*) FROM "State" WHERE "deletedFlag" = false) as total_states,
    (SELECT COUNT(*) FROM "City" WHERE "deletedFlag" = false) as total_cities,
    (SELECT COUNT(*) FROM "User" WHERE "deletedFlag" = false) as total_users,
    (SELECT COUNT(*) FROM "Stay" WHERE "deletedFlag" = false) as total_stays,
    (SELECT COUNT(*) FROM "Plan" WHERE "deletedFlag" = false) as total_plans,
    (SELECT COUNT(*) FROM "Subscription" WHERE status = 'active') as active_subscriptions,
    (SELECT COUNT(*) FROM "BlogPost" WHERE "deletedFlag" = false) as total_blog_posts;


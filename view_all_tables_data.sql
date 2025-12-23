-- ========================================
-- View ALL Tables and Data in tripsxing_chatbot Database
-- ========================================
-- First, let's see all tables in the database
-- ========================================

-- 1. LIST ALL TABLES IN THE DATABASE
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- ========================================
-- 2. VIEW ALL DATA FROM EACH TABLE
-- ========================================

-- View all Countries
SELECT * FROM "Country";

-- View all States
SELECT * FROM "State";

-- View all Cities
SELECT * FROM "City";

-- View all Users
SELECT * FROM "User";

-- View all Stays (Hotels)
SELECT * FROM "Stay";

-- View all Special Facilities
SELECT * FROM "SpecialFacility";

-- View all Plans
SELECT * FROM "Plan";

-- View all Subscriptions
SELECT * FROM "Subscription";

-- View all Coupons
SELECT * FROM "Coupon";

-- View all Stay Ratings
SELECT * FROM "StayRating";

-- View all Stay Reviews
SELECT * FROM "StayReview";

-- View all Wishlist Stays
SELECT * FROM "WishlistStay";

-- View all Tags
SELECT * FROM "Tag";

-- View all Blog Posts
SELECT * FROM "BlogPost";

-- View all Comments
SELECT * FROM "Comments";

-- View all Landing Page Media
SELECT * FROM "LandingPageMedia";

-- View all Reference Types
SELECT * FROM "ReferenceType";

-- View all Reference Options
SELECT * FROM "ReferenceOption";

-- View all Audit Logs
SELECT * FROM "AuditLog";

-- View Junction Tables (Many-to-Many relationships)
SELECT * FROM "_SpecialFacilityToStay";
SELECT * FROM "_CouponToUser";
SELECT * FROM "_BlogPostToTag";

-- ========================================
-- 3. QUICK SUMMARY - COUNT ALL RECORDS IN EACH TABLE
-- ========================================

SELECT 
    'Country' as table_name, COUNT(*) as record_count FROM "Country"
UNION ALL
SELECT 'State', COUNT(*) FROM "State"
UNION ALL
SELECT 'City', COUNT(*) FROM "City"
UNION ALL
SELECT 'User', COUNT(*) FROM "User"
UNION ALL
SELECT 'Stay', COUNT(*) FROM "Stay"
UNION ALL
SELECT 'SpecialFacility', COUNT(*) FROM "SpecialFacility"
UNION ALL
SELECT 'Plan', COUNT(*) FROM "Plan"
UNION ALL
SELECT 'Subscription', COUNT(*) FROM "Subscription"
UNION ALL
SELECT 'Coupon', COUNT(*) FROM "Coupon"
UNION ALL
SELECT 'StayRating', COUNT(*) FROM "StayRating"
UNION ALL
SELECT 'StayReview', COUNT(*) FROM "StayReview"
UNION ALL
SELECT 'WishlistStay', COUNT(*) FROM "WishlistStay"
UNION ALL
SELECT 'Tag', COUNT(*) FROM "Tag"
UNION ALL
SELECT 'BlogPost', COUNT(*) FROM "BlogPost"
UNION ALL
SELECT 'Comments', COUNT(*) FROM "Comments"
UNION ALL
SELECT 'LandingPageMedia', COUNT(*) FROM "LandingPageMedia"
UNION ALL
SELECT 'ReferenceType', COUNT(*) FROM "ReferenceType"
UNION ALL
SELECT 'ReferenceOption', COUNT(*) FROM "ReferenceOption"
UNION ALL
SELECT 'AuditLog', COUNT(*) FROM "AuditLog"
ORDER BY table_name;


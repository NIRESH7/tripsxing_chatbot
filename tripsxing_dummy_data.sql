-- TripsXing Database Dummy Data - SQL INSERT Statements

-- Run this file directly in PostgreSQL to populate your database with sample data

-- Usage: psql -U postgres -d tripsxing_chatbot -f tripsxing_dummy_data.sql

-- Make sure you're connected to the tripsxing_chatbot database before running this script

-- ====================
-- 1. COUNTRIES
-- ====================

INSERT INTO "Country" (id, name, "imageUrl", "deletedFlag") VALUES
(1, 'India', ARRAY['https://images.unsplash.com/photo-1524492412937-b28074a5d7da'], false),
(2, 'United States', ARRAY['https://images.unsplash.com/photo-1485738422979-f5c462d49f74'], false)
ON CONFLICT (id) DO NOTHING;

-- Reset sequence
SELECT setval('"Country_id_seq"', (SELECT MAX(id) FROM "Country"), true);

-- ====================
-- 2. STATES
-- ====================

INSERT INTO "State" (id, name, "imageUrl", "deletedFlag", "countryId") VALUES
(1, 'Tamil Nadu', ARRAY['https://images.unsplash.com/photo-1582510003544-4d00b7f74220'], false, 1),
(2, 'Kerala', ARRAY['https://images.unsplash.com/photo-1602216056096-3b40cc0c9944'], false, 1),
(3, 'California', ARRAY['https://images.unsplash.com/photo-1549416878-fe0f84ab4838'], false, 2)
ON CONFLICT (id) DO NOTHING;

SELECT setval('"State_id_seq"', (SELECT MAX(id) FROM "State"), true);

-- ====================
-- 3. CITIES
-- ====================

INSERT INTO "City" (id, name, "imageUrl", "deletedFlag", "stateId", "countryId") VALUES
(1, 'Chennai', ARRAY['https://images.unsplash.com/photo-1582510003544-4d00b7f74220'], false, 1, 1),
(2, 'Kochi', ARRAY['https://images.unsplash.com/photo-1596422846543-75c6fc197f07'], false, 2, 1),
(3, 'San Francisco', ARRAY['https://images.unsplash.com/photo-1506146332389-18140dc7b2fb'], false, 3, 2)
ON CONFLICT (id) DO NOTHING;

SELECT setval('"City_id_seq"', (SELECT MAX(id) FROM "City"), true);

-- ====================
-- 4. SPECIAL FACILITIES
-- ====================

INSERT INTO "SpecialFacility" (id, name, description, "imageUrl", "deletedFlag", status) VALUES
(1, 'Free WiFi', 'High-speed complimentary WiFi', 'https://cdn-icons-png.flaticon.com/512/93/93158.png', false, 'active'),
(2, 'Swimming Pool', 'Outdoor swimming pool', 'https://cdn-icons-png.flaticon.com/512/2989/2989988.png', false, 'active'),
(3, 'Spa & Wellness', 'Full-service spa and wellness center', 'https://cdn-icons-png.flaticon.com/512/2917/2917995.png', false, 'active'),
(4, 'Free Parking', 'Complimentary parking available', 'https://cdn-icons-png.flaticon.com/512/3097/3097150.png', false, 'active')
ON CONFLICT (id) DO NOTHING;

SELECT setval('"SpecialFacility_id_seq"', (SELECT MAX(id) FROM "SpecialFacility"), true);

-- ====================
-- 5. USERS
-- ====================

INSERT INTO "User" (id, email, password, "uuid", "userName", "firstName", "lastName", dob, address, contact, "profileImage", salt, type, "authType", "deletedFlag") VALUES
(1, 'admin@tripsxing.com', '$2a$10$dummyHashedPassword123456789012', NULL, 'admin_tripsx', 'Admin', 'User', '1990-01-01', '123 Admin Street, Chennai', '+91-9876543210', NULL, 'cuid-salt-1', 'superAdmin', 'local', false),
(2, 'john.doe@example.com', '$2a$10$dummyHashedPassword123456789012', NULL, 'johndoe', 'John', 'Doe', '1985-05-15', '456 Customer Lane, San Francisco', '+1-555-0123', NULL, 'cuid-salt-2', 'customer', 'local', false),
(3, 'priya.sharma@example.com', '$2a$10$dummyHashedPassword123456789012', 'google-oauth-uuid-123', 'priyasharma', 'Priya', 'Sharma', '1992-08-20', '789 Beach Road, Kochi', '+91-9123456789', NULL, 'cuid-salt-3', 'customer', 'google', false),
(4, 'hotel.admin@resort.com', '$2a$10$dummyHashedPassword123456789012', NULL, 'hotel_admin', 'Hotel', 'Manager', NULL, NULL, NULL, NULL, 'cuid-salt-4', 'hotelAdmin', 'local', false)
ON CONFLICT (id) DO NOTHING;

SELECT setval('"User_id_seq"', (SELECT MAX(id) FROM "User"), true);

-- ====================
-- 6. STAYS (HOTELS)
-- ====================

INSERT INTO "Stay" (id, name, address, contact, rating, description, videos, images, "cityId", "stateId", "countryId", "deletedFlag", price) VALUES
(1, 'Luxury Beach Resort', 'Marine Drive, Kochi, Kerala 682031', '+91-484-1234567', 4.8, 'Experience luxury at its finest with stunning ocean views, world-class amenities, and exceptional service.', 
 ARRAY['https://www.example.com/resort-tour.mp4'], 
 ARRAY['https://images.unsplash.com/photo-1566073771259-6a8506099945', 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b', 'https://images.unsplash.com/photo-1571896349842-33c89424de2d'], 
 2, 2, 1, false, 15000),
(2, 'Heritage Temple Inn', 'Mylapore, Chennai, Tamil Nadu 600004', '+91-44-2345678', 4.5, 'Stay in the heart of Chennai''s cultural district, close to ancient temples and vibrant markets.', 
 ARRAY[]::text[], 
 ARRAY['https://images.unsplash.com/photo-1542314831-068cd1dbfeeb', 'https://images.unsplash.com/photo-1611892440504-42a792e24d32'], 
 1, 1, 1, false, 8000),
(3, 'Golden Gate Boutique Hotel', '123 Market Street, San Francisco, CA 94103', '+1-415-555-0199', 4.7, 'Modern boutique hotel in downtown San Francisco with easy access to major attractions.', 
 ARRAY[]::text[], 
 ARRAY['https://images.unsplash.com/photo-1551882547-ff40c63fe5fa', 'https://images.unsplash.com/photo-1564501049412-61c2a3083791'], 
 3, 3, 2, false, 25000)
ON CONFLICT (id) DO NOTHING;

SELECT setval('"Stay_id_seq"', (SELECT MAX(id) FROM "Stay"), true);

-- Link Stays to Special Facilities (Many-to-Many)
INSERT INTO "_SpecialFacilityToStay" ("A", "B") VALUES
(1, 1), -- WiFi for Luxury Beach Resort
(2, 1), -- Pool for Luxury Beach Resort
(3, 1), -- Spa for Luxury Beach Resort
(4, 1), -- Parking for Luxury Beach Resort
(1, 2), -- WiFi for Heritage Temple Inn
(4, 2), -- Parking for Heritage Temple Inn
(1, 3), -- WiFi for Golden Gate Hotel
(2, 3) -- Pool for Golden Gate Hotel
ON CONFLICT DO NOTHING;

-- ====================
-- 7. SUBSCRIPTION PLANS
-- ====================

INSERT INTO "Plan" (id, name, "planDate", description, benefits, renewal, validity, "titleDescription", price, "deletedFlag", status) VALUES
(1, 'Free Explorer Plan', NOW(), 'Perfect for occasional travelers', 'Access to basic features, Limited bookings per month, Email support', 'No renewal required', 'lifeTime', 'Start your journey with us', 0, false, 'active'),
(2, 'Basic Traveler Plan', NOW(), 'For regular travelers', '10% discount on all bookings, Priority email support, Monthly newsletter with exclusive deals', 'Auto-renewal available', 'monthly', 'Great value for frequent travelers', 499, false, 'active'),
(3, 'Premium Voyager Plan', NOW(), 'Ultimate travel experience', '20% discount on all bookings, 24/7 priority support, Free cancellation, Exclusive access to premium stays, Complimentary upgrades when available', 'Auto-renewal with 5% discount', 'yearly', 'The ultimate travel companion', 4999, false, 'active')
ON CONFLICT (id) DO NOTHING;

SELECT setval('"Plan_id_seq"', (SELECT MAX(id) FROM "Plan"), true);

-- ====================
-- 8. SUBSCRIPTIONS
-- ====================

INSERT INTO "Subscription" (id, "userId", "planId", "orderId", "transactionId", status, "startDate", "expirationDate") VALUES
(1, 2, 3, 'ORD-2024-001', 'TXN-ABC123XYZ', 'active', '2024-01-01', '2025-01-01'),
(2, 3, 2, 'ORD-2024-002', 'TXN-DEF456UVW', 'active', '2024-12-01', '2025-01-01')
ON CONFLICT (id) DO NOTHING;

SELECT setval('"Subscription_id_seq"', (SELECT MAX(id) FROM "Subscription"), true);

-- ====================
-- 9. COUPONS
-- ====================

INSERT INTO "Coupon" (id, code, "expireDate", "isClaimed", "percentageDiscount", name, "createdDate", "deletedFlag") VALUES
(1, 'WELCOME2024', '2025-12-31', false, 500, 'Welcome Offer', NOW(), false),
(2, 'SUMMER25', '2025-06-30', false, 1500, 'Summer Special', NOW(), false),
(3, 'PREMIUM50', '2025-12-31', true, 2000, 'Premium Member Exclusive', NOW(), false)
ON CONFLICT (id) DO NOTHING;

SELECT setval('"Coupon_id_seq"', (SELECT MAX(id) FROM "Coupon"), true);

-- Link claimed coupon to user
INSERT INTO "_CouponToUser" ("A", "B") VALUES (3, 2)
ON CONFLICT DO NOTHING;

-- ====================
-- 10. STAY RATINGS & REVIEWS
-- ====================

INSERT INTO "StayRating" (id, rating, "stayId", "userId") VALUES
(1, 5.0, 1, 2),
(2, 4.5, 2, 3)
ON CONFLICT (id) DO NOTHING;

SELECT setval('"StayRating_id_seq"', (SELECT MAX(id) FROM "StayRating"), true);

INSERT INTO "StayReview" (id, review, "stayId", "userId") VALUES
(1, 'Absolutely amazing stay! The staff was incredible and the ocean view from our room was breathtaking. Highly recommend!', 1, 2),
(2, 'Great location near the temples. Room was clean and comfortable. Would definitely stay again.', 2, 3)
ON CONFLICT (id) DO NOTHING;

SELECT setval('"StayReview_id_seq"', (SELECT MAX(id) FROM "StayReview"), true);

-- ====================
-- 11. WISHLISTS
-- ====================

INSERT INTO "WishlistStay" ("userId", "stayId") VALUES
(3, 1), -- Priya wishlisted Luxury Beach Resort
(2, 3) -- John wishlisted Golden Gate Hotel
ON CONFLICT DO NOTHING;

-- ====================
-- 12. BLOG TAGS
-- ====================

INSERT INTO "Tag" (id, name) VALUES
(1, 'Pilgrimage'),
(2, 'Tourism'),
(3, 'Travel Tips')
ON CONFLICT (id) DO NOTHING;

SELECT setval('"Tag_id_seq"', (SELECT MAX(id) FROM "Tag"), true);

-- ====================
-- 13. BLOG POSTS
-- ====================

INSERT INTO "BlogPost" (id, title, description, content, "datePosted", status, category, views, "Media", images, videos, "authorId", "deletedFlag") VALUES
(1, 'Top 10 Temples to Visit in Tamil Nadu', 'Explore the ancient and magnificent temples of Tamil Nadu', 
 'Tamil Nadu is home to some of the most spectacular temples in India. From the towering gopurams of Madurai Meenakshi Temple to the shore temple of Mahabalipuram, each temple tells a unique story...', 
 NOW(), 'published', 'pilgrimage', 1250, 
 ARRAY[]::text[], 
 ARRAY['https://images.unsplash.com/photo-1582510003544-4d00b7f74220', 'https://images.unsplash.com/photo-1609920658906-8223801e5a87'], 
 ARRAY[]::text[], 
 1, false),
(2, 'Kerala Backwaters: A Complete Travel Guide', 'Everything you need to know about exploring Kerala''s famous backwaters', 
 'The Kerala backwaters are a network of lagoons, lakes, and canals that offer a unique and tranquil travel experience. This guide covers the best houseboats, routes, and local experiences...', 
 NOW(), 'published', 'tourism', 2100, 
 ARRAY[]::text[], 
 ARRAY['https://images.unsplash.com/photo-1602216056096-3b40cc0c9944'], 
 ARRAY[]::text[], 
 1, false)
ON CONFLICT (id) DO NOTHING;

SELECT setval('"BlogPost_id_seq"', (SELECT MAX(id) FROM "BlogPost"), true);

-- Link Blog Posts to Tags (Many-to-Many)
INSERT INTO "_BlogPostToTag" ("A", "B") VALUES
(1, 1), -- Blog 1 has Pilgrimage tag
(1, 3), -- Blog 1 has Travel Tips tag
(2, 2), -- Blog 2 has Tourism tag
(2, 3) -- Blog 2 has Travel Tips tag
ON CONFLICT DO NOTHING;

-- ====================
-- 14. BLOG COMMENTS
-- ====================

INSERT INTO "Comments" (id, content, "datePosted", "postId", "userId") VALUES
(1, 'Great article! Planning my trip to Tamil Nadu next month.', NOW(), 1, 2),
(2, 'The backwaters look absolutely stunning. Adding this to my bucket list!', NOW(), 2, 3)
ON CONFLICT (id) DO NOTHING;

SELECT setval('"Comments_id_seq"', (SELECT MAX(id) FROM "Comments"), true);

-- ====================
-- 15. LANDING PAGE MEDIA
-- ====================

INSERT INTO "LandingPageMedia" (id, url, type, "sequenceId") VALUES
(1, 'https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1', 'image', 1),
(2, 'https://images.unsplash.com/photo-1488646953014-85cb44e25828', 'image', 2)
ON CONFLICT (id) DO NOTHING;

SELECT setval('"LandingPageMedia_id_seq"', (SELECT MAX(id) FROM "LandingPageMedia"), true);

-- ====================
-- 16. REFERENCE TYPES & OPTIONS
-- ====================

INSERT INTO "ReferenceType" (id, name, description, "deletedFlag", status) VALUES
(1, 'Travel Preference', 'User travel preferences', false, 'active')
ON CONFLICT (id) DO NOTHING;

SELECT setval('"ReferenceType_id_seq"', (SELECT MAX(id) FROM "ReferenceType"), true);

INSERT INTO "ReferenceOption" (id, name, description, "deletedFlag", status, "typeId") VALUES
(1, 'Adventure', 'Adventure travel and activities', false, 'active', 1),
(2, 'Relaxation', 'Beach and spa relaxation', false, 'active', 1),
(3, 'Cultural', 'Cultural and heritage tourism', false, 'active', 1)
ON CONFLICT (id) DO NOTHING;

SELECT setval('"ReferenceOption_id_seq"', (SELECT MAX(id) FROM "ReferenceOption"), true);

-- ====================
-- 17. AUDIT LOGS
-- ====================

INSERT INTO "AuditLog" (id, action, "userId", model, "changedItemId", timestamp, "oldValue", "newValue", description) VALUES
(1, 'create', 1, 'Stay', 1, NOW(), NULL, '{"name":"Luxury Beach Resort"}', 'Created new stay: Luxury Beach Resort')
ON CONFLICT (id) DO NOTHING;

SELECT setval('"AuditLog_id_seq"', (SELECT MAX(id) FROM "AuditLog"), true);

-- ====================
-- DONE!
-- ====================
-- You now have complete dummy data for your TripXing website including:
-- ✅ 2 Countries, 3 States, 3 Cities
-- ✅ 4 Special Facilities
-- ✅ 4 Users (Admin, 2 Customers, Hotel Admin)
-- ✅ 3 Hotels/Stays with facilities
-- ✅ 3 Subscription Plans
-- ✅ 2 Active Subscriptions
-- ✅ 3 Discount Coupons
-- ✅ 2 Ratings & 2 Reviews
-- ✅ 2 Wishlist entries
-- ✅ 3 Blog Tags
-- ✅ 2 Blog Posts with tags
-- ✅ 2 Comments
-- ✅ 2 Landing Page Media
-- ✅ 1 Reference Type with 3 Options
-- ✅ 1 Audit Log entry


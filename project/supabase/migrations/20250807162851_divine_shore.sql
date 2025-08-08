-- Initialize the database with required extensions and settings

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create indexes for better performance
-- These will be created by Alembic migrations, but included here for reference

-- User table indexes
-- CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
-- CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Post table indexes
-- CREATE INDEX IF NOT EXISTS idx_posts_owner_id ON posts(owner_id);
-- CREATE INDEX IF NOT EXISTS idx_posts_category_id ON posts(category_id);
-- CREATE INDEX IF NOT EXISTS idx_posts_topic_id ON posts(topic_id);
-- CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at);
-- CREATE INDEX IF NOT EXISTS idx_posts_view_count ON posts(view_count);
-- CREATE INDEX IF NOT EXISTS idx_posts_upvote_count ON posts(upvote_count);

-- User interaction indexes
-- CREATE INDEX IF NOT EXISTS idx_user_interactions_user_id ON user_interactions(user_id);
-- CREATE INDEX IF NOT EXISTS idx_user_interactions_post_id ON user_interactions(post_id);
-- CREATE INDEX IF NOT EXISTS idx_user_interactions_timestamp ON user_interactions(timestamp);
-- CREATE INDEX IF NOT EXISTS idx_user_interactions_type ON user_interactions(interaction_type);

-- Composite indexes for common queries
-- CREATE INDEX IF NOT EXISTS idx_user_interactions_user_post ON user_interactions(user_id, post_id);
-- CREATE INDEX IF NOT EXISTS idx_posts_category_available ON posts(category_id, is_available_in_public_feed);
-- CREATE INDEX IF NOT EXISTS idx_posts_topic_available ON posts(topic_id, is_available_in_public_feed);

-- Full-text search indexes
-- CREATE INDEX IF NOT EXISTS idx_posts_title_gin ON posts USING gin(to_tsvector('english', title));
-- CREATE INDEX IF NOT EXISTS idx_posts_tags_gin ON posts USING gin(tags);

-- Set up database configuration for better performance
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
ALTER SYSTEM SET random_page_cost = 1.1;
ALTER SYSTEM SET effective_io_concurrency = 200;

-- Reload configuration
SELECT pg_reload_conf();
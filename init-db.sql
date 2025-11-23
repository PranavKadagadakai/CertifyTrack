-- PostgreSQL initialization script for CertifyTrack
-- This script runs automatically when the container starts
-- Create UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- Create application schema
CREATE SCHEMA IF NOT EXISTS certifytrack;
-- Set default search path
ALTER DATABASE certifytrack
SET search_path TO certifytrack,
    public;
-- Create indexes for common queries
-- (These will be created by Django migrations, but you can add custom ones here)
-- Create application user with limited permissions (optional, for security)
-- REVOKE CONNECT ON DATABASE certifytrack FROM PUBLIC;
-- GRANT CONNECT ON DATABASE certifytrack TO certifytrack_user;
-- GRANT USAGE ON SCHEMA certifytrack TO certifytrack_user;
-- GRANT CREATE ON SCHEMA certifytrack TO certifytrack_user;
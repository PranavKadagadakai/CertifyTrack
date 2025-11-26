# Frontend Dockerfile for CertifyTrack
# Multi-stage build for optimized production image

# Stage 1: Builder
FROM node:18-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package.json pnpm-lock.yaml ./

RUN apk add --no-cache build-base && \
    npm install -g pnpm@^8.15.0 && \
    pnpm install --frozen-lockfile

# Copy source
COPY . .

# Build application
RUN pnpm build

# Stage 2: Runtime
FROM node:18-alpine

WORKDIR /app

# Install serve to run production build
RUN npm install -g serve

# Create non-root user
RUN addgroup -g 1000 appuser && adduser -D -u 1000 -G appuser appuser

# Copy built app from builder
COPY --from=builder --chown=appuser:appuser /app/dist ./dist

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 3000

# Environment variables
ENV NODE_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000 || exit 1

# Start application
CMD ["serve", "-s", "dist", "-l", "3000"]

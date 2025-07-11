from backend.db.mongo_client import chunks_col

def setup_ttl_index():
    # Delete chunks older than 7 days
    chunks_col.create_index("createdAt", expireAfterSeconds=604800)
CREATE TABLE IF NOT EXISTS CORE_DB.resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    department VARCHAR(255) NOT NULL,
    text TEXT NOT NULL,
    embedding VECTOR(768) COMMENT "hnsw(distance=cosine)",
    available BOOLEAN DEFAULT FALSE
);
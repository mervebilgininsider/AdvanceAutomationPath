-- Test results table
CREATE TABLE IF NOT EXISTS test_results (
    id SERIAL PRIMARY KEY,
    test_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    duration DECIMAL(10,3),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    error_message TEXT,
    screenshot_path VARCHAR(500),
    build_number VARCHAR(100),
    git_commit VARCHAR(100),
    branch VARCHAR(100)
);

-- Test metrics table
CREATE TABLE IF NOT EXISTS test_metrics (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metric_type VARCHAR(100),
    total_tests INTEGER,
    passed INTEGER,
    failed INTEGER,
    duration DECIMAL(10,3),
    build_number VARCHAR(100),
    git_commit VARCHAR(100)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_test_results_timestamp ON test_results(timestamp);
CREATE INDEX IF NOT EXISTS idx_test_results_status ON test_results(status);
CREATE INDEX IF NOT EXISTS idx_test_results_test_name ON test_results(test_name);

CREATE INDEX IF NOT EXISTS idx_test_metrics_timestamp ON test_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_test_metrics_type ON test_metrics(metric_type);

-- Insert sample data
INSERT INTO test_results (test_name, status, duration, build_number, git_commit, branch) 
VALUES ('sample_test', 'passed', 45.2, '1', 'sample-commit', 'main');

INSERT INTO test_metrics (metric_type, total_tests, passed, failed, duration, build_number, git_commit)
VALUES ('test_summary', 1, 1, 0, 45.2, '1', 'sample-commit');

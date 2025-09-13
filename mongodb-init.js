db = db.getSiblingDB('test_metrics');

// Test results collection
db.createCollection('test_results');

// Test metrics collection
db.createCollection('test_metrics');

// Create indexes for better performance
db.test_results.createIndex({ "timestamp": 1 });
db.test_results.createIndex({ "test_name": 1 });
db.test_results.createIndex({ "status": 1 });

db.test_metrics.createIndex({ "timestamp": 1 });
db.test_metrics.createIndex({ "metric_type": 1 });

print('MongoDB initialized for test metrics');

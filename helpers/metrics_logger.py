import pymongo
import json
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MetricsLogger:
    def __init__(self):
        self.mongo_client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """MongoDB'ye bağlan"""
        try:
            mongo_url = os.getenv('MONGO_URL', 'mongodb://admin:password123@localhost:27017/test_metrics?authSource=admin')
            self.mongo_client = pymongo.MongoClient(mongo_url)
            self.db = self.mongo_client['test_metrics']
            logger.info("MongoDB'ye başarıyla bağlandı")
        except Exception as e:
            logger.error(f"MongoDB bağlantı hatası: {e}")
    
    def log_test_result(self, test_name, status, duration, error_message=None, screenshot_path=None):
        """Test sonucunu MongoDB'ye kaydet"""
        try:
            test_result = {
                "test_name": test_name,
                "status": status,  # "passed", "failed", "skipped"
                "duration": duration,
                "timestamp": datetime.utcnow(),
                "error_message": error_message,
                "screenshot_path": screenshot_path,
                "build_number": os.getenv('BUILD_NUMBER', 'unknown'),
                "git_commit": os.getenv('GIT_COMMIT', 'unknown'),
                "branch": os.getenv('GIT_BRANCH', 'unknown')
            }
            
            result = self.db.test_results.insert_one(test_result)
            logger.info(f"Test sonucu kaydedildi: {test_name} - {status}")
            return result.inserted_id
            
        except Exception as e:
            logger.error(f"Test sonucu kaydetme hatası: {e}")
            return None
    
    def log_test_metrics(self, metrics_data):
        """Test metriklerini kaydet"""
        try:
            metrics = {
                "timestamp": datetime.utcnow(),
                "metric_type": "test_summary",
                "data": metrics_data,
                "build_number": os.getenv('BUILD_NUMBER', 'unknown'),
                "git_commit": os.getenv('GIT_COMMIT', 'unknown')
            }
            
            result = self.db.test_metrics.insert_one(metrics)
            logger.info("Test metrikleri kaydedildi")
            return result.inserted_id
            
        except Exception as e:
            logger.error(f"Test metrikleri kaydetme hatası: {e}")
            return None
    
    def get_test_summary(self, hours=24):
        """Son X saatteki test özetini al"""
        try:
            from datetime import timedelta
            start_time = datetime.utcnow() - timedelta(hours=hours)
            
            pipeline = [
                {"$match": {"timestamp": {"$gte": start_time}}},
                {"$group": {
                    "_id": "$status",
                    "count": {"$sum": 1},
                    "avg_duration": {"$avg": "$duration"}
                }},
                {"$group": {
                    "_id": None,
                    "total_tests": {"$sum": "$count"},
                    "passed": {"$sum": {"$cond": [{"$eq": ["$_id", "passed"]}, "$count", 0]}},
                    "failed": {"$sum": {"$cond": [{"$eq": ["$_id", "failed"]}, "$count", 0]}},
                    "avg_duration": {"$avg": "$avg_duration"}
                }}
            ]
            
            result = list(self.db.test_results.aggregate(pipeline))
            return result[0] if result else None
            
        except Exception as e:
            logger.error(f"Test özeti alma hatası: {e}")
            return None
    
    def close(self):
        """MongoDB bağlantısını kapat"""
        if self.mongo_client:
            self.mongo_client.close()
            logger.info("MongoDB bağlantısı kapatıldı")

# Global instance
metrics_logger = MetricsLogger()

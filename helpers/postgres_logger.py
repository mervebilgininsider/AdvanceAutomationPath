import psycopg2
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PostgresLogger:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """PostgreSQL'ye bağlan"""
        try:
            self.connection = psycopg2.connect(
                host=os.getenv('POSTGRES_HOST', 'localhost'),
                port=os.getenv('POSTGRES_PORT', '5432'),
                database=os.getenv('POSTGRES_DB', 'test_metrics'),
                user=os.getenv('POSTGRES_USER', 'admin'),
                password=os.getenv('POSTGRES_PASSWORD', 'password123')
            )
            logger.info("PostgreSQL'ye başarıyla bağlandı")
        except Exception as e:
            logger.error(f"PostgreSQL bağlantı hatası: {e}")
    
    def log_test_result(self, test_name, status, duration, error_message=None, screenshot_path=None):
        """Test sonucunu PostgreSQL'ye kaydet"""
        try:
            cursor = self.connection.cursor()
            
            query = """
                INSERT INTO test_results 
                (test_name, status, duration, timestamp, error_message, screenshot_path, build_number, git_commit, branch)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            
            values = (
                test_name,
                status,
                duration,
                datetime.utcnow(),
                error_message,
                screenshot_path,
                os.getenv('BUILD_NUMBER', 'unknown'),
                os.getenv('GIT_COMMIT', 'unknown'),
                os.getenv('GIT_BRANCH', 'unknown')
            )
            
            cursor.execute(query, values)
            result_id = cursor.fetchone()[0]
            self.connection.commit()
            cursor.close()
            
            logger.info(f"Test sonucu kaydedildi: {test_name} - {status} - ID: {result_id}")
            return result_id
            
        except Exception as e:
            logger.error(f"Test sonucu kaydetme hatası: {e}")
            return None
    
    def log_test_metrics(self, metrics_data):
        """Test metriklerini kaydet"""
        try:
            cursor = self.connection.cursor()
            
            query = """
                INSERT INTO test_metrics 
                (timestamp, metric_type, total_tests, passed, failed, duration, build_number, git_commit)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            
            values = (
                datetime.utcnow(),
                'test_summary',
                metrics_data.get('total_tests', 0),
                metrics_data.get('passed', 0),
                metrics_data.get('failed', 0),
                metrics_data.get('duration', 0),
                os.getenv('BUILD_NUMBER', 'unknown'),
                os.getenv('GIT_COMMIT', 'unknown')
            )
            
            cursor.execute(query, values)
            result_id = cursor.fetchone()[0]
            self.connection.commit()
            cursor.close()
            
            logger.info("Test metrikleri kaydedildi")
            return result_id
            
        except Exception as e:
            logger.error(f"Test metrikleri kaydetme hatası: {e}")
            return None
    
    def get_test_summary(self, hours=24):
        """Son X saatteki test özetini al"""
        try:
            cursor = self.connection.cursor()
            
            query = """
                SELECT 
                    COUNT(*) as total_tests,
                    SUM(CASE WHEN status = 'passed' THEN 1 ELSE 0 END) as passed,
                    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                    AVG(duration) as avg_duration
                FROM test_results 
                WHERE timestamp >= NOW() - INTERVAL '%s hours'
            """
            
            cursor.execute(query, (hours,))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return {
                    'total_tests': result[0],
                    'passed': result[1],
                    'failed': result[2],
                    'avg_duration': float(result[3]) if result[3] else 0
                }
            return None
            
        except Exception as e:
            logger.error(f"Test özeti alma hatası: {e}")
            return None
    
    def close(self):
        """PostgreSQL bağlantısını kapat"""
        if self.connection:
            self.connection.close()
            logger.info("PostgreSQL bağlantısı kapatıldı")

postgres_logger = PostgresLogger()

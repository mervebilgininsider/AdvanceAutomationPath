"""PostgreSQL database logging utilities for test metrics and results."""

import os
import logging
from datetime import datetime
import psycopg2

logger = logging.getLogger(__name__)

class PostgresLogger:
    """Logs test results and metrics to PostgreSQL."""
    def __init__(self):
        """Initialize PostgreSQL connection."""
        self.connection = None
        self.connect()

    def connect(self):
        """Connect to PostgreSQL."""
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
            logger.error("PostgreSQL bağlantı hatası: %s", e)

    def log_test_result(
            self,
            test_name,
            status,
            duration,
            error_message=None,
            screenshot_path=None):
        """Log test result to PostgreSQL."""
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

            logger.info(
                "Test sonucu kaydedildi: %s - %s - ID: %s", test_name, status, result_id)
            return result_id

        except Exception as e:
            logger.error("Test sonucu kaydetme hatası: %s", e)
            return None

    def log_test_metrics(self, metrics_data):
        """Log test metrics to PostgreSQL."""
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
            logger.error("Test metrikleri kaydetme hatası: %s", e)
            return None

    def get_test_summary(self, hours=24):
        """Get test summary for the last X hours."""
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
            logger.error("Test özeti alma hatası: %s", e)
            return None

    def close(self):
        """Close PostgreSQL connection."""
        if self.connection:
            self.connection.close()
            logger.info("PostgreSQL bağlantısı kapatıldı")

postgres_logger = PostgresLogger()

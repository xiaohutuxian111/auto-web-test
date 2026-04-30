"""
数据库工具模块

该模块提供了基于SQLAlchemy的数据库操作工具，支持连接池管理和事务处理。
"""

import contextlib
from typing import Any, Dict, List, Optional, Union

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from config.settings import settings


class DBUtil:
    """
    数据库工具类
    
    提供数据库连接、查询、事务管理等功能。
    支持连接池配置和自动事务处理。
    """
    
    def __init__(self, database_url: Optional[str] = None, echo: Optional[bool] = None):
        """
        初始化数据库工具
        
        Args:
            database_url: 数据库连接URL，默认使用settings中的配置
            echo: 是否启用SQL日志，默认使用settings中的配置
        """
        self.database_url = database_url or settings.DATABASE_URL
        self.echo = echo if echo is not None else settings.DB_ECHO
        
        # 创建数据库引擎
        self.engine = create_engine(
            self.database_url,
            echo=self.echo,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_pre_ping=settings.DB_POOL_PRE_PING,  # 连接前检查连接是否有效
            pool_recycle=settings.DB_POOL_RECYCLE    # 连接回收时间（秒）
        )
        
        # 创建会话工厂
        self.SessionLocal = sessionmaker(
            bind=self.engine, 
            class_=Session, 
            autocommit=False, 
            autoflush=False
        )

    @contextlib.contextmanager
    def _session_scope(self):
        """
        提供事务范围的上下文管理器
        
        Yields:
            Session: 数据库会话对象
            
        Raises:
            SQLAlchemyError: 数据库操作异常
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise SQLAlchemyError(f"数据库操作失败: {e}") from e
        finally:
            session.close()

    def get_one(self, sql: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        执行查询，返回单行数据
        
        Args:
            sql: SQL查询语句
            params: 查询参数
            
        Returns:
            Optional[Dict[str, Any]]: 查询结果，如果没有数据则返回None
            
        Raises:
            SQLAlchemyError: 数据库操作异常
        """
        with self._session_scope() as session:
            result = session.execute(text(sql), params or {})
            row = result.mappings().fetchone()
            return dict(row) if row else None

    def get_all(self, sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        执行查询，返回所有行数据
        
        Args:
            sql: SQL查询语句
            params: 查询参数
            
        Returns:
            List[Dict[str, Any]]: 查询结果列表
            
        Raises:
            SQLAlchemyError: 数据库操作异常
        """
        with self._session_scope() as session:
            result = session.execute(text(sql), params or {})
            return [dict(row) for row in result.mappings()]

    def save(self, sql: str, params: Optional[Dict[str, Any]] = None) -> int:
        """
        执行插入操作
        
        Args:
            sql: SQL插入语句
            params: 插入参数
            
        Returns:
            int: 影响的行数
            
        Raises:
            SQLAlchemyError: 数据库操作异常
        """
        return self._execute_dml(sql, params)

    def update(self, sql: str, params: Optional[Dict[str, Any]] = None) -> int:
        """
        执行更新操作
        
        Args:
            sql: SQL更新语句
            params: 更新参数
            
        Returns:
            int: 影响的行数
            
        Raises:
            SQLAlchemyError: 数据库操作异常
        """
        return self._execute_dml(sql, params)

    def delete(self, sql: str, params: Optional[Dict[str, Any]] = None) -> int:
        """
        执行删除操作
        
        Args:
            sql: SQL删除语句
            params: 删除参数
            
        Returns:
            int: 影响的行数
            
        Raises:
            SQLAlchemyError: 数据库操作异常
        """
        return self._execute_dml(sql, params)

    def _execute_dml(self, sql: str, params: Optional[Dict[str, Any]] = None) -> int:
        """
        统一处理DML操作（INSERT、UPDATE、DELETE）
        
        Args:
            sql: SQL语句
            params: 参数
            
        Returns:
            int: 影响的行数
            
        Raises:
            SQLAlchemyError: 数据库操作异常
        """
        with self._session_scope() as session:
            result = session.execute(text(sql), params or {})
            return result.rowcount

    def execute_batch(self, sql_list: List[str], params_list: Optional[List[Dict[str, Any]]] = None) -> List[int]:
        """
        批量执行SQL语句
        
        Args:
            sql_list: SQL语句列表
            params_list: 参数列表，与SQL语句一一对应
            
        Returns:
            List[int]: 每个SQL语句影响的行数列表
            
        Raises:
            SQLAlchemyError: 数据库操作异常
            ValueError: 当SQL语句和参数数量不匹配时
        """
        if params_list and len(sql_list) != len(params_list):
            raise ValueError("SQL语句数量与参数数量不匹配")
        
        results = []
        with self._session_scope() as session:
            for i, sql in enumerate(sql_list):
                params = params_list[i] if params_list else {}
                result = session.execute(text(sql), params)
                results.append(result.rowcount)
        
        return results

    def test_connection(self) -> bool:
        """
        测试数据库连接
        
        Returns:
            bool: 连接是否成功
        """
        try:
            with self._session_scope() as session:
                session.execute(text("SELECT 1"))
            return True
        except Exception:
            return False


# 创建全局数据库工具实例
db_util = DBUtil()


if __name__ == '__main__':
    # 测试数据库连接
    if db_util.test_connection():
        print("数据库连接成功")
        
        # 测试删除操作
        try:
            result = db_util.delete(
                sql="DELETE FROM project.t_project_type_configuration WHERE c_project_type = :c_project_type",
                params={'c_project_type': '自动化创建_888f4f58-ced9-4d10-a95c-6da1c92cc42a'}
            )
            print(f"删除操作影响行数: {result}")
        except Exception as e:
            print(f"删除操作失败: {e}")
    else:
        print("数据库连接失败")

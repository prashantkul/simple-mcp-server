"""
Database management module for customer MCP server.
Handles all database operations for customer management.
"""

import sqlite3
import os
import logging
from datetime import datetime
from typing import Optional, Dict, List, Any

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages SQLite database operations for customer management."""

    def __init__(self, db_path: str = None):
        """
        Initialize database manager.

        Args:
            db_path: Path to SQLite database file. Defaults to ./data/customers.db
        """
        self.db_path = db_path or os.path.join(os.getcwd(), 'data', 'customers.db')
        self._ensure_data_directory()
        self.init_database()

    def _ensure_data_directory(self):
        """Ensure the data directory exists."""
        data_dir = os.path.dirname(self.db_path)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
            logger.info(f"Created data directory: {data_dir}")

    def get_connection(self):
        """Create a database connection with row factory for dict-like access."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
        """Convert a SQLite row to a dictionary."""
        return {key: row[key] for key in row.keys()}

    def init_database(self):
        """Initialize the SQLite database with the customers table and sample data."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Create customers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    status TEXT DEFAULT 'active' CHECK(status IN ('active', 'disabled')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create indexes
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_customer_status ON customers(status)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_customer_email ON customers(email)
            ''')

            # Check if we need to add sample data
            cursor.execute('SELECT COUNT(*) FROM customers')
            count = cursor.fetchone()[0]

            if count == 0:
                # Insert sample data
                sample_customers = [
                    ('Alice Johnson', 'alice.johnson@email.com', '+1-555-0101', 'active'),
                    ('Bob Smith', 'bob.smith@email.com', '+1-555-0102', 'active'),
                    ('Carol White', 'carol.white@email.com', '+1-555-0103', 'active'),
                    ('David Brown', 'david.brown@email.com', '+1-555-0104', 'disabled'),
                    ('Eve Davis', 'eve.davis@email.com', '+1-555-0105', 'active'),
                    ('Frank Miller', 'frank.miller@email.com', '+1-555-0106', 'active'),
                    ('Grace Wilson', 'grace.wilson@email.com', '+1-555-0107', 'active'),
                    ('Henry Moore', 'henry.moore@email.com', '+1-555-0108', 'disabled'),
                    ('Iris Taylor', 'iris.taylor@email.com', '+1-555-0109', 'active'),
                    ('Jack Anderson', 'jack.anderson@email.com', '+1-555-0110', 'active'),
                ]

                cursor.executemany('''
                    INSERT INTO customers (name, email, phone, status)
                    VALUES (?, ?, ?, ?)
                ''', sample_customers)

                conn.commit()
                logger.info(f"Initialized database with {len(sample_customers)} sample customers")

            # Log database stats
            cursor.execute('SELECT COUNT(*) FROM customers')
            total = cursor.fetchone()[0]
            cursor.execute('SELECT COUNT(*) FROM customers WHERE status = "active"')
            active = cursor.fetchone()[0]
            cursor.execute('SELECT COUNT(*) FROM customers WHERE status = "disabled"')
            disabled = cursor.fetchone()[0]

            conn.close()

            logger.info(f"Database initialized: {total} customers ({active} active, {disabled} disabled)")

        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    # ==================== READ OPERATIONS ====================

    def get_customer(self, customer_id: int) -> Dict[str, Any]:
        """
        Retrieve a specific customer by ID.

        Args:
            customer_id: The unique ID of the customer

        Returns:
            Dict containing customer data or error message
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
            row = cursor.fetchone()
            conn.close()

            if row:
                return {
                    'success': True,
                    'customer': self.row_to_dict(row)
                }
            else:
                return {
                    'success': False,
                    'error': f'Customer with ID {customer_id} not found'
                }
        except Exception as e:
            logger.error(f"Error getting customer {customer_id}: {e}")
            return {
                'success': False,
                'error': f'Database error: {str(e)}'
            }

    def list_customers(self, status: Optional[str] = None) -> Dict[str, Any]:
        """
        List all customers, optionally filtered by status.

        Args:
            status: Optional filter - 'active', 'disabled', or None for all

        Returns:
            Dict containing list of customers or error message
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            if status:
                if status not in ['active', 'disabled']:
                    return {
                        'success': False,
                        'error': 'Status must be "active" or "disabled"'
                    }
                cursor.execute('SELECT * FROM customers WHERE status = ? ORDER BY name', (status,))
            else:
                cursor.execute('SELECT * FROM customers ORDER BY name')

            rows = cursor.fetchall()
            conn.close()

            customers = [self.row_to_dict(row) for row in rows]

            return {
                'success': True,
                'count': len(customers),
                'customers': customers
            }
        except Exception as e:
            logger.error(f"Error listing customers: {e}")
            return {
                'success': False,
                'error': f'Database error: {str(e)}'
            }

    # ==================== CREATE OPERATION ====================

    def add_customer(self, name: str, email: Optional[str] = None,
                     phone: Optional[str] = None) -> Dict[str, Any]:
        """
        Add a new customer to the database.

        Args:
            name: Customer's full name (required)
            email: Customer's email address (optional)
            phone: Customer's phone number (optional)

        Returns:
            Dict containing the new customer data or error message
        """
        try:
            if not name or not name.strip():
                return {
                    'success': False,
                    'error': 'Customer name is required'
                }

            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO customers (name, email, phone, status)
                VALUES (?, ?, ?, 'active')
            ''', (name.strip(), email, phone))

            customer_id = cursor.lastrowid
            conn.commit()

            # Fetch the newly created customer
            cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
            row = cursor.fetchone()
            conn.close()

            logger.info(f"Added new customer: {name} (ID: {customer_id})")

            return {
                'success': True,
                'message': f'Customer created with ID {customer_id}',
                'customer': self.row_to_dict(row)
            }
        except Exception as e:
            logger.error(f"Error adding customer: {e}")
            return {
                'success': False,
                'error': f'Database error: {str(e)}'
            }

    # ==================== UPDATE OPERATIONS ====================

    def update_customer(self, customer_id: int, name: Optional[str] = None,
                       email: Optional[str] = None, phone: Optional[str] = None) -> Dict[str, Any]:
        """
        Update customer information.

        Args:
            customer_id: The unique ID of the customer to update
            name: New name (optional)
            email: New email (optional)
            phone: New phone (optional)

        Returns:
            Dict containing updated customer data or error message
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Check if customer exists
            cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
            if not cursor.fetchone():
                conn.close()
                return {
                    'success': False,
                    'error': f'Customer with ID {customer_id} not found'
                }

            # Build update query dynamically
            updates = []
            params = []

            if name is not None:
                updates.append('name = ?')
                params.append(name.strip())
            if email is not None:
                updates.append('email = ?')
                params.append(email)
            if phone is not None:
                updates.append('phone = ?')
                params.append(phone)

            if not updates:
                conn.close()
                return {
                    'success': False,
                    'error': 'No fields to update'
                }

            # Always update the updated_at timestamp
            updates.append('updated_at = CURRENT_TIMESTAMP')
            params.append(customer_id)

            update_clause = ', '.join(updates)
            query = f'UPDATE customers SET {update_clause} WHERE id = ?'
            cursor.execute(query, params)
            conn.commit()

            # Fetch updated customer
            cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
            row = cursor.fetchone()
            conn.close()

            logger.info(f"Updated customer {customer_id}")

            return {
                'success': True,
                'message': f'Customer {customer_id} updated successfully',
                'customer': self.row_to_dict(row)
            }
        except Exception as e:
            logger.error(f"Error updating customer {customer_id}: {e}")
            return {
                'success': False,
                'error': f'Database error: {str(e)}'
            }

    def disable_customer(self, customer_id: int) -> Dict[str, Any]:
        """
        Set customer status to 'disabled'.

        Args:
            customer_id: The unique ID of the customer to disable

        Returns:
            Dict containing updated customer data or error message
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
            if not cursor.fetchone():
                conn.close()
                return {
                    'success': False,
                    'error': f'Customer with ID {customer_id} not found'
                }

            cursor.execute('''
                UPDATE customers
                SET status = 'disabled', updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (customer_id,))
            conn.commit()

            cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
            row = cursor.fetchone()
            conn.close()

            logger.info(f"Disabled customer {customer_id}")

            return {
                'success': True,
                'message': f'Customer {customer_id} has been disabled',
                'customer': self.row_to_dict(row)
            }
        except Exception as e:
            logger.error(f"Error disabling customer {customer_id}: {e}")
            return {
                'success': False,
                'error': f'Database error: {str(e)}'
            }

    def activate_customer(self, customer_id: int) -> Dict[str, Any]:
        """
        Set customer status to 'active'.

        Args:
            customer_id: The unique ID of the customer to activate

        Returns:
            Dict containing updated customer data or error message
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
            if not cursor.fetchone():
                conn.close()
                return {
                    'success': False,
                    'error': f'Customer with ID {customer_id} not found'
                }

            cursor.execute('''
                UPDATE customers
                SET status = 'active', updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (customer_id,))
            conn.commit()

            cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
            row = cursor.fetchone()
            conn.close()

            logger.info(f"Activated customer {customer_id}")

            return {
                'success': True,
                'message': f'Customer {customer_id} has been activated',
                'customer': self.row_to_dict(row)
            }
        except Exception as e:
            logger.error(f"Error activating customer {customer_id}: {e}")
            return {
                'success': False,
                'error': f'Database error: {str(e)}'
            }

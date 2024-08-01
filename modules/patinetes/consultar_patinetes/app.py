import json

from psycopg2.extras import RealDictCursor

from connect_db import get_db_connection


def lambda_handler(_event, _context):
    conn = None
    cur = None
    try:
        # Get database connection
        conn = get_db_connection()

        # Create cursor
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Find current events
        cur.execute("SELECT * FROM patinetes")
        entities = cur.fetchall()

        if not entities:
            return {"statusCode": 204, "body": json.dumps({"message": "No hay patinetes registrados"})}

        return {'statusCode': 200, 'body': json.dumps({'data': entities})}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({"error": str(e)})}
    finally:
        # Close connection and cursor
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()


test_event = None
test_context = None

print(lambda_handler(test_event, test_context))

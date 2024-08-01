import json

from psycopg2.extras import RealDictCursor

from connect_db import get_db_connection


def lambda_handler(event, _context):
    conn = None
    cur = None
    try:
        # Get database connection
        conn = get_db_connection()

        # Create cursor
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Get id
        request_id = event['pathParameters']['id']

        # Start transaction
        conn.autocommit = False

        # Find entity by id
        cur.execute("SELECT * FROM patinetes WHERE id  = %s", (request_id,))
        entity = cur.fetchone()

        if not entity:
            return {"statusCode": 204, "body": json.dumps({"message": "Patinete no encontrado."})}

        # Delete entity by id
        cur.execute("DELETE FROM patinetes WHERE id = %s", (request_id,))

        # Commit query
        conn.commit()
        return {'statusCode': 200, 'body': json.dumps({'message': "Patinete eliminado."})}
    except Exception as e:
        # Handle rollback
        if conn is not None:
            conn.rollback()
        return {'statusCode': 500, 'body': json.dumps({"error": str(e)})}
    finally:
        # Close connection and cursor
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()


# test_event = {
#     "pathParameters": {
#         "id": 2
#     }
# }
# test_context = None
#
# print(lambda_handler(test_event, test_context))

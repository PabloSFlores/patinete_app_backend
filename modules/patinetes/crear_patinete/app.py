import json

from connect_db import get_db_connection

headers = {
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST'
}


def lambda_handler(event, _context):
    conn = None
    cur = None
    try:
        # Get database connection
        conn = get_db_connection()

        # Create cursor
        cur = conn.cursor()

        # Get payload
        payload = json.loads(event['body'])

        marca = payload['marca']
        modelo = payload['modelo']
        tipo = payload['tipo']
        color = payload['color']

        # Start transaction
        conn.autocommit = False

        # Save new entity
        cur.execute("INSERT INTO patinetes(marca, modelo, tipo, color) VALUES (%s, %s, %s, %s)",
                    (marca, modelo, tipo, color))

        # Commit query
        conn.commit()
        return {
            'statusCode': 200,
            'body': json.dumps({'message': "Patinete creado."}),
            'headers': headers,
        }
    except Exception as e:
        # Handle rollback
        if conn is not None:
            conn.rollback()
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)}),
            'headers': headers,
        }
    finally:
        # Close connection and cursor
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()

# test_event = {
#     "body": json.dumps({
#         "marca": "Marca",
#         "modelo": "Modelo",
#         "tipo": "Tipo",
#         "color": "Color"
#     })
# }
# test_context = None
#
# print(lambda_handler(test_event, test_context))

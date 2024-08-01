import json

from connect_db import get_db_connection


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

        entity_id = payload['id']
        marca = payload['marca']
        modelo = payload['modelo']
        tipo = payload['tipo']
        color = payload['color']

        # Start transaction
        conn.autocommit = False

        # Find entity by id
        cur.execute("SELECT * FROM patinetes WHERE id = %s", (entity_id,))
        entity = cur.fetchone()

        if not entity:
            return {"statusCode": 204, "body": json.dumps({"message": "Patinete no encontrado"})}

        # Save new entity
        cur.execute("UPDATE patinetes SET marca = %s, modelo = %s, tipo = %s, color = %s WHERE id = %s",
                    (marca, modelo, tipo, color, entity_id))

        # Commit query
        conn.commit()
        return {'statusCode': 200, 'body': json.dumps({'message': "Patinete atualizado."})}
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
#     "body": json.dumps({
#         "id": 2,
#         "marca": "Marca 2",
#         "modelo": "Modelo 2",
#         "tipo": "Tipo 2",
#         "color": "Color 2"
#     })
# }
# test_context = None
#
# print(lambda_handler(test_event, test_context))

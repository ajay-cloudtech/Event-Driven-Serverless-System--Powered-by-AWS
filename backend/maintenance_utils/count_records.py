import boto3
from boto3.dynamodb.conditions import Key

def count_records(table_name, user_id):
    """
    Counts the number of records in a given DynamoDB table for a specific user.

    Parameters:
        table_name (str): The name of the DynamoDB table to count records in.
        user_id (str): The user ID to filter the records.

    Returns:
        int: The count of records in the specified table for the given user.
    """
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    
    try:
        # Scan the table with a filter to get the count of records for the specific user_id
        response = table.scan(
            FilterExpression="user_id = :user_id",
            ExpressionAttributeValues={":user_id": user_id}
        )
        return response.get("Count", 0)
    except Exception as e:
        print(f"Error counting records in DynamoDB table {table_name} for user {user_id}: {e}")
        return 0
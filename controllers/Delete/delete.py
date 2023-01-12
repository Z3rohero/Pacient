def userDel(id):
    client.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({"message": "user" + id + " ha sido eliminado"})
    return response
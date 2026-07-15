from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = [] #armazenando em memória
task_id_control = 1


@app.route("/tasks", methods = ["POST"]) # Create
def create_task():
    global task_id_control # Permite que consiga mexer com a variável de dentro da funcao
    data = request.get_json()
    new_task = Task(id= task_id_control,title=data.get("title"), description=data.get("description", " "))
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message": "New task created"}) # jsonify formata para JSON, padrão REST


@app.route("/tasks", methods=["GET"]) # Read
def get_task():
    task_list = [task.to_dict() for task in tasks]

    output = {
                "tasks": task_list,
                "total_tasks": len(task_list)
             }
    return jsonify(output)


@app.route("/tasks/<int:id>", methods=["GET"]) # Read
def get_task_by_id(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
        
    return jsonify({"message": "Sorry, we don't found this ID in tasks list"}), 404


@app.route("/tasks/<int:id>", methods=["PUT"]) # Update
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    if task == None:
        return jsonify({"message": "We can't find this task"}), 404
    
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    return jsonify({"message": "Task updated!"})

@app.route("/tasks/<int:id>", methods=["DELETE"]) # Delete
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    if task == None:
        jsonify({"message": "We don't found this task"}), 404

    tasks.remove(task)
    return jsonify({"message": "task removed with sucess"})


if __name__ == "__main__": #Roda o servidor
    app.run(debug=True)
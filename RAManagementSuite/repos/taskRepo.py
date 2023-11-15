from models import db, Task, User, TaskPriority, TaskStatus
from datetime import datetime


def create_task(title, description, deadline, priority, creator_id, assigned_user_ids):
    deadline_time = datetime.strptime(deadline, "%Y-%m-%dT%H:%M")

    new_task = Task(title=title,
                    description=description,
                    deadline=deadline_time,
                    priority=priority,
                    creator_id=creator_id)

    db.session.add(new_task)
    db.session.flush()  # To get the task ID
    for user_id in assigned_user_ids:
        user = User.query.get(user_id)
        if user:
            new_task.assigned_users.append(user)
    db.session.commit()
    return new_task.id


def get_tasks_by_user(user_id, priority=None, status=None):
    query = Task.query.join(Task.assigned_users).filter(User.id == user_id)

    if priority:
        query = query.filter(Task.priority == TaskPriority[priority.upper()])
    if status:
        query = query.filter(Task.status == TaskStatus[status.upper()])

    return query.all()


def get_all_tasks(priority=None, status=None):
    query = Task.query

    if priority:
        query = query.filter(Task.priority == TaskPriority[priority.upper()])
    if status:
        query = query.filter(Task.status == TaskStatus[status.upper()])

    return query.all()


def get_task_by_id(task_id):
    return Task.query.get(task_id)


def update_task(task_id, title, description, deadline, priority, status, assigned_user_ids):
    task = get_task_by_id(task_id)
    if task:
        task.title = title
        task.description = description
        task.deadline = datetime.strptime(deadline, "%Y-%m-%dT%H:%M")  # Adjust the format if needed
        task.priority = priority
        task.status = status

        # Clear existing relationships
        task.assigned_users.clear()

        # Assign new users
        for user_id in assigned_user_ids:
            user = User.query.get(user_id)
            if user:
                task.assigned_users.append(user)
        db.session.commit()
    else:
        raise ValueError("Task not found")


def delete_task(task_id):
    task = get_task_by_id(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    else:
        raise ValueError("Task not found")


def update_task_status(task_id, new_status):
    task = get_task_by_id(task_id)
    if task:
        task.status = new_status
        db.session.commit()
    else:
        raise ValueError("Task not found")

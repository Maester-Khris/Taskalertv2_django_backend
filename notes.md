# to go deeper
- how to define @extends schema attributes to populate documentation

# api reference
## definition of tasks endpoints
### schema 
    item:{
        name: str
    }
    user:{
        name: str,
        created_at: date_time, default (now)
    }
    task:{
        title: str,
        group: str,
        description: text,
        items: [item], default ([])
        editors: [user],
        created_at: date_time, default (now)
        last_modification_time: datetime, default (null)
    }
    filtering_pagination_result: {
        "totalTasks": 20,
        "currentPage": 2,
        "totalPages": 4,
        "tasks": [
            {
                "id": "1",
                "title": "Team Meeting",
                "description": "Discuss project updates",
            },
        ]
    }

### endpoints
- /api/task/ [post]
- /api/tasks/ [get]
- /api/tasks/{id} [get, put]
- /api/tasks/{id}/editors [get]
- /api/tasks/{id}/editor/{userid} [put]
- /api/tasks/group?name [get]
- /api/tasks?title=xxx&description=xxx&item=xxx&page=xxx&limit=xxx

- /api/user/ [post]
- /api/users/ [get]
- /api/users/{id} [get, put]
- /api/users/{id}/tasks [get]
- /api/users/{id}/task/{taskid} [put]

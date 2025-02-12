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
    task:{//
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
- /api/tasks/search?query=xxx

- /api/user/ [post]
- /api/users/ [get]
- /api/users/{id} [get, put]
- /api/users/{id}/tasks [get]
- /api/users/{id}/task/{taskid} [put] (not necessary just use update task endpoint)

- requirement to install
django, djangorest, drf_spectacular, drf_spectacular sidecar, mongoengine, pymongo

67a6868e09983788efa6a53c
{
  "title": "continue !",
  "group": "strong",
  "description": "keep improving and working",
  "items": [
    "finish with mongo api",
    "engage with view crud backed by api",
    "start rabbitmq websocket connection"
  ],
  "editors": [
    {
      "name": "niki"
    },
    {
      "name": "renzel"
    }
  ]
}
"last_modification_time": "2025-02-07T22:06:08.567Z"

[
  {
    $search: {
      index: "tasks-ft-search",
      text: {
        query: "<query>",
        path: {
          wildcard: "*"
        }
      }
    }
  }
]


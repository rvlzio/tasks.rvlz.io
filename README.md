# tasks.rvlz.io

## REST Endpoints
* POST /tasks
* GET /tasks/{id}
* GET /tasks
* DELETE /tasks/{id}
* PATCH /tasks/{id}
* POST /users
* GET /users/{id}
* POST /sessions
* DELETE /sessions

### User Resource

 **POST /users**  

 Register user

 ```sh
 curl -X POST https://api.tasks.rvlz.io/v1/users \
 -H 'Content-Type: application/json' \
 -d '{"username": "user", "password": "mypassword", "email": "user@gmail.com"}'
 ```

Location response header has relative path to new user.

```sh
# Location: /v1/users/Uh2Jj
```

**GET /users/{id}**  

Get user information

```sh
curl https://api.tasks.rvlz.io/v1/users/Uh2Jj
```

```json
// Response Body
{
    "username": "user",
    "email": "user@gmail.com",
    "approved": false
}
```

### Sessions Resource

**POST /sessions**  

Log in using basic authentication.

```sh
curl -X POST https://api.tasks.rvlz.io/v1/sessions \
-H 'Content-Type: application/json' \
--user user:mypassword
```

API responds with a token.

```json
// Response body
{
    "token": "hyj3jiOJ.4JkRRr2"
}
```

To access protected endpoint, use the bearer token scheme.

```sh
# Authorization: Bearer hyj3jiOJ.4JkRRr2
```

**DELETE /sessions**  

Log out using bearer token scheme.

```sh
curl -X DELETE https://api.tasks.rvlz.io/v1/sessions \
-H 'Authorization: Bearer hyj3jiOJ.4JkRRr2'
```

### Task Resource

**POST /tasks**  

Create a tasks.

```sh
curl -X POST https://api.tasks.rvlz.io/v1/tasks \
-H 'Content-Type: application/json' \
-d '{"subject": "Phone bill", "description": "Pay 101.33 by 11/1"}'
```

Location response header has relative path to new task.

```sh
# Location: /v1/tasks/hyeU3H
```

**GET /tasks/{id}**  

Read task.

```sh
curl https://api.tasks.rvlz.io/v1/tasks/hyeU3H
```

```json
// Response body
{
    "id": "hyeU3H",
    "subject": "Phone bill",
    "description": "Pay 101.33 by 11/1",
    "completed": false
}
```

**PATCH /tasks/{id}**  

Update task.

```sh
curl -X PATCH https://api.tasks.rvlz.io/v1/tasks/hyeU3H \
-H 'Content-Type: application/json' \
-d '{"completed": true}'
```

Location response header has relative path to new task.

```sh
# Location: /v1/tasks/hyeU3H
```

**DELETE /tasks/{id}**  

Delete task.

```sh
curl -X DELETE https://api.tasks.rvlz.io/v1/tasks/hyeU3H
```

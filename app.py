[2026-03-04 16:39:04,264] ERROR in app: Exception on /register [POST]
Traceback (most recent call last):
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
    ~~~~~~~~~~~~~~~~~~~~~~~^
        cursor, str_statement, effective_parameters, context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
sqlite3.OperationalError: no such table: user
The above exception was the direct cause of the following exception:
Traceback (most recent call last):
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask/app.py", line 1511, in wsgi_app
    response = self.full_dispatch_request()
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask/app.py", line 919, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask/app.py", line 917, in full_dispatch_request
    rv = self.dispatch_request()
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask/app.py", line 902, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/opt/render/project/src/app.py", line 71, in register
    if User.query.filter_by(username=username).first():
       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/query.py", line 2759, in first
    return self.limit(1)._iter().first()  # type: ignore
           ~~~~~~~~~~~~~~~~~~~^^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/query.py", line 2857, in _iter
    result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
                                                  ~~~~~~~~~~~~~~~~~~~~^
        statement,
        ^^^^^^^^^^
        params,
        ^^^^^^^
        execution_options={"_sa_orm_load_options": self.load_options},
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
    return self._execute_internal(
           ~~~~~~~~~~~~~~~~~~~~~~^
        statement,
        ^^^^^^^^^^
    ...<4 lines>...
        _add_event=_add_event,
        ^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py", line 2249, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        self,
        ^^^^^
    ...<4 lines>...
        conn,
        ^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/context.py", line 306, in orm_execute_statement
    result = conn.execute(
        statement, params or {}, execution_options=execution_options
    )
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1419, in execute
    return meth(
        self,
        distilled_parameters,
        execution_options or NO_OPTIONS,
    )
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/sql/elements.py", line 527, in _execute_on_connection
    return connection._execute_clauseelement(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        self, distilled_params, execution_options
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1641, in _execute_clauseelement
    ret = self._execute_context(
        dialect,
    ...<8 lines>...
        cache_hit=cache_hit,
    )
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1846, in _execute_context
    return self._exec_single_context(
           ~~~~~~~~~~~~~~~~~~~~~~~~~^
        dialect, context, statement, parameters
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1986, in _exec_single_context
    self._handle_dbapi_exception(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        e, str_statement, effective_parameters, cursor, context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 2363, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
    ~~~~~~~~~~~~~~~~~~~~~~~^
        cursor, str_statement, effective_parameters, context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: user
[SQL: SELECT user.id AS user_id, user.username AS user_username, user.password AS user_password, user.email AS user_email, user.profile_image AS user_profile_image 
FROM user 
WHERE user.username = ?
 LIMIT ? OFFSET ?]
[parameters: ('sajeed191', 1, 0)]
(Background on this error at: https://sqlalche.me/e/20/e3q8)
127.0.0.1 - - [04/Mar/2026:16:39:04 +0000] "POST /register HTTP/1.1" 500 265 "https://password-strength-analyzer-00wx.onrender.com/register" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
127.0.0.1 - - [04/Mar/2026:16:39:10 +0000] "GET / HTTP/1.1" 302 199 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
127.0.0.1 - - [04/Mar/2026:16:39:11 +0000] "GET /login HTTP/1.1" 200 1386 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
127.0.0.1 - - [04/Mar/2026:16:39:15 +0000] "GET /register HTTP/1.1" 200 1467 "https://password-strength-analyzer-00wx.onrender.com/login" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
[2026-03-04 16:39:47,358] ERROR in app: Exception on /register [POST]
Traceback (most recent call last):
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
    ~~~~~~~~~~~~~~~~~~~~~~~^
        cursor, str_statement, effective_parameters, context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
sqlite3.OperationalError: no such table: user
The above exception was the direct cause of the following exception:
Traceback (most recent call last):
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask/app.py", line 1511, in wsgi_app
    response = self.full_dispatch_request()
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask/app.py", line 919, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask/app.py", line 917, in full_dispatch_request
    rv = self.dispatch_request()
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask/app.py", line 902, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/opt/render/project/src/app.py", line 71, in register
    if User.query.filter_by(username=username).first():
       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/query.py", line 2759, in first
    return self.limit(1)._iter().first()  # type: ignore
           ~~~~~~~~~~~~~~~~~~~^^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/query.py", line 2857, in _iter
    result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
                                                  ~~~~~~~~~~~~~~~~~~~~^
        statement,
        ^^^^^^^^^^
        params,
        ^^^^^^^
        execution_options={"_sa_orm_load_options": self.load_options},
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
    return self._execute_internal(
           ~~~~~~~~~~~~~~~~~~~~~~^
        statement,
        ^^^^^^^^^^
    ...<4 lines>...
        _add_event=_add_event,
        ^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py", line 2249, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        self,
        ^^^^^
    ...<4 lines>...
        conn,
        ^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/context.py", line 306, in orm_execute_statement
    result = conn.execute(
        statement, params or {}, execution_options=execution_options
    )
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1419, in execute
    return meth(
        self,
        distilled_parameters,
        execution_options or NO_OPTIONS,
    )
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/sql/elements.py", line 527, in _execute_on_connection
    return connection._execute_clauseelement(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        self, distilled_params, execution_options
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1641, in _execute_clauseelement
    ret = self._execute_context(
        dialect,
    ...<8 lines>...
        cache_hit=cache_hit,
    )
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1846, in _execute_context
    return self._exec_single_context(
           ~~~~~~~~~~~~~~~~~~~~~~~~~^
        dialect, context, statement, parameters
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1986, in _exec_single_context
    self._handle_dbapi_exception(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        e, str_statement, effective_parameters, cursor, context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 2363, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
    ~~~~~~~~~~~~~~~~~~~~~~~^
        cursor, str_statement, effective_parameters, context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: user
[SQL: SELECT user.id AS user_id, user.username AS user_username, user.password AS user_password, user.email AS user_email, user.profile_image AS user_profile_image 
FROM user 
WHERE user.username = ?
 LIMIT ? OFFSET ?]
[parameters: ('account', 1, 0)]
(Background on this error at: https://sqlalche.me/e/20/e3q8)
127.0.0.1 - - [04/Mar/2026:16:39:47 +0000] "POST /register HTTP/1.1" 500 265 "https://password-strength-analyzer-00wx.onrender.com/register" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
[2026-03-04 16:39:51 +0000] [56] [INFO] Handling signal: term
[2026-03-04 16:39:51 +0000] [58] [INFO] Worker exiting (pid: 58)
[2026-03-04 16:39:53 +0000] [56] [INFO] Shutting down: Master
[2026-03-04 16:39:58,666] ERROR in app: Exception on /register [POST]
Traceback (most recent call last):
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
    ~~~~~~~~~~~~~~~~~~~~~~~^
        cursor, str_statement, effective_parameters, context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
sqlite3.OperationalError: no such table: user
The above exception was the direct cause of the following exception:
Traceback (most recent call last):
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask/app.py", line 1511, in wsgi_app
    response = self.full_dispatch_request()
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask/app.py", line 919, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask/app.py", line 917, in full_dispatch_request
    rv = self.dispatch_request()
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask/app.py", line 902, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/opt/render/project/src/app.py", line 71, in register
    if User.query.filter_by(username=username).first():
       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/query.py", line 2759, in first
    return self.limit(1)._iter().first()  # type: ignore
           ~~~~~~~~~~~~~~~~~~~^^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/query.py", line 2857, in _iter
    result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
                                                  ~~~~~~~~~~~~~~~~~~~~^
        statement,
        ^^^^^^^^^^
        params,
        ^^^^^^^
        execution_options={"_sa_orm_load_options": self.load_options},
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
    return self._execute_internal(
           ~~~~~~~~~~~~~~~~~~~~~~^
        statement,
        ^^^^^^^^^^
    ...<4 lines>...
        _add_event=_add_event,
        ^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py", line 2249, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        self,
        ^^^^^
    ...<4 lines>...
        conn,
        ^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/context.py", line 306, in orm_execute_statement
    result = conn.execute(
        statement, params or {}, execution_options=execution_options
    )
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1419, in execute
    return meth(
        self,
        distilled_parameters,
        execution_options or NO_OPTIONS,
    )
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/sql/elements.py", line 527, in _execute_on_connection
    return connection._execute_clauseelement(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        self, distilled_params, execution_options
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1641, in _execute_clauseelement
    ret = self._execute_context(
        dialect,
    ...<8 lines>...
        cache_hit=cache_hit,
    )
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1846, in _execute_context
    return self._exec_single_context(
           ~~~~~~~~~~~~~~~~~~~~~~~~~^
        dialect, context, statement, parameters
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1986, in _exec_single_context
    self._handle_dbapi_exception(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        e, str_statement, effective_parameters, cursor, context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 2363, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
    ~~~~~~~~~~~~~~~~~~~~~~~^
        cursor, str_statement, effective_parameters, context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: user
[SQL: SELECT user.id AS user_id, user.username AS user_username, user.password AS user_password, user.email AS user_email, user.profile_image AS user_profile_image 
FROM user 
WHERE user.username = ?
 LIMIT ? OFFSET ?]
[parameters: ('account', 1, 0)]
(Background on this error at: https://sqlalche.me/e/20/e3q8)
127.0.0.1 - - [04/Mar/2026:16:39:58 +0000] "POST /register HTTP/1.1" 500 265 "https://password-strength-analyzer-00wx.onrender.com/register" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"

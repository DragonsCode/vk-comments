from models.database import MyDatabase, SQLITE, USERS, POSTS, VIEW

dbms = MyDatabase(SQLITE)

class User:
    def __init__(self, id, user_id, balance, tasks, skips):
        self.id = id
        self.user_id = user_id
        self.balance = balance
        self.tasks = tasks
        self.skips = skips
    
    def __str__(self):
        return f'👤Ваш профиль:\n\n💳Баллы: {self.balance}'

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"balance={self.balance}, "
            f")>"
        )

class Posts:
    def __init__(self, id, user_id, link, count, all):
        self.id = id
        self.user_id = user_id
        self.link = link
        self.count = count
        self.all = all
    
    def __str__(self):
        return self.link

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"link={self.link}, "
            f"count={self.count}, "
            f")>"
        )

class View:
    def __init__(self, id, user_id, post_id, status, brief):
        self.id = id
        self.user_id = user_id
        self.post_id = post_id
    
    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"post_id={self.post_id}, "
            f")>"
        )

# Program entry point
class methods:
    def get_user_by_id(user_id=None, id=None):
        if user_id is None and id is None:
            users = []
            res = dbms.get_all(db=USERS)
            for i in res:
                users.append(User(i[0], i[1], i[2], i[3], i[4]))
            return users
        elif user_id is not None:
            res = dbms.get_by(db=USERS, vals=f'user_id={user_id}')[0] # simple query
            return User(res[0], res[1], res[2], res[3], res[4])
        elif id is not None:
            res = dbms.get_by(db=USERS, vals=f'id={id}')[0] # simple query
            return User(res[0], res[1], res[2], res[3], res[4])
    
    def insert_user(user_id):
        prev = dbms.get_by(db=USERS, vals=f'user_id={user_id}')
        if prev:
            return 1
        dbms.insert(db=USERS, vals=f"{user_id}, 50, 0, 3", columns="user_id, balance, tasks, skips") # insert data
        return 0
    
    def change_balance(user_id, balance):
        res = dbms.get_by(db=USERS, vals=f'user_id={user_id}')[0]
        prev = User(res[0], res[1], res[2], res[3], res[4])
        dbms.update(db=USERS, set=f"balance='{prev.balance + balance}'", vals=f"user_id={user_id}") # update data
    
    def change_tasks(user_id, tasks):
        res = dbms.get_by(db=USERS, vals=f'user_id={user_id}')[0]
        prev = User(res[0], res[1], res[2], res[3], res[4])
        dbms.update(db=USERS, set=f"tasks='{prev.tasks + tasks}'", vals=f"user_id={user_id}")
    
    def change_skips(user_id, skips):
        res = dbms.get_by(db=USERS, vals=f'user_id={user_id}')[0]
        prev = User(res[0], res[1], res[2], res[3], res[4])
        dbms.update(db=USERS, set=f"skips='{prev.skips + skips}'", vals=f"user_id={user_id}")
    
    def delete_user(user_id):
        dbms.delete(db=USERS, vals=f'user_id={user_id}') # delete data
    

    
    def get_post_by_id(user_id=None, id=None):
        if user_id is None and id is None:
            posts = []
            res = dbms.get_all(db=POSTS)
            for i in res:
                posts.append(Posts(i[0], i[1], i[2], i[3], i[4]))
            return posts
        elif user_id is not None:
            posts = []
            res = dbms.get_by(db=POSTS, vals=f'user_id={user_id}') # simple query
            for i in res:
                posts.append(Posts(i[0], i[1], i[2], i[3], i[4]))
            return posts
        elif id is not None:
            res = dbms.get_by(db=POSTS, vals=f'id={id}')[0] # simple query
            return Posts(res[0], res[1], res[2], res[3], res[4])
    
    def get_dating_posts(user_id=None):
        posts = []
        res = dbms.get_all(db=POSTS)
        for i in res:
            posts.append(Posts(i[0], i[1], i[2], i[3], i[4]))
        views = []
        res1 = dbms.get_by(db=VIEW, vals=f'user_id={user_id}')
        for i in res1:
            views.append(i[2])
        datings = []
        for i in posts:
            if i.id not in views:
                datings.append(i)
        return datings

    
    def insert_post(user_id, link, count):
        comms = count
        dbms.insert(db=POSTS, vals=f"{user_id}, '{link}', {count}, {comms}", columns="user_id, link, count, comms") # insert data
    
    def change_count(id, count):
        res = dbms.get_by(db=POSTS, vals=f'id={id}')[0]
        prev = Posts(res[0], res[1], res[2], res[3], res[4])
        dbms.update(db=POSTS, set=f"count='{prev.count + count}'", vals=f"id={id}") # update data
    
    def delete_post(id):
        dbms.delete(db=POSTS, vals=f'id={id}') # delete data
    


    def get_view_by_id(user_id=None, post_id=None):
        if user_id is None and post_id is None:
            views = []
            res = dbms.get_all(db=VIEW)
            for i in res:
                views.append(View(i[0], i[1], i[2]))
            return views
        elif user_id is not None:
            views = []
            res = dbms.get_by(db=VIEW, vals=f'user_id={user_id}') # simple query
            for i in res:
                views.append(View(i[0], i[1], i[2]))
            return views
        elif post_id is not None:
            views = []
            res = dbms.get_by(db=VIEW, vals=f'post_id={post_id}') # simple query
            for i in res:
                views.append(View(i[0], i[1], i[2]))
            return views
    
    def insert_view(user_id, post_id):
        dbms.insert(db=VIEW, vals=f"{user_id}, {post_id}", columns="user_id, post_id") # insert data
    
    def delete_view(post_id):
        dbms.delete(db=VIEW, vals=f'post_id={post_id}') # delete data
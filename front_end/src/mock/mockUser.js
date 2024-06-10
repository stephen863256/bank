import Mock from 'mockjs';

let userlist = [
    {
        username: "admin",
        password: "admin123"
    },
    {
        username: "guest",
        password: "guest123"
    },
    {
        username: "john",
        password: "john123"
    },
    {
        username: "jane",
        password: "jane123"
    }
];

Mock.mock('http://localhost:8081/login', 'post', (params) => {
    console.log('Mock: Intercepted /login request', params);

    let bodyData = JSON.parse(params.body);

    let result = userlist.filter(item => item.username === bodyData.username && item.password === bodyData.password)[0];

    if (result) {
        return {
            code: 200, // 修改为200
            message: "登录成功",
            data: result // 你可能想返回用户数据
        };
    } else {
        return {
            code: 1,
            message: "用户名或密码错误"
        };
    }
});

Mock.mock(/http:\/\/localhost:8081\/user\/get.*/, 'post', (params) => {
  let searchForm = JSON.parse(params.body);
  const url = new URL(params.url);
  const page = url.searchParams.get('page');
  const size = url.searchParams.get('size');

  console.log('Mock: Intercepted /user/get request', searchForm);
  console.log('Mock: Intercepted /user/get request', page, size);

 
  const matchesSearchForm = (user, searchForm) => {
    if (searchForm.username && user.username !== searchForm.username) {
      return false;
    }
  
    if (searchForm.password && user.password !== searchForm.password) {
      return false;
    }
  
    return true;
  };

  const getAllUsers = (page, size) => {
    const start = (page - 1) * size;
    const end = start + size;
    return userlist.slice(start, end);
  };

  const getFilteredUsers = (searchForm, page, size) => {
    const filteredUsers = userlist.filter(user => {
      // 根据你的需求来实现这个函数
      return matchesSearchForm(user, searchForm);
    });
    const start = (page - 1) * size;
    const end = start + size;
    return filteredUsers.slice(start, end);
  };

  let users;
  if(searchForm == null) {
    // 如果 searchForm 为空，返回所有用户的指定页
    users = getAllUsers(page, size);
  } else {
    // 如果 searchForm 不为空，根据 searchForm 过滤用户并返回指定页
    users = getFilteredUsers(searchForm, page, size);
  }

  console.log('Mock: Intercepted /user/get request', users);
  return {
    code: 200,
    data: {data:users, count:userlist.length}
  };
});

Mock.mock(/http:\/\/localhost:8081\/user\/edit.*/, 'put', (params) => {
  const username = JSON.parse(params.body).username;
  const password = JSON.parse(params.body).password;

  console.log('Mock: Intercepted /user/edit request', username, password);

  const user = userlist.find(user => user.username === username);

  if (user) {
    user.password = password;
    return {
      code: 200,
      message: "修改成功"
    };
  } else {
    return {
      code: 1,
      message: "用户不存在"
    };
  } 
});

Mock.mock(/http:\/\/localhost:8081\/user\/delete.*/, 'delete', (params) => {
  console.log('Mock: Intercepted /user/delete request', params);
  const username = JSON.parse(params.body).username;

  console.log('Mock: Intercepted /user/delete request', username);

  const index = userlist.findIndex(user => user.username === username);

  if (index !== -1) {
    userlist.splice(index, 1);
    return {
      code: 200,
      message: "删除成功"
    };
  } else {
    return {
      code: 1,
      message: "用户不存在" 
    };
  }
});
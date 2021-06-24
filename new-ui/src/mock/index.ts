import Mock from 'mockjs'
import api from '../api'

Mock.mock(api.getUrlByMsg("get-webshell-connections"),  {
    code: 0,
    msg:"",
    data:[
        {
            createDatetime:Date.now(),
            webshellType:"PHP",
            url:"http://sdfsdf.com/1.php",
            ip:"127.0.0.1",
            note:"test123",
            id:"123",
            sessionCount:1231
        },
        {
            createDatetime:Date.now()+300,
            webshellType:"ASP_NET_CS",
            url:"http://sdfsdf.com/1.aspx",
            ip:"127.0.0.1",
            note:"nbnbnb",
            id:"321",
            sessionCount:10
        },
        {
            createDatetime:Date.now()+300,
            webshellType:"ASP_NET_CS",
            url:"http://sdfsdf.com/1.aspx",
            ip:"127.0.0.1",
            note:"nbnbnb",
            id:"321123",
            sessionCount:0
        }
    ]
})

Mock.mock(api.getUrlByMsg("get-code-executor-list"),  {
    code: 0,
    msg:"",
    data:[
        {
            id:"123",
            type:"PHP",
            name:"test123",
            uiPathOfConfig: "/"
        },
        {
            id:"1213",
            type:"ASP_NET_CS",
            name:"test123",
            uiPathOfConfig: "/"
        },
        {
            id:"sdf",
            type:"JSP",
            name:"test123",
            uiPathOfConfig: "/"
        },
        {
            id:"sdfsdf",
            type:"JSP",
            name:"okok",
            uiPathOfConfig: "/testpage"
        },
    ]
})
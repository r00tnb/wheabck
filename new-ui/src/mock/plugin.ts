import Mock from 'mockjs'
import api from '../api'

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
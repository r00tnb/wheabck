import Mock from 'mockjs'
import api from '../api'


export default Mock.mock(api.getUrlByMsg("get-webshell-connections"),  {
    code: 0,
    msg:"",
    data:[
        {
            createDatetime:Date.now(),
            webshellType:"PHP",
            url:"http://sdfsdf.com/1.php",
            ip:"127.0.0.1",
            note:"test123",
            key:"123"
        },
        {
            createDatetime:Date.now()+300,
            webshellType:"ASP_NET_CS",
            url:"http://sdfsdf.com/1.aspx",
            ip:"127.0.0.1",
            note:"nbnbnb",
            key:"321"
        }
    ]
})
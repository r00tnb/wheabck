import Mock from 'mockjs'
import api from '../api'

Mock.mock(api.getUrlByMsg('test'),'post',(option:any)=>{
    const data = JSON.parse(option.body)
    return data
})
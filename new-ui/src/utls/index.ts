
/**
 * 生成随机字符串
 * @param length 随机字符串的长度
 * @param words 随机字符的范围
 * @returns 随机字符串
 */
export function randomStr(length=16, words="0123456789abcd"):string {
    let result = ''
    for(let i=0, j=0;i<length;i++){
        j = Math.ceil(Math.random()*words.length)
        result += words.charAt(j)
    }
    return result
}


/**
 * 在数组中查找元素的指定键的值是否在数组中有重复，有则返回所有重复的值的数组,否则返回所有值的数组。
 * 如：
 *  数组var a=[{id:1}, {id:2}, {id:1}]， 则在执行findArrayElementCommonValues(a, 'id')后将会返回重复键值的数组[1]
 * @param arr 待查询的数组
 * @param keyName 需要查找的键名
 */
export function findArrayElementCommonValues<T, V>(arr:T[], keyName:string):V[]{
    interface TempV {
        value:V,
        count:number
    }
    if(arr.length===0 || !(arr[0] as Object).hasOwnProperty(keyName)) return []
    let temp:TempV[] = [] 
    let result:V[] = []
    arr.forEach(item=>{
        let v = (item as any)[keyName]
        if(!temp.some(t=>{
            if(t.value===v){
                t.count += 1
            }
            return t.value===v
        })){
            temp.push({
                value:v,
                count:0
            })
        }
    })
    
    if(temp.some(t=>t.count>1)){
        temp.forEach(t=>{
            if(t.count>1)
                result.push(t.value)
        })
    }else{
        result = temp.map(t=>t.value)
    }
    return result
}
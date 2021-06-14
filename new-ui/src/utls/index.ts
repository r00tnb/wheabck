
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
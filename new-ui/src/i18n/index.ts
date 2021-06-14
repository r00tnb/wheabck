import zh_CN from './locale/zh_CN.json'
import intl from 'react-intl-universal'

const lang = (navigator.languages && navigator.languages[0]) || navigator.language

intl.init({
    currentLocale: lang,
    locales:{
        'zh-CN':zh_CN
    }
})

/**
 * 根据键获取对应的国际化字符串，若没找到则返回键值
 * @param key i18n键值
 * @returns 返回指定键对应的值
 */
export function t(key:string):string{
    const result = intl.get(key)
    return result===''?key:result
} 

export {lang}
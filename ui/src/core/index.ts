/**
 * 实现全局对象wheabck，用于插件进行通用操作
 */
import {ComponentPublicInstance} from 'vue'

export class Wheabck {
    public app: ComponentPublicInstance
    public constructor(app:ComponentPublicInstance){
        this.app = app
    }

}

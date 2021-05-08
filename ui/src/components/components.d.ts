
export declare interface Tab{
    name:string,
    title:string,
    path: string
}

export declare interface MenuItem{
    name:string,
    index:string,
    icon?:string,
    group?:boolean,
    sub?:MenuItem[]
}
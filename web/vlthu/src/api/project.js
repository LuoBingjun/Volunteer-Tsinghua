import request from './request'

export function getProjectDetails(projectID){
    return request({
        url:`/project/detail?projectID=${projectID}`,
        method:'get'
    })
}

export function getProjectList(){
    return request({
        url:'/project/list',
        method:'get'
    })
}

import request from './request'

export function getProjectDetails(projectID){
    return request({
        url:`/project/detail?id=${projectID}`,
        method:'get'
    })
}

export function getProjectApplyList(projectID)
{
    return request({
        url:`/check/ViewApplyInfo?project_id=${projectID}`,
        method:'get'
    })
}

export function checkApplyRecord(applyID,checked)
{
    //console.log(applyID,checked)
    return request({
        url:`/check/CheckOp`,
        method:`post`,
        data:{
            apply_id:applyID,
            checked:checked
        }
    })
}

export function getProjectList(){
    return request({
        url:'/project/list',
        method:'get'
    })
}

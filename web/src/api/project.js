import request from '@/utils/request'

export function getProjectDetails(projectID){
    return request({
        url:`/project/detail?id=${projectID}`,
        method:'get'
    })
}

export function deleteProject(projectID)
{
    return request({
        url:'/project/cancel',
        method:'post',
        data:{
            project_id:projectID
        }
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
        url:'/my/allproject',
        method:'get'
    })
}

export function downloadExcel(projectID){
    return request({
        url:`/worktime/Export?project_id=${projectID}`,
        method:'get'
    })
}

export function uploadExcel(options){
    return request({
        url:`/worktime/import`,
        method:'post',
        data:options
    })
}

export function startSign(options)
{
    return request({
        url:"/sign/project",
        method:"post",
        data:options
    })
}

export function startProject(options)
{
    return request({
        method:"post",
        url: '/project/detail',
        data:options
    })
}

export function endProject(id,options)
{
    return request({
        method:"put",
        url:`/project/detail?id=${id}`,
        data:{
            "finished":true
        }
    })
}

export function getProjectJoinList(id)
{
    return request({
        method:"get",
        url:`/worktime/viewjoininfo?project_id=${id}`
    })
}
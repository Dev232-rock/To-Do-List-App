var Edit = document.getElementsByClassName('edit');
var Delete = document.getElementsByClassName('delete');
var Done = document.getElementsByClassName('done');


//  edit section START 
var Modal_Edit = document.querySelector('#Modal-Edit');
var CloseModal_edit = document.querySelector('#Close-Modal');
for (let i = 0 ; i < Edit.length; i++)
{   
    Edit[i].addEventListener('click',function(){
        Modal_Edit.style.display="block";
    });
}
CloseModal_edit.addEventListener('click',function(){
    Modal_Edit.style.display="none";
});
//  edit section END 


//  delete section Start 
var Modal_Delete = document.querySelector('#Modal-Delete');
var CloseModal_delete = document.querySelector('#Close-Modal-edit');

for(let i = 0 ; i< Delete.length; i++)
{   
    Delete[i].addEventListener('click', function(){
        Modal_Delete.style.display="block";
    });
}

CloseModal_delete.addEventListener('click',function(){
    Modal_Delete.style.display="none";
});
//  delete section END



// add new task start
var Modal_Add_Task = document.querySelector("#Modal_Add_Task");
var Btn_Add_New_Task = document.querySelector("#Btn_Add-New-Task");
var Close_Modal_Add = document.querySelector("#Close_Btn_Add");

Btn_Add_New_Task.addEventListener('click' , function (){
    Modal_Add_Task.style.display = 'block';
});

Close_Modal_Add.addEventListener('click',function(){
    Modal_Add_Task.style.display = "none";
});
// add new task ENd



// alert adding task
// Not working ned to fix  +Error+
const Task_Name_Field = document.querySelector('#Task_Name_Field');
const Task_Info_Field = document.querySelector('#Task_Info_Field');
const ADD_BTN = document.querySelector('#ADD_BTN');
const alert_add = document.querySelector('.Modal_alert');
const Add_alert_text = document.querySelector('#Add_alert_text');
const form_add_task = document.querySelector('#Form_add_task');


form_add_task.addEventListener('submit',(e) => {
    if (Task_Title_Field.innerHTML.length < 1){
        e.preventDefault()
        Add_alert_text.innerHTML = "Task Name Field Can Not be Empty !" ;
        Modal_alert.style.display = 'block';
    }
    if (Task_Info_Field.innerHTML.length < 1){
        e.preventDefault()
        Add_alert_text.innerHTML = "Info Field Can Not be Empty !" ;
        Modal_alert.style.display = 'block';
    }
    return true;


});
// alert adding task
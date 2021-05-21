webpackJsonp([47],{"8hNE":function(e,t){},DRBO:function(e,t,i){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var a={name:"",props:{},data:function(){var e=this;return{trainList:[],themeList:[],trainFileList:[],staffList:[],isShowQuery:!1,newTrainList:[],currentStaff:"",currentCompletion:2,trainTaskDialog:{dialogVisible:!1,trainTaskForm:{desc:"",checkedDate:"",checkedTheme:"",checkedTrainFile:[],checkedTrainStaff:[]}},trainFileDialog:{dialogVisible:!1,trainFileList:[]},addFileDialog:{dialogVisible:!1,addFileForm:{checkedTheme:"",addThemeName:"",filePath:""},addThemeNameDisabled:!0},scoreDialog:{dialogVisible:!1,scoreForm:{staff:"",theme:"",score:0}},formRules:{score:[{type:"number",required:!0,message:"请输入正确的分数格式",trigger:"blur"}],checkedTheme:[{required:!0,message:"请选择培训主题",trigger:"change"}],addThemeName:[{validator:function(t,i,a){if("新增主题"==e.addFileDialog.addFileForm.checkedTheme){if(!i)return a("主题不能为空");a()}else a()},trigger:"blur"}],checkedDate:[{required:!0,message:"请选择培训时间",trigger:"change"}],checkedTrainFile:[{validator:function(t,i,a){e.trainTaskDialog.trainTaskForm.checkedTrainFile.length?a():a("至少选择一个培训文件")},trigger:"change"}],checkedTrainStaff:[{type:"array",required:!0,message:"请至少选择一个培训人员",trigger:"change"}]}}},computed:{},watch:{},methods:{getTrainList:function(){var e=this;this.$api2.getTrainList().then(function(t){e.trainList=t.data.data,console.log(t.data),e.themeList=t.data.train_theme_file_data,console.log(e.themeList),e.staffList=t.data.users})},addTask:function(){this.trainTaskDialog.dialogVisible=!0},gatherFile:function(){var e=this;this.$api2.gatherTrainFile().then(function(t){e.trainFileDialog.trainFileList=t.data.data}),this.trainFileDialog.dialogVisible=!0},addFile:function(){this.themeList.push({train_theme:"新增主题"}),this.addFileDialog.addThemeNameDisabled=!0,this.addFileDialog.dialogVisible=!0},newThemeChange:function(e){this.addFileDialog.addThemeNameDisabled="新增主题"!=e},fileChange:function(e){console.log(e),this.addFileDialog.addFileForm.filePath=e.target.files[0],console.log("上传文件",this.addFileDialog.addFileForm.filePath),console.log(this.addFileDialog.addFileForm.filePath)},addFileConfirm:function(){var e=this;this.$refs.addFileRef.validate(function(t){if(t){var i=new FormData;"新增主题"==e.addFileDialog.addFileForm.checkedTheme?(i.append("train_theme",e.addFileDialog.addFileForm.addThemeName),console.log("aaabbb")):(i.append("train_theme",e.addFileDialog.addFileForm.checkedTheme),console.log("ccccc")),i.append("train_file",e.addFileDialog.addFileForm.filePath),e.$api2.addTrainFile(i).then(function(t){t&&(e.$message.success("新增培训文档成功"),e.getTrainList(),console.log("拿到input",e.$refs.uploadTrainDoc),e.$refs.uploadTrainDoc.value="",e.addFileDialog.addFileForm={checkedTheme:"",addThemeName:"",filePath:""},e.addFileDialog.dialogVisible=!1)})}})},themeChange:function(e){var t=this;console.log(e),this.themeList.forEach(function(i){i.train_theme==e&&(t.trainFileList=i.train_files)})},removeTrainFile:function(e,t){var i=this;this.$confirm("此操作将永久删除此培训文档, 是否继续?","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then(function(){i.$api2.removeTrainFile(e,t).then(function(e){e&&(i.$message.success("删除成功"),i.trainFileDialog.dialogVisible=!1)})}).catch(function(){i.$message({type:"info",message:"已取消删除"})})},addTaskConfirm:function(){var e=this;this.$refs.trainTaskRef.validate(function(t){if(t){var i=new FormData;i.append("train_date",e.trainTaskDialog.trainTaskForm.checkedDate),i.append("train_theme",e.trainTaskDialog.trainTaskForm.checkedTheme);var a=e.trainTaskDialog.trainTaskForm.checkedTrainFile.join(",");console.log(a),i.append("train_file",a);var r=e.trainTaskDialog.trainTaskForm.checkedTrainStaff.join(",");console.log(r),i.append("train_user",r),i.append("train_remarks",e.trainTaskDialog.trainTaskForm.desc),console.log(i),e.$api2.addTrainTask(i).then(function(t){t&&(console.log(t),e.$message.success("添加任务成功"),e.trainTaskDialog.dialogVisible=!1,e.getTrainList())})}})},score:function(e,t){this.scoreDialog.scoreForm.staff=e,this.scoreDialog.scoreForm.theme=t,this.scoreDialog.dialogVisible=!0},scoreConfirm:function(){var e=this;this.$refs.scoreFormRef.validate(function(t){t&&e.$api2.trainScore(e.scoreDialog.scoreForm.staff,e.scoreDialog.scoreForm.theme,e.scoreDialog.scoreForm.score).then(function(t){e.getTrainList(),e.scoreDialog.dialogVisible=!1,e.scoreDialog.scoreForm.score=0})})},staffCommand:function(e){""==this.currentStaff?this.currentStaff=e:this.currentStaff!=e&&(this.currentStaff=e,this.newTrainList=[]),this.isShowQuery=!0,0==this.newTrainList.length&&(this.newTrainList=this.$utils.deepClone(this.trainList));for(var t=0;t<this.newTrainList.length;t++)e!=this.newTrainList[t].train_user&&(this.newTrainList.splice(t,1),t--)},finishCommand:function(e){if(2==this.currentCompletion?this.currentCompletion=e:this.currentCompletion!=e&&(this.currentCompletion=e,this.newTrainList=[]),console.log(e),this.isShowQuery=!0,0==this.newTrainList.length&&(this.newTrainList=this.$utils.deepClone(this.trainList)),1==e)for(var t=0;t<this.newTrainList.length;t++)this.newTrainList[t].score||(this.newTrainList.splice(t,1),t--);else for(var i=0;i<this.newTrainList.length;i++)this.newTrainList[i].score&&(this.newTrainList.splice(i,1),i--)},trainTaskDialogClose:function(){this.$refs.trainTaskRef.resetFields()},addFileDialogClose:function(){this.$refs.addFileRef.resetFields()},scoreDialogClose:function(){this.$refs.scoreFormRef.resetFields()}},created:function(){this.getTrainList()},mounted:function(){}},r={render:function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{staticClass:"con"},[i("div",{staticClass:"train_record table_box"},[i("table",{staticClass:"table"},[e._m(0),e._v(" "),e.isShowQuery?i("tbody",[i("tr",[i("td",[e._v("序号")]),e._v(" "),i("td",[e._v("培训时间")]),e._v(" "),i("td",[e._v("培训主题")]),e._v(" "),i("td",[i("el-dropdown",{attrs:{trigger:"click"},on:{command:e.staffCommand}},[i("span",{staticClass:"el-dropdown-link"},[e._v("\n                培训人员\n                "),i("i",{staticClass:"el-icon-arrow-down el-icon--right"})]),e._v(" "),i("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},e._l(e.staffList,function(t,a){return i("el-dropdown-item",{key:a,attrs:{command:t.real_name}},[e._v(e._s(t.real_name))])}),1)],1)],1),e._v(" "),i("td",[e._v("培训文件")]),e._v(" "),i("td",[i("el-dropdown",{attrs:{trigger:"click"},on:{command:e.finishCommand}},[i("span",{staticClass:"el-dropdown-link"},[e._v("\n                完成情况\n                "),i("i",{staticClass:"el-icon-arrow-down el-icon--right"})]),e._v(" "),i("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},[i("el-dropdown-item",{attrs:{command:"1"}},[e._v("已完成")]),e._v(" "),i("el-dropdown-item",{attrs:{command:"0"}},[e._v("未完成")])],1)],1)],1),e._v(" "),i("td",[e._v("分数")]),e._v(" "),i("td",[e._v("备注")]),e._v(" "),i("td",[e._v("操作")])]),e._v(" "),e._l(e.newTrainList,function(t,a){return i("tr",{key:a},[i("td",[e._v(e._s(a+1))]),e._v(" "),i("td",[e._v(e._s(t.train_date))]),e._v(" "),i("td",[e._v(e._s(t.train_theme))]),e._v(" "),i("td",[e._v(e._s(t.train_user))]),e._v(" "),i("td",[e._v(e._s(t.train_files))]),e._v(" "),t.score?i("td",[e._v("已完成")]):i("td",[e._v("未完成")]),e._v(" "),i("td",[e._v(e._s(t.score))]),e._v(" "),i("td",[e._v(e._s(t.remarks))]),e._v(" "),i("td",[i("el-button",{attrs:{type:"primary",size:"mini"},on:{click:function(i){return e.score(t.train_user,t.train_theme)}}},[e._v("评分")])],1)])})],2):i("tbody",[i("tr",[i("td",[e._v("序号")]),e._v(" "),i("td",[e._v("培训时间")]),e._v(" "),i("td",[e._v("培训主题")]),e._v(" "),i("td",[i("el-dropdown",{attrs:{trigger:"click"},on:{command:e.staffCommand}},[i("span",{staticClass:"el-dropdown-link"},[e._v("\n                培训人员\n                "),i("i",{staticClass:"el-icon-arrow-down el-icon--right"})]),e._v(" "),i("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},e._l(e.staffList,function(t,a){return i("el-dropdown-item",{key:a,attrs:{command:t.user_name}},[e._v(e._s(t.user_name))])}),1)],1)],1),e._v(" "),i("td",[e._v("培训文件")]),e._v(" "),i("td",[i("el-dropdown",{attrs:{trigger:"click"},on:{command:e.finishCommand}},[i("span",{staticClass:"el-dropdown-link"},[e._v("\n                完成情况\n                "),i("i",{staticClass:"el-icon-arrow-down el-icon--right"})]),e._v(" "),i("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},[i("el-dropdown-item",{attrs:{command:"1"}},[e._v("已完成")]),e._v(" "),i("el-dropdown-item",{attrs:{command:"0"}},[e._v("未完成")])],1)],1)],1),e._v(" "),i("td",[e._v("分数")]),e._v(" "),i("td",[e._v("备注")]),e._v(" "),i("td",[e._v("操作")])]),e._v(" "),e._l(e.trainList,function(t,a){return i("tr",{key:a},[i("td",[e._v(e._s(a+1))]),e._v(" "),i("td",[e._v(e._s(t.train_date))]),e._v(" "),i("td",[e._v(e._s(t.train_theme))]),e._v(" "),i("td",[e._v(e._s(t.train_user))]),e._v(" "),i("td",[e._v(e._s(t.train_files))]),e._v(" "),t.score?i("td",[e._v("已完成")]):i("td",[e._v("未完成")]),e._v(" "),i("td",[e._v(e._s(t.score))]),e._v(" "),i("td",[e._v(e._s(t.remarks))]),e._v(" "),i("td",[i("el-button",{attrs:{type:"primary",size:"mini"},on:{click:function(i){return e.score(t.train_user,t.train_theme)}}},[e._v("评分")])],1)])})],2)]),e._v(" "),i("div",{staticClass:"train_operation"},[i("el-button",{attrs:{type:"primary",size:"mini"},on:{click:e.addTask}},[e._v("培训任务新增")]),e._v(" "),i("el-button",{attrs:{type:"primary",size:"mini"},on:{click:e.gatherFile}},[e._v("培训文档汇总")]),e._v(" "),i("el-button",{attrs:{type:"primary",size:"mini"},on:{click:e.addFile}},[e._v("培训文档新增")])],1)]),e._v(" "),i("el-dialog",{attrs:{visible:e.trainTaskDialog.dialogVisible,width:"30%",center:""},on:{"update:visible":function(t){return e.$set(e.trainTaskDialog,"dialogVisible",t)},close:e.trainTaskDialogClose}},[i("el-form",{ref:"trainTaskRef",attrs:{model:e.trainTaskDialog.trainTaskForm,rules:e.formRules,"label-width":"100px"}},[i("el-form-item",{attrs:{label:"培训时间",prop:"checkedDate"}},[i("el-date-picker",{attrs:{type:"date",placeholder:"选择日期",format:"yyyy/MM/dd","value-format":"yyyy/MM/dd"},model:{value:e.trainTaskDialog.trainTaskForm.checkedDate,callback:function(t){e.$set(e.trainTaskDialog.trainTaskForm,"checkedDate",t)},expression:"trainTaskDialog.trainTaskForm.checkedDate"}})],1),e._v(" "),i("el-form-item",{attrs:{label:"培训主题",prop:"checkedTheme"}},[i("el-select",{attrs:{placeholder:"请选择"},on:{change:e.themeChange},model:{value:e.trainTaskDialog.trainTaskForm.checkedTheme,callback:function(t){e.$set(e.trainTaskDialog.trainTaskForm,"checkedTheme",t)},expression:"trainTaskDialog.trainTaskForm.checkedTheme"}},e._l(e.themeList,function(e,t){return i("el-option",{key:t,attrs:{label:e.train_theme,value:e.train_theme}})}),1)],1),e._v(" "),i("el-form-item",{attrs:{label:"培训文件",prop:"checkedTrainFile"}},[e.trainTaskDialog.trainTaskForm.checkedTheme.length>0?i("el-checkbox-group",{model:{value:e.trainTaskDialog.trainTaskForm.checkedTrainFile,callback:function(t){e.$set(e.trainTaskDialog.trainTaskForm,"checkedTrainFile",t)},expression:"trainTaskDialog.trainTaskForm.checkedTrainFile"}},e._l(e.trainFileList,function(e,t){return i("el-checkbox",{key:t,attrs:{label:e}})}),1):e._e()],1),e._v(" "),i("el-form-item",{attrs:{label:"培训人员",prop:"checkedTrainStaff"}},[i("el-checkbox-group",{model:{value:e.trainTaskDialog.trainTaskForm.checkedTrainStaff,callback:function(t){e.$set(e.trainTaskDialog.trainTaskForm,"checkedTrainStaff",t)},expression:"trainTaskDialog.trainTaskForm.checkedTrainStaff"}},e._l(e.staffList,function(e,t){return i("el-checkbox",{key:t,attrs:{label:e.user_name}})}),1)],1),e._v(" "),i("el-form-item",{attrs:{label:"备注",prop:"desc"}},[i("el-input",{attrs:{type:"textarea"},model:{value:e.trainTaskDialog.trainTaskForm.desc,callback:function(t){e.$set(e.trainTaskDialog.trainTaskForm,"desc",t)},expression:"trainTaskDialog.trainTaskForm.desc"}})],1)],1),e._v(" "),i("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[i("el-button",{attrs:{type:"primary"},on:{click:e.addTaskConfirm}},[e._v("确定新增")])],1)],1),e._v(" "),i("el-dialog",{attrs:{visible:e.trainFileDialog.dialogVisible,width:"50%",center:""},on:{"update:visible":function(t){return e.$set(e.trainFileDialog,"dialogVisible",t)}}},[i("table",[i("thead",[i("tr",[i("th",[e._v("培训主题")]),e._v(" "),i("th",[e._v("培训文件名")]),e._v(" "),i("th",[e._v("上传时间")]),e._v(" "),i("th",[e._v("操作")])])]),e._v(" "),i("tbody",e._l(e.trainFileDialog.trainFileList,function(t,a){return i("tr",{key:a},[i("td",[e._v(e._s(t.train_theme))]),e._v(" "),i("td",[e._v(e._s(t.train_file))]),e._v(" "),i("td",[e._v(e._s(t.upload_date))]),e._v(" "),i("td",[i("el-button",{attrs:{type:"danger",size:"mini"},on:{click:function(i){return e.removeTrainFile(t.train_theme,t.train_file)}}},[e._v("删除")])],1)])}),0)])]),e._v(" "),i("el-dialog",{attrs:{visible:e.addFileDialog.dialogVisible,width:"30%",center:""},on:{"update:visible":function(t){return e.$set(e.addFileDialog,"dialogVisible",t)},close:e.addFileDialogClose}},[i("el-form",{ref:"addFileRef",attrs:{model:e.addFileDialog.addFileForm,rules:e.formRules,"label-width":"100px"}},[i("el-form-item",{attrs:{label:"培训主题",prop:"checkedTheme"}},[i("el-select",{attrs:{placeholder:"请选择"},on:{change:e.newThemeChange},model:{value:e.addFileDialog.addFileForm.checkedTheme,callback:function(t){e.$set(e.addFileDialog.addFileForm,"checkedTheme",t)},expression:"addFileDialog.addFileForm.checkedTheme"}},e._l(e.themeList,function(e,t){return i("el-option",{key:t,attrs:{label:e.train_theme,value:e.train_theme}})}),1)],1),e._v(" "),i("el-form-item",{attrs:{label:"添加主题",prop:"addThemeName"}},[i("el-input",{attrs:{disabled:e.addFileDialog.addThemeNameDisabled},model:{value:e.addFileDialog.addFileForm.addThemeName,callback:function(t){e.$set(e.addFileDialog.addFileForm,"addThemeName",t)},expression:"addFileDialog.addFileForm.addThemeName"}})],1),e._v(" "),i("el-form-item",{attrs:{label:"上传文件",prop:"file"}},[i("input",{ref:"uploadTrainDoc",attrs:{type:"file"},on:{change:e.fileChange}})])],1),e._v(" "),i("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[i("el-button",{attrs:{type:"primary"},on:{click:e.addFileConfirm}},[e._v("提交")])],1)],1),e._v(" "),i("el-dialog",{attrs:{visible:e.scoreDialog.dialogVisible,width:"30%",center:""},on:{"update:visible":function(t){return e.$set(e.scoreDialog,"dialogVisible",t)},close:e.scoreDialogClose}},[i("el-form",{ref:"scoreFormRef",attrs:{model:e.scoreDialog.scoreForm,"label-width":"80px",rules:e.formRules}},[i("el-form-item",{attrs:{label:"培训人员",prop:"staff"}},[i("el-input",{attrs:{disabled:!0},model:{value:e.scoreDialog.scoreForm.staff,callback:function(t){e.$set(e.scoreDialog.scoreForm,"staff",t)},expression:"scoreDialog.scoreForm.staff"}})],1),e._v(" "),i("el-form-item",{attrs:{label:"培训主题",prop:"theme"}},[i("el-input",{attrs:{disabled:!0},model:{value:e.scoreDialog.scoreForm.theme,callback:function(t){e.$set(e.scoreDialog.scoreForm,"theme",t)},expression:"scoreDialog.scoreForm.theme"}})],1),e._v(" "),i("el-form-item",{attrs:{label:"评分",prop:"score"}},[i("el-input",{model:{value:e.scoreDialog.scoreForm.score,callback:function(t){e.$set(e.scoreDialog.scoreForm,"score",e._n(t))},expression:"scoreDialog.scoreForm.score"}})],1)],1),e._v(" "),i("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[i("el-button",{attrs:{type:"primary"},on:{click:e.scoreConfirm}},[e._v("确 定")])],1)],1)],1)},staticRenderFns:[function(){var e=this.$createElement,t=this._self._c||e;return t("thead",[t("tr",[t("th",{staticStyle:{width:"72vw"},attrs:{colspan:"8"}},[this._v("培训记录")])])])}]};var o=i("VU/8")(a,r,!1,function(e){i("Ny1n"),i("8hNE")},"data-v-28224642",null);t.default=o.exports},Ny1n:function(e,t){}});
//# sourceMappingURL=47.60db6da6b43d9856bfa6.js.map
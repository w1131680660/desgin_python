webpackJsonp([42],{"Ovj/":function(e,t){},VzoP:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r={data:function(){return{form:{log_code:"",dates:"",organization_personnel:"",department:"",theme:""},personlist:[],workdepartments:[],initData:[],tableData:[{log_code:"112",dates:"123",department:"123",organization_personnel:"234",staff_code:"21334",theme:"234"},{log_code:"",dates:"123",department:"123",organization_personnel:"234",staff_code:"21334",theme:"234"}],file:"",insertFlag:!0,curSelectPerson:{},isShowErrogDialog:!1,newFormData:{department:"",organization_personnel:"",theme:"",desc:""},changeThemelist:["主题一","主题二"],log_title:"新增错误日志"}},methods:{uploadFile:function(){this.file=this.$refs.uploadInput.files[0]},showDetail:function(e){this.insertFlag=!1,this.isShowErrogDialog=!0,this.curSelectPerson=e,this.log_title="详情查看"},query:function(){var e=this,t=new FormData;for(var a in this.form)this.form[a]&&this.form[a].length&&t.append(a,this.form[a]);console.log(this.form);this.$axios.post(this._url2+"server/personnel_management/error_log_data/",t).then(function(t){e.tableData=t.data.data})},changeDepartment:function(){var e=this;this.personlist=[],this.initData.forEach(function(t){t.department===e.curSelectPerson.department&&(e.personlist=t.organization_personnel)})},selectDepartment:function(){var e=this;console.log(111),this.personlist=[],this.initData.forEach(function(t){t.department===e.form.department&&(e.personlist=t.organization_personnel)})},onSubmit:function(){var e=this;if(console.log(this.curSelectPerson.theme,this.curSelectPerson.content),this.curSelectPerson.department&&this.curSelectPerson.organization_personnel&&this.curSelectPerson.theme&&this.curSelectPerson.content){var t=new FormData;for(var a in this.curSelectPerson)t.append(a,this.curSelectPerson[a]);this.file&&t.append("file",this.file);this.$axios.post(this._url2+"server/personnel_management/error_log_add/",t).then(function(t){200===t.data.code?(alert("提交成功！"),e.isShowErrogDialog=!1,e.tableData=t.data.data):alert("未提交成！")})}else alert("请选择部门，编制人，主题，内容")},newErrorLog:function(){this.curSelectPerson={},this.insertFlag=!0,this.isShowErrogDialog=!0},closeErrorLog:function(){this.isShowErrogDialog=!1},getSelect:function(){var e=this;this.$axios.get(this._url2+"server/personnel_management/staff_error_log/").then(function(t){console.log(t),e.initData=t.data.data||[],e.initData.forEach(function(t){e.workdepartments.push(t.department)})})},getTable:function(){var e=this;this.$axios.post(this._url2+"server/personnel_management/error_log_data/").then(function(t){e.tableData=t.data.data||[]})}},created:function(){this.getSelect(),this.getTable()}},n={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"error_log"},[a("div",{staticClass:"topOpt"},[a("el-form",{attrs:{inline:!0,model:e.form,"label-width":"80px"}},[a("el-form-item",{attrs:{label:"日志编号"}},[a("el-input",{model:{value:e.form.log_code,callback:function(t){e.$set(e.form,"log_code",t)},expression:"form.log_code"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"日期"}},[a("el-date-picker",{attrs:{"value-format":"yyyy-MM-dd",type:"date",placeholder:"选择日期"},model:{value:e.form.dates,callback:function(t){e.$set(e.form,"dates",t)},expression:"form.dates"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"部门"}},[a("el-select",{attrs:{placeholder:"请选择"},on:{change:e.selectDepartment},model:{value:e.form.department,callback:function(t){e.$set(e.form,"department",t)},expression:"form.department"}},e._l(e.workdepartments,function(e){return a("el-option",{key:e,attrs:{label:e,value:e}})}),1)],1),e._v(" "),a("el-form-item",{attrs:{label:"编制人"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.form.organization_personnel,callback:function(t){e.$set(e.form,"organization_personnel",t)},expression:"form.organization_personnel"}},e._l(e.personlist,function(e){return a("el-option",{key:e,attrs:{label:e,value:e}})}),1)],1),e._v(" "),a("el-form-item",{attrs:{label:"主题搜索"}},[a("el-input",{model:{value:e.form.theme,callback:function(t){e.$set(e.form,"theme",t)},expression:"form.theme"}})],1),e._v(" "),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:e.query}},[e._v("查询")])],1)],1)],1),e._v(" "),a("div",{staticClass:"table_con"},[a("h2",[e._v("错误日志")]),e._v(" "),a("el-button",{staticClass:"addNewBtn",attrs:{type:"primary"},on:{click:e.newErrorLog}},[e._v("新增")]),e._v(" "),a("el-table",{staticStyle:{width:"100%"},attrs:{data:e.tableData}},[a("el-table-column",{attrs:{align:"center",type:"index",label:"序号",width:"180"}}),e._v(" "),a("el-table-column",{attrs:{align:"center",prop:"log_code",label:"日志编号",width:"180"}}),e._v(" "),a("el-table-column",{attrs:{align:"center",prop:"dates",label:"日期"}}),e._v(" "),a("el-table-column",{attrs:{align:"center",prop:"organization_personnel",label:"编制人"}}),e._v(" "),a("el-table-column",{attrs:{align:"center",prop:"staff_code",label:"员工编码"}}),e._v(" "),a("el-table-column",{attrs:{align:"center",prop:"department",label:"部门"}}),e._v(" "),a("el-table-column",{attrs:{align:"center",prop:"theme",label:"主题"}}),e._v(" "),a("el-table-column",{attrs:{align:"center",label:"查看"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("a",{attrs:{href:"javascript:;"},on:{click:function(a){return e.showDetail(t.row)}}},[e._v("查看详情")])]}}])})],1)],1),e._v(" "),a("el-dialog",{staticStyle:{"text-align":"center"},attrs:{title:e.log_title,visible:e.isShowErrogDialog,width:"30%"},on:{"update:visible":function(t){e.isShowErrogDialog=t}}},[a("div",[a("div",{staticClass:"error_contain",staticStyle:{padding:"0 113px"}},[a("el-form",{attrs:{model:e.curSelectPerson,"label-width":"80px"}},[a("el-form-item",{attrs:{label:"部门"}},[a("el-select",{attrs:{disabled:!e.insertFlag,placeholder:"请选择"},on:{change:e.changeDepartment},model:{value:e.curSelectPerson.department,callback:function(t){e.$set(e.curSelectPerson,"department",t)},expression:"curSelectPerson.department"}},e._l(e.workdepartments,function(e){return a("el-option",{key:e,attrs:{label:e,value:e}})}),1)],1),e._v(" "),a("el-form-item",{attrs:{label:"编制人"}},[a("el-select",{attrs:{disabled:!e.insertFlag,placeholder:"请选择"},model:{value:e.curSelectPerson.organization_personnel,callback:function(t){e.$set(e.curSelectPerson,"organization_personnel",t)},expression:"curSelectPerson.organization_personnel"}},e._l(e.personlist,function(e){return a("el-option",{key:e,attrs:{label:e,value:e}})}),1)],1),e._v(" "),a("el-form-item",{attrs:{label:"主题搜索"}},[a("el-select",{attrs:{disabled:!e.insertFlag,placeholder:"请选择"},model:{value:e.curSelectPerson.theme,callback:function(t){e.$set(e.curSelectPerson,"theme",t)},expression:"curSelectPerson.theme"}},e._l(e.changeThemelist,function(e){return a("el-option",{key:e,attrs:{label:e,value:e}})}),1)],1),e._v(" "),a("el-form-item",{attrs:{label:"内容"}},[a("el-input",{attrs:{disabled:!e.insertFlag,rows:6,type:"textarea"},model:{value:e.curSelectPerson.content,callback:function(t){e.$set(e.curSelectPerson,"content",t)},expression:"curSelectPerson.content"}})],1),e._v(" "),e.insertFlag?a("el-form-item",[a("span",{staticClass:"uploadlink"},[a("a",{staticClass:"alink",attrs:{href:"javascript:;"}},[e._v("附件上传")]),e._v(" "),a("input",{ref:"uploadInput",staticClass:"fileInput",attrs:{type:"file"},on:{change:e.uploadFile}})]),e._v(" "),a("el-button",{attrs:{type:"primary"},on:{click:e.onSubmit}},[e._v("提交")])],1):e._e(),e._v(" "),e.curSelectPerson.files?a("el-form-item",[[a("span",[e._v("文件名："+e._s(e.curSelectPerson.files))])]],2):e._e()],1)],1)])])],1)},staticRenderFns:[]};var l=a("VU/8")(r,n,!1,function(e){a("nkEJ"),a("Ovj/")},"data-v-30382362",null);t.default=l.exports},nkEJ:function(e,t){}});
//# sourceMappingURL=42.ba361352499023629b90.js.map
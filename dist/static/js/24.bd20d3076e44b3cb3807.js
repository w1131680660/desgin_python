webpackJsonp([24],{"5L1+":function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n,l=a("bOdI"),i=a.n(l),o=a("mtWM"),r=a.n(o),s={data:function(){return{editTemplateForm:{problem_type:"",email_content:""},editDialogVisable:!1,editTemplateFormData:"",centerDialogVisible:!1,leftNavData:[],tableList:[],uploadPlatformList:[],restaurants:[],restaurants2:[],restaurants3:[],uploadPlatform:"",uploadCountry:"",uploadLanguage:"",uploadProblemType:"",uploadTextarea:"",total:0,page:1,firstNav:"",twiceNav:"",threeNav:"",Instructions_use:""}},methods:(n={editTemplateSubmit:function(){var t=this;if(""!==this.editTemplateForm.problem_type||""!==this.editTemplateForm.email_content){this.editDialogVisable=!1;var e=this._url2+"server/customer_management/email_template_manage";this.editTemplateFormData.append("problem_type",this.editTemplateForm.problem_type),this.editTemplateFormData.append("email_content",this.editTemplateForm.email_content);var a=this.formatTime();this.editTemplateFormData.append("upload_time",a),this.$axios.put(e,this.editTemplateFormData).then(function(e){200===e.data.code&&(alert("编辑成功！"),t.getDefaultData())})}else alert("请至少填写其中一个！")},formatTime:function(){var t=new Date;return t.getFullYear()+"-"+(t.getMonth()+1>10?t.getMonth()+1:"0"+(t.getMonth()+1))+"-"+(t.getDate()>10?t.getDate():"0"+t.getDate())},handleClose:function(){this.editDialogVisable=!1,this.$refs.templateForm.resetFields()},querySearch:function(t,e){var a=this.restaurants;e(t?a.filter(this.createFilter(t)):a)},createFilter:function(t){return function(e){return 0===e.value.toLowerCase().indexOf(t.toLowerCase())}},querySearch2:function(t,e){var a=this.restaurants2;e(t?a.filter(this.createFilter(t)):a)}},i()(n,"createFilter",function(t){return function(e){return 0===e.value.toLowerCase().indexOf(t.toLowerCase())}}),i()(n,"querySearch3",function(t,e){var a=this.restaurants3;e(t?a.filter(this.createFilter(t)):a)}),i()(n,"createFilter",function(t){return function(e){return 0===e.value.toLowerCase().indexOf(t.toLowerCase())}}),i()(n,"getDefaultData",function(){var t=this;r()({url:this._url2+"server/customer_management/email_template_manage",method:"get",params:{page:this.page}}).then(function(e){console.log(e),t.tableList=e.data.data,t.restaurants=e.data.country_data,t.restaurants2=e.data.problem_data,t.restaurants3=e.data.language_data,t.uploadPlatformList=e.data.channel_data,t.total=e.data.count[0].count/2})}),i()(n,"NavClick",function(t,e,a){var n=this;this.firstNav=t,this.twiceNav=e,this.threeNav=a,r()({url:this._url2+"server/customer_management/email_template_manage",method:"get",params:{platform:t,country:e,language:a,page:1}}).then(function(t){console.log(t),n.tableList=t.data.data,n.$nextTick(function(){$(".tempalateUploadTable>tbody").scrollTop(0)}),n.total=t.data.count[0].count/2,n.page=1})}),i()(n,"openEdit",function(){for(var t=[],e=document.querySelectorAll(".checkli"),a=0;a<e.length;a++)1==e[a].checked&&t.push(e[a].value);if(1!==t.length)alert("请选中一个数据进行编辑！");else{this.editDialogVisable=!0,console.log(t[0]);var n=this.tableList.find(function(e){return e.id==t[0]});console.log(n),this.editTemplateForm.problem_type=n.problem_type||"",this.editTemplateForm.email_content=n.email_content||"",this.editTemplateFormData=new FormData,this.editTemplateFormData.append("id",t[0])}}),i()(n,"openUpload",function(){this.centerDialogVisible=!0,this.uploadProblemType="",this.uploadTextarea="",this.uploadLanguage="",this.uploadCountry="",this.uploadPlatform="",this.Instructions_use=""}),i()(n,"upLoadSet",function(){this.uploadProblemType="",this.uploadTextarea="",this.uploadLanguage="",this.uploadCountry="",this.Instructions_use="",this.uploadPlatform=""}),i()(n,"addSubmit",function(){var t=this,e=this.checkeChinese(this.uploadCountry),a=this.checkeChinese(this.uploadLanguage),n=this.checkeChinese(this.uploadProblemType);if(""==this.uploadCountry||""==this.uploadPlatform||""==this.uploadLanguage||""==this.uploadProblemType||""==this.uploadTextarea||""==this.Instructions_use||0==e||0==a||0==n)alert("请把所有选项填上（问题类型、国家、语言必须为中文字段）");else{this.centerDialogVisible=!1;var l=new Date,i=l.getFullYear()+"-"+(l.getMonth()+1)+"-"+l.getDate(),o=new FormData;o.append("country",this.uploadCountry),o.append("platform",this.uploadPlatform),o.append("language",this.uploadLanguage),o.append("problem_type",this.uploadProblemType),o.append("email_content",this.uploadTextarea),o.append("upload_time",i),o.append("Instructions_use",this.Instructions_use),o.append("upload_people","上传人2"),this.$axios.post(this._url2+"server/customer_management/email_template_manage",o).then(function(e){200==e.data.code&&(alert("新增成功"),r()({url:t._url2+"server/customer_management/email_template_manage",method:"get",params:{platform:t.firstNav,country:t.twiceNav,language:t.threeNav,page:t.page}}).then(function(e){console.log(e),t.tableList=e.data.data}))})}}),i()(n,"handleCurrentChange",function(t){var e=this;this.page=t,r()({url:this._url2+"server/customer_management/email_template_manage",method:"get",params:{platform:this.firstNav,country:this.twiceNav,language:this.threeNav,page:this.page}}).then(function(t){console.log(t),e.tableList=t.data.data,e.$nextTick(function(){$(".tempalateUploadTable>tbody").scrollTop(0)});for(var a=document.querySelectorAll(".checkli"),n=0;n<a.length;n++)a[n].checked=!1})}),i()(n,"returMai",function(){this.$router.push("/MailTemplateManagement")}),i()(n,"deleteEmail",function(){for(var t=this,e=[],a=document.querySelectorAll(".checkli"),n=0;n<a.length;n++)1==a[n].checked&&e.push(a[n].value);0==e.length?alert("请选中想删除的数据"):this.$confirm("此操作将永久删除选中模板, 是否继续?","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then(function(){t.$axios.delete(t._url2+"server/customer_management/email_template_manage",{params:{id:e}}).then(function(e){if(200==e.data.code){t.$message({type:"success",message:"删除成功!"});for(var a=document.querySelectorAll(".checkli"),n=0;n<a.length;n++)a[n].checked=!1;r()({url:t._url2+"server/customer_management/email_template_manage",method:"get",params:{platform:t.firstNav,country:t.twiceNav,language:t.threeNav,page:t.page}}).then(function(e){t.tableList=e.data.data})}})}).catch(function(){})}),i()(n,"tagClick",function(t){1==document.querySelectorAll(".checkli")[t].checked?document.querySelectorAll(".checkli")[t].checked=!1:document.querySelectorAll(".checkli")[t].checked=!0}),i()(n,"checkeChinese",function(t){return!t.match(/[^\u4e00-\u9fa5]/g)}),n),created:function(){var t=this;this.getDefaultData(),r()({url:this._url2+"server/personnel_management/area_sign2/",method:"get"}).then(function(e){console.log(e,5),t.leftNavData=e.data.data1})}},u={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{attrs:{id:"TemplateUploadManagement"}},[a("el-menu",{staticClass:"leftNav",staticStyle:{width:"12vw",height:"95vh",position:"fixed",left:"0"},attrs:{"unique-opened":""}},t._l(t.leftNavData,function(e,n){return a("el-submenu",{key:n,attrs:{index:n+""}},[a("template",{slot:"title"},[t._v(t._s(n))]),t._v(" "),t._l(e,function(e,l){return a("el-submenu",{key:l,attrs:{index:l+""}},[a("template",{slot:"title"},[t._v(t._s(l))]),t._v(" "),t._l(e,function(e,i){return a("el-menu-item",{key:i,attrs:{index:l+e},on:{click:function(a){return t.NavClick(n,l,e)}}},[t._v(t._s(e))])})],2)})],2)}),1),t._v(" "),a("header",{staticStyle:{color:"white","margin-left":"-1.5vw","font-weight":"800"}},[a("el-button",{attrs:{type:"primary"},on:{click:function(e){return t.openUpload()}}},[t._v("上 传")]),t._v(" "),a("el-button",{attrs:{type:"primary"},on:{click:function(e){return t.openEdit()}}},[t._v("编 辑")]),t._v(" "),a("el-button",{attrs:{type:"danger"},on:{click:function(e){return t.deleteEmail()}}},[t._v("删 除")]),t._v(" "),a("el-button",{attrs:{type:"warning"},on:{click:function(e){return t.returMai()}}},[t._v("所 有")]),t._v(" "),a("span",{staticStyle:{"padding-left":"25vw","font-size":"1.5rem"}},[t._v("上传邮件模板")])],1),t._v(" "),a("footer",[a("table",{staticClass:"tempalateUploadTable"},[t._m(0),t._v(" "),a("tbody",t._l(t.tableList,function(e,n){return a("tr",{key:n},[a("td",[a("input",{staticClass:"checkli",attrs:{type:"checkbox"},domProps:{value:e.id}})]),t._v(" "),a("td",{on:{click:function(e){return t.tagClick(n)}}},[t._v(t._s(n+1+50*(t.page-1)))]),t._v(" "),a("td",{on:{click:function(e){return t.tagClick(n)}}},[t._v(t._s(e.platform))]),t._v(" "),a("td",{on:{click:function(e){return t.tagClick(n)}}},[t._v(t._s(e.country))]),t._v(" "),a("td",{on:{click:function(e){return t.tagClick(n)}}},[t._v(t._s(e.language))]),t._v(" "),a("td",{on:{click:function(e){return t.tagClick(n)}}},[t._v(t._s(e.problem_type))]),t._v(" "),a("td",{on:{click:function(e){return t.tagClick(n)}}},[t._v(t._s(e.Instructions_use))]),t._v(" "),a("td",{on:{click:function(e){return t.tagClick(n)}}},[a("div",{staticClass:"tdDiv"},[t._v(t._s(e.email_content))])]),t._v(" "),a("td",{on:{click:function(e){return t.tagClick(n)}}},[t._v(t._s(e.upload_people))]),t._v(" "),a("td",{on:{click:function(e){return t.tagClick(n)}}},[t._v(t._s(e.upload_time))])])}),0)]),t._v(" "),a("el-pagination",{staticClass:"pagetotle",staticStyle:{margin:"1vh 0 0 44vw"},attrs:{background:"","current-page":t.page,layout:"prev, pager, next, jumper",total:t.total},on:{"current-change":t.handleCurrentChange}})],1),t._v(" "),a("el-dialog",{attrs:{title:"上传邮件模板文件",visible:t.centerDialogVisible,"close-on-click-modal":!1,width:"42%",center:""},on:{"update:visible":function(e){t.centerDialogVisible=e}}},[a("span",[a("div",{staticClass:"mainTop"},[a("div",{staticStyle:{position:"relative"}},[a("span",{staticStyle:{position:"absolute",top:"1.2vh",left:"0vw"}},[t._v("国家：")]),t._v(" "),a("span",{staticStyle:{position:"absolute",top:"6vh",left:"-1.4vw"}},[t._v("问题类型：")]),t._v(" "),a("span",{staticStyle:{position:"absolute",top:"6vh"}},[t._v("语言：")]),t._v(" "),a("span",[t._v("渠道：\n            "),a("el-select",{attrs:{placeholder:"请选择"},model:{value:t.uploadPlatform,callback:function(e){t.uploadPlatform=e},expression:"uploadPlatform"}},t._l(t.uploadPlatformList,function(t){return a("el-option",{key:t.value,attrs:{label:t.label,value:t.value}})}),1)],1),t._v(" "),a("span",{staticStyle:{"margin-left":"1.5vw"}},[a("el-col",{attrs:{span:25}},[a("el-autocomplete",{staticClass:"inline-input",staticStyle:{margin:"0 1.7vw 0 2.5vw",width:"11.2vw"},attrs:{"fetch-suggestions":t.querySearch,placeholder:"请输入内容"},model:{value:t.uploadCountry,callback:function(e){t.uploadCountry=e},expression:"uploadCountry"}})],1)],1)]),t._v(" "),a("div",[a("span",[a("el-col",{attrs:{span:25}},[a("el-autocomplete",{staticClass:"inline-input",staticStyle:{margin:"0 1.7vw 0 2.5vw",width:"11.2vw"},attrs:{"fetch-suggestions":t.querySearch2,placeholder:"请输入内容"},model:{value:t.uploadProblemType,callback:function(e){t.uploadProblemType=e},expression:"uploadProblemType"}})],1)],1),t._v(" "),a("span",[a("el-col",{attrs:{span:25}},[a("el-autocomplete",{staticClass:"inline-input",staticStyle:{margin:"0 1.7vw 0 2.5vw",width:"11.2vw"},attrs:{"fetch-suggestions":t.querySearch3,placeholder:"请输入内容"},model:{value:t.uploadLanguage,callback:function(e){t.uploadLanguage=e},expression:"uploadLanguage"}})],1)],1)]),t._v(" "),a("div",[a("span",{staticClass:"textareaspan"},[t._v("请输入模板：（直接输入文字）")]),t._v(" "),a("textarea",{directives:[{name:"model",rawName:"v-model",value:t.uploadTextarea,expression:"uploadTextarea"}],staticStyle:{"font-size":"0.9rem","line-height":"2.2vh",height:"20vh",resize:"none"},attrs:{name:"",id:"",cols:"50"},domProps:{value:t.uploadTextarea},on:{input:function(e){e.target.composing||(t.uploadTextarea=e.target.value)}}}),t._v(" "),a("br"),t._v(" "),a("span",[t._v("适用情况(直接输入文字)")]),a("br"),t._v(" "),a("textarea",{directives:[{name:"model",rawName:"v-model",value:t.Instructions_use,expression:"Instructions_use"}],staticStyle:{"font-size":"0.9rem","line-height":"2.2vh",height:"20vh",resize:"none","margin-top":"0"},attrs:{name:"",id:"",cols:"50"},domProps:{value:t.Instructions_use},on:{input:function(e){e.target.composing||(t.Instructions_use=e.target.value)}}})])])]),t._v(" "),a("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(e){t.centerDialogVisible=!1}}},[t._v("取 消")]),t._v(" "),a("el-button",{attrs:{type:"warning"},on:{click:function(e){return t.upLoadSet()}}},[t._v("重 置")]),t._v(" "),a("el-button",{attrs:{type:"primary"},on:{click:function(e){return t.addSubmit()}}},[t._v("提 交")])],1)]),t._v(" "),a("el-dialog",{attrs:{title:"编辑",visible:t.editDialogVisable,width:"20%","before-close":t.handleClose},on:{"update:visible":function(e){t.editDialogVisable=e}}},[a("el-form",{ref:"templateForm",attrs:{model:t.editTemplateForm,"label-width":"100px",inline:!0}},[a("el-form-item",{attrs:{label:"售后类型",prop:"problem_type"}},[a("el-input",{attrs:{type:"textarea",rows:2},model:{value:t.editTemplateForm.problem_type,callback:function(e){t.$set(t.editTemplateForm,"problem_type",e)},expression:"editTemplateForm.problem_type"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"邮件回复模板",prop:"email_content"}},[a("el-input",{attrs:{type:"textarea",rows:5},model:{value:t.editTemplateForm.email_content,callback:function(e){t.$set(t.editTemplateForm,"email_content",e)},expression:"editTemplateForm.email_content"}})],1),t._v(" "),a("el-form-item",[a("el-button",{on:{click:t.handleClose}},[t._v("取 消")]),t._v(" "),a("el-button",{attrs:{type:"primary"},on:{click:t.editTemplateSubmit}},[t._v("确 定")])],1)],1)],1)],1)},staticRenderFns:[function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("thead",[a("tr",[a("th"),t._v(" "),a("th",[t._v("序号")]),t._v(" "),a("th",[t._v("渠道")]),t._v(" "),a("th",[t._v("对应国家")]),t._v(" "),a("th",[t._v("语言")]),t._v(" "),a("th",[t._v("售后类型")]),t._v(" "),a("th",[t._v("适用情况")]),t._v(" "),a("th",[t._v("邮件回复模板")]),t._v(" "),a("th",[t._v("上传人")]),t._v(" "),a("th",[t._v("上传时间")])])])}]};var c=a("VU/8")(s,u,!1,function(t){a("s9VX"),a("Ittl")},"data-v-f124bf9c",null);e.default=c.exports},Ittl:function(t,e){},s9VX:function(t,e){}});
//# sourceMappingURL=24.bd20d3076e44b3cb3807.js.map
webpackJsonp([52],{ToRl:function(t,e){},golq:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var l=a("mvHQ"),s=a.n(l),n={data:function(){return{taskForm:{warehouse_name:"",template_type:"",country:"",reason:"",station:""},task_warehouses:[],task_countries:[],task_stations:[],task_templateTypes:[],templateTable:[],templateChangeForm:{warehouse_name:"",template_type:"",country:"",station:""},templateChange_stations:[],templateChange_countries:[],templateChange_warehouses:[],templateChange_templateTypes:[],templateStepList:[{id:1,station:"胤佑",country:"美国",warehouse_name:"品晟美东仓",template_type:"美东仓标准模板",step:"0",title:"（自动化，加急，隔日达，当天达 + 1天备货时间）",content:null,images:null},{id:2,station:"胤佑",country:"美国",warehouse_name:"品晟美东仓",template_type:"美东仓标准模板",step:"1",title:"1、设置仓库",content:"点击设置-配送设置-一般配送设置-编辑-添加新地址，填写仓库地址 美东仓库地址：12 McCullough Dr New Castle，DE 19720,New Castle, DE, 19720, 美国",images:"mdc_step1.png"},{id:3,station:"胤佑",country:"美国",warehouse_name:"品晟美东仓",template_type:"美东仓标准模板",step:"2",title:"2、配送模板",content:"创建新配送模板并命名",images:"mdc_step2.png"},{id:4,station:"胤佑",country:"美国",warehouse_name:"品晟美东仓",template_type:"美东仓标准模板",step:"3",title:"3、设置模板",content:"选择美东仓库-下一步-选择承运人配送服务（此处为FedEx配送）",images:"mdc_step3_1.png,mdc_step3_2.png"},{id:5,station:"胤佑",country:"美国",warehouse_name:"品晟美东仓",template_type:"美东仓标准模板",step:"4",title:"4.下一步-完成",content:"勾选自动化，标准运输时间，设置为2-4天，偏远地区为5-8天，且运费为4.99，每磅0.99刀",images:"mdc_step4_1.png,mdc_step4_2.png"},{id:6,station:"胤佑",country:"美国",warehouse_name:"品晟美东仓",template_type:"美东仓标准模板",step:"5",title:"5、库存-商品页面-选择相应的配送模板-报价-处理时间-1天",content:"",images:"mdc_step5.png"}],templateStepList_:{},dialogImageUrl:"",dialogVisible:!1,disabled:!1}},methods:{addNewTask:function(){var t=this,e=this._url2+"server/order_management/add_work/",a={};for(var l in this.taskForm){if(0===this.taskForm[l].length)return void alert("请选择渠道站点国家更改原因及模板类型！");a[l]=this.taskForm[l]}this.$axios.get(e,{params:a}).then(function(e){console.log(e),200===e.data.code?(alert("提交成功！"),t.taskForm.warehouse_name="",t.taskForm.template_type="",t.taskForm.country="",t.taskForm.reason="",t.taskForm.station=""):alert("提交未成功！")})},approved:function(t,e){var a=this;console.log(t,e);var l=e[t],s=this._url2+"server/order_management/examined_template_update/";this.$axios.get(s,{params:{id:l.id,station:l.station,country:l.country,warehouse_name:l.warehouse_name}}).then(function(t){a.templateTable=t.data.data})},reject:function(t,e){console.log(t,e)},hTitle_placeholder:function(t){return"请输入步骤标题，示例："+this.templateStepList_[t].title},hTip_placeholder:function(t){return"请输入步骤标题，示例："+this.templateStepList_[t].content},changeOpt1:function(){var t=this;this.task_warehouses=[],this.task_stations=[],this.taskForm.warehouse_name="",this.taskForm.station="";var e=this._url2+"server/order_management/warehouse_datas/";this.$axios.get(e,{params:{country:this.taskForm.country}}).then(function(e){t.task_warehouses=e.data.data});var a=this._url2+"server/personnel_management/get_sign_area/";this.$axios.get(a,{params:{country:this.taskForm.country}}).then(function(e){t.task_stations=e.data.data})},changeOpt2:function(){var t=this,e=this._url2+"server/order_management/warehouse_datas/";this.$axios.get(e,{params:{country:this.templateChangeForm.country}}).then(function(e){t.templateChange_warehouses=e.data.data});var a=this._url2+"server/personnel_management/get_sign_area/";this.$axios.get(a,{params:{country:this.templateChangeForm.country}}).then(function(e){t.templateChange_stations=e.data.data})},handleRemove:function(t,e){console.log(this.$refs[e][0].uploadFiles),console.log(e);var a=this.$refs[e][0].uploadFiles;console.log(t.uid,a);var l=a.findIndex(function(e){return e.uid===t.uid});a.splice(l,1)},handlePictureCardPreview:function(t){this.dialogImageUrl=t.url,this.dialogVisible=!0},submitImg:function(t){this.$refs[t][0].submit()},submitFormData:function(){var t=this,e=new FormData,a=[];for(var l in this.templateStepList){var n={},o=this.templateStepList[l];for(var r in o)"id"!==r&&"images"!==r&&(n[r]=o[r]);a.push(n)}var i=s()(a);e.append("data",i),console.log("打印数据",e);for(var m=this.templateStepList.length,p=function(a){t.$refs["uploadImg"+a][0].uploadFiles.forEach(function(t){console.log(t),e.append("files"+a,t.raw)})},c=1;c<m;c++)p(c);this.$axios.post(this._url2+"server/order_management/template_datas_update/",e).then(function(t){console.log(t),200===t.data.code?alert("修改模板成功！"):alert("提交出错！")})},getSelect:function(){var t=this,e=s()(this.templateStepList);this.templateStepList_=JSON.parse(e);var a=this._url2+"server/personnel_management/get_sign_country/";this.$axios.get(a).then(function(e){t.task_countries=e.data.data,t.templateChange_countries=e.data.data});var l=this._url2+"server/order_management/get_template/";this.$axios.get(l).then(function(e){t.task_templateTypes=e.data.data,t.templateChange_templateTypes=e.data.data})},getData:function(){var t=this,e=this._url2+"server/order_management/get_examined_data/";this.$axios.get(e).then(function(e){t.templateTable=e.data.data})},getTemplate:function(){var t=this;for(var e in this.templateChangeForm)if(!this.templateChangeForm[e])return void alert("请选择国家站点仓库名及模板类型");this.$axios.get(this._url2+"server/order_management/template_datas/",{params:{station:this.templateChangeForm.station,country:this.templateChangeForm.country,warehouse_name:this.templateChangeForm.warehouse_name,template_type:this.templateChangeForm.template_type}}).then(function(e){console.log(e),t.templateStepList=e.data.data})}},components:{},created:function(){this.getSelect(),this.getData()}},o={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{attrs:{id:"SupervisorPage"}},[a("div",{staticClass:"addNewTask"},[a("h2",[t._v("新增任务")]),t._v(" "),a("div",[a("el-form",{attrs:{model:t.taskForm,inline:!0}},[a("el-form-item",{attrs:{label:"国家"}},[a("el-select",{attrs:{placeholder:"请选择国家"},on:{change:t.changeOpt1},model:{value:t.taskForm.country,callback:function(e){t.$set(t.taskForm,"country",e)},expression:"taskForm.country"}},t._l(t.task_countries,function(t,e){return a("el-option",{key:e,attrs:{label:t,value:t}})}),1)],1),t._v(" "),a("el-form-item",{attrs:{label:"站点"}},[a("el-select",{attrs:{placeholder:"请选择站点"},model:{value:t.taskForm.station,callback:function(e){t.$set(t.taskForm,"station",e)},expression:"taskForm.station"}},t._l(t.task_stations,function(t,e){return a("el-option",{key:e,attrs:{label:t,value:t}})}),1)],1),t._v(" "),a("el-form-item",{attrs:{label:"仓库"}},[a("el-select",{attrs:{placeholder:"请选择需要更改的仓库"},model:{value:t.taskForm.warehouse_name,callback:function(e){t.$set(t.taskForm,"warehouse_name",e)},expression:"taskForm.warehouse_name"}},t._l(t.task_warehouses,function(t,e){return a("el-option",{key:e,attrs:{label:t.warehouse_name,value:t.warehouse_name}})}),1)],1),t._v(" "),a("el-form-item",{attrs:{label:"更换原因"}},[a("el-input",{attrs:{placeholder:"请输入更换原因",type:"text"},model:{value:t.taskForm.reason,callback:function(e){t.$set(t.taskForm,"reason",e)},expression:"taskForm.reason"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"模板类型"}},[a("el-select",{attrs:{placeholder:"请选择模板类型"},model:{value:t.taskForm.template_type,callback:function(e){t.$set(t.taskForm,"template_type",e)},expression:"taskForm.template_type"}},t._l(t.task_templateTypes,function(t,e){return a("el-option",{key:e,attrs:{label:t,value:t}})}),1)],1),t._v(" "),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:t.addNewTask}},[t._v("更改仓库模板")])],1)],1)],1)]),t._v(" "),a("div",{staticClass:"checkTemplateUpdate"},[a("h2",[t._v("模板更改审核")]),t._v(" "),a("div",[a("el-table",{staticStyle:{width:"80%",margin:"0 auto"},attrs:{border:"",data:t.templateTable,"max-height":"300"}},[a("el-table-column",{attrs:{align:"center",prop:"country",label:"国家"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"warehouse_name",label:"仓库"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"template_type",label:"模板类型"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"update_times",label:"更新时间"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"update_reason",label:"更新原因"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",label:"操作"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("el-button",{attrs:{type:"primary",size:"small"},nativeOn:{click:function(a){return a.preventDefault(),t.approved(e.$index,t.templateTable)}}},[t._v("\n              通过\n            ")]),t._v(" "),a("el-button",{attrs:{type:"danger",size:"small"},nativeOn:{click:function(a){return a.preventDefault(),t.reject(e.$index,t.templateTable)}}},[t._v("\n              驳回\n            ")])]}}])})],1)],1)]),t._v(" "),a("div",{staticClass:"templateChange"},[a("h2",[t._v("模板更改")]),t._v(" "),a("div",[a("el-form",{attrs:{model:t.templateChangeForm,inline:!0}},[a("el-form-item",{attrs:{label:"国家"}},[a("el-select",{attrs:{placeholder:"请选择国家"},on:{change:t.changeOpt2},model:{value:t.templateChangeForm.country,callback:function(e){t.$set(t.templateChangeForm,"country",e)},expression:"templateChangeForm.country"}},t._l(t.templateChange_countries,function(t,e){return a("el-option",{key:e,attrs:{label:t,value:t}})}),1)],1),t._v(" "),a("el-form-item",{attrs:{label:"站点"}},[a("el-select",{attrs:{placeholder:"请选择站点"},model:{value:t.templateChangeForm.station,callback:function(e){t.$set(t.templateChangeForm,"station",e)},expression:"templateChangeForm.station"}},t._l(t.templateChange_stations,function(t,e){return a("el-option",{key:e,attrs:{label:t,value:t}})}),1)],1),t._v(" "),a("el-form-item",{attrs:{label:"仓库"}},[a("el-select",{attrs:{placeholder:"请选择需要新增的仓库"},model:{value:t.templateChangeForm.warehouse_name,callback:function(e){t.$set(t.templateChangeForm,"warehouse_name",e)},expression:"templateChangeForm.warehouse_name"}},t._l(t.templateChange_warehouses,function(t,e){return a("el-option",{key:e,attrs:{label:t.warehouse_name,value:t.warehouse_name}})}),1)],1),t._v(" "),a("el-form-item",{attrs:{label:"模板"}},[a("el-select",{attrs:{placeholder:"请选择需要模板"},model:{value:t.templateChangeForm.template_type,callback:function(e){t.$set(t.templateChangeForm,"template_type",e)},expression:"templateChangeForm.template_type"}},t._l(t.templateChange_templateTypes,function(t,e){return a("el-option",{key:e,attrs:{label:t,value:t}})}),1)],1),t._v(" "),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:t.getTemplate}},[t._v("模板搜索")])],1)],1)],1),t._v(" "),a("div",{staticClass:"templateModel"},[a("div",{staticClass:"complete_template"},[a("el-input",{attrs:{placeholder:"请输入模板标题,示例：（自动化，加急，隔日达，当天达 + 1天备货时间）"},model:{value:t.templateStepList[0].title,callback:function(e){t.$set(t.templateStepList[0],"title",e)},expression:"templateStepList[0].title"}}),t._v(" "),t._l(t.templateStepList,function(e,l){return a("div",{key:l,staticClass:"stepCard"},[l>0?a("div",[a("p",{staticClass:"step"},[t._v("步骤"+t._s(e.step))]),t._v(" "),a("el-input",{attrs:{type:"text",placeholder:t.hTitle_placeholder(l)},model:{value:e.title,callback:function(a){t.$set(e,"title",a)},expression:"item.title"}}),t._v(" "),a("el-input",{attrs:{type:"textarea",placeholder:t.hTip_placeholder(l)},model:{value:e.content,callback:function(a){t.$set(e,"content",a)},expression:"item.content"}}),t._v(" "),a("div",{staticClass:"img_con"},t._l(e.images.split(","),function(e,l){return a("img",{key:l,attrs:{src:"/home/beyoung_operate/static/data/template_datas/"+t.templateChangeForm.station+"/"+t.templateChangeForm.country+"/"+t.templateChangeForm.warehouse_name+"/"+t.templateChangeForm.template_type+"/"+e,alt:""}})}),0),t._v(" "),a("div",{staticClass:"confirm"},[a("el-upload",{ref:"uploadImg"+e.step,refInFor:!0,attrs:{action:"https://jsonplaceholder.typicode.com/posts/","list-type":"picture-card","auto-upload":!1,drag:"",multiple:""},scopedSlots:t._u([{key:"file",fn:function(e){var s=e.file;return a("div",{},[a("img",{staticClass:"el-upload-list__item-thumbnail",attrs:{src:s.url,alt:""}}),t._v(" "),a("span",{staticClass:"el-upload-list__item-actions"},[a("span",{staticClass:"el-upload-list__item-preview",on:{click:function(e){return t.handlePictureCardPreview(s)}}},[a("i",{staticClass:"el-icon-zoom-in"})]),t._v(" "),t.disabled?t._e():a("span",{staticClass:"el-upload-list__item-delete",on:{click:function(e){return t.handleRemove(s,"uploadImg"+l)}}},[a("i",{staticClass:"el-icon-delete"})])])])}}],null,!0)},[a("i",{staticClass:"el-icon-plus",attrs:{slot:"default"},slot:"default"})]),t._v(" "),a("el-dialog",{attrs:{visible:t.dialogVisible},on:{"update:visible":function(e){t.dialogVisible=e}}},[a("img",{attrs:{width:"100%",src:t.dialogImageUrl,alt:""}})])],1)],1):t._e()])})],2),t._v(" "),a("div",{staticClass:"submitBtn"},[a("el-button",{attrs:{type:"primary"},on:{click:t.submitFormData}},[t._v("提交模板")])],1)])])])},staticRenderFns:[]};var r=a("VU/8")(n,o,!1,function(t){a("ToRl"),a("hjOp")},"data-v-1807e70b",null);e.default=r.exports},hjOp:function(t,e){}});
//# sourceMappingURL=52.74ae3e967d3111b1f385.js.map
webpackJsonp([14],{GdUM:function(t,e){},s1Nq:function(t,e,i){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var a=i("bOdI"),l=i.n(a),o={data:function(){var t;return t={flag:!1,DialogVisible:!1,addFormRules:{country:[{required:!0,message:"请输入国家",trigger:"blur"}],site:[{required:!0,message:"请输入站点",trigger:"blur"}],manual_name:[{required:!0,message:"请输入手动组名称",trigger:"blur"}],automatic_name:[{required:!0,message:"请输入自动组名称",trigger:"blur"}]},addForm:{country:"",site:"",manual_name:"",automatic_name:""},DialogVisible1:!1,editFormRules:{country:[{required:!0,message:"请输入国家",trigger:"blur"}],site:[{required:!0,message:"请输入站点",trigger:"blur"}],manual_name:[{required:!0,message:"请输入手动组名称",trigger:"blur"}],automatic_name:[{required:!0,message:"请输入自动组名称",trigger:"blur"}]},editForm:{id:"",country:"",site:"",manual_name:"",automatic_name:""},menuPlatFormList:[],showCountryList:[],menuSiteList:[]},l()(t,"showCountryList",""),l()(t,"showSiteList",""),l()(t,"lastSiteList",""),l()(t,"checkedPlatform",""),l()(t,"checkedCountry",""),l()(t,"checkedSite",""),l()(t,"lastSiteList",[]),l()(t,"tableList",[{xx:112},{xx:3334}]),l()(t,"multipleSelection",[]),l()(t,"id",""),l()(t,"deleteVisible",!1),t},created:function(){this.getMenuList()},methods:{deleteSubmit:function(){var t=this;this.deleteVisible=!1,this.$api2.AMdeleteFormData({id:this.id}).then(function(e){console.log(e),200===e.data.code?(t.$message.success("请求成功"),t.multipleSelection=[],t.getTableData()):t.$message.warning("请求失败")})},go_route:function(t){this.$router.push({path:t})},select:function(t,e){if(this.multipleSelection=[],t.length>1){var i=t.shift();this.$refs.multipleTable.toggleRowSelection(i,!1)}this.multipleSelection.push(t[0]),console.log("当用户手动勾选数据行",this.multipleSelection)},selectAll:function(t){this.multipleSelection=[],console.log("当用户手动勾选全选 Checkbox 时触发的事件",t),t.length>1?(t.length=1,this.multipleSelection.push(t[0])):this.multipleSelection.push(t[0]),console.log("当用户手动勾选全选",this.multipleSelection)},openedit:function(){if(this.flag)if(0===this.multipleSelection.length||1===this.multipleSelection.length&&void 0===this.multipleSelection[0])this.$message.warning("请选择一个数据进行编辑");else{for(var t in this.DialogVisible1=!0,this.editForm)this.editForm[t]="";var e=this.multipleSelection[0];for(var i in console.log("当前选中的对象",e),this.editForm)this.editForm[i]=e[i]}},addNewdata:function(){if(this.flag){for(var t in this.DialogVisible=!0,this.addForm)this.addForm[t]="";this.addForm.country=this.checkedCountry,this.addForm.site=this.checkedSite}},deleteData:function(){0===this.multipleSelection.length||1===this.multipleSelection.length&&void 0===this.multipleSelection[0]?this.$message.warning("请选择一个数据删除"):(this.id=this.multipleSelection[0].id,console.log(this.id),this.deleteVisible=!0)},addSubmit:function(t){var e=this;this.$refs[t].validate(function(t){if(t){e.DialogVisible=!1;var i=new FormData;for(var a in e.addForm)i.append(a,e.addForm[a]);e.$api2.AMAddSubmit(i).then(function(t){console.log(t),200===t.data.code?(e.$message.success("请求成功"),e.getTableData()):e.$message.warning("请求不成功")})}})},addReset:function(){for(var t in this.addForm)console.log(t),"country"!==t&&"site"!==t&&(this.addForm[t]="")},editSubmit:function(t){var e=this;this.$refs[t].validate(function(t){if(t){e.DialogVisible1=!1;var i=new FormData;for(var a in e.editForm)i.append(a,e.editForm[a]);e.$api2.AMeditFormData(i).then(function(t){console.log(t),200===t.data.code?(e.$message.success("请求成功"),e.getTableData(),e.multipleSelection=[]):e.$message.warning("请求失败")})}})},editReset:function(){for(var t in this.editForm)"country"!==t&&"site"!==t&&"id"!==t&&(this.editForm[t]="")},indexMethod:function(t){return t+1},getMenuList:function(){var t=this;this.$api.getMenuList().then(function(e){t.menuPlatFormList=e.data.data1,t.menuCountryList=e.data.data2,t.menuSiteList=e.data.data3,t.showCountryList=t.menuCountryList[0],t.showSiteList=t.menuSiteList[0],t.lastSiteList=t.showSiteList[0],t.checkedPlatform=t.menuPlatFormList[0],t.checkedCountry=t.showCountryList[0],t.checkedSite=t.lastSiteList[0],t.thirdClick(t.checkedPlatform,t.checkedCountry,t.checkedSite)})},onceClick:function(t){this.showCountryList=[],this.showSiteList=[],this.showCountryList=this.menuCountryList[t],this.showSiteList=this.menuSiteList[t]},secondClick:function(t){this.lastSiteList=[],this.lastSiteList=this.showSiteList[t]},getTableData:function(){var t=this;this.$api2.AMgetTableData({country:this.checkedCountry,site:this.checkedSite}).then(function(e){console.log(e),t.tableList=e.data.re_data||[]})},thirdClick:function(t,e,i){console.log("渠道站点国家",t,e,i),this.checkedCountry=e,this.checkedSite=i,this.flag=!0,this.getTableData()}}},s={render:function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{attrs:{id:"AutoManualGroup"}},[i("div",{staticClass:"leftMenu"},[i("el-menu",{staticClass:"el-menu-vertical-demo",attrs:{"default-active":"0-0-0","unique-opened":""}},t._l(t.menuPlatFormList,function(e,a){return i("el-submenu",{key:a,attrs:{index:a+""}},[i("template",{slot:"title"},[i("span",{staticStyle:{display:"inline-block",width:"100%"},on:{click:function(e){return t.onceClick(a)}}},[t._v(t._s(e))])]),t._v(" "),t._l(t.showCountryList,function(l,o){return i("el-submenu",{key:o,attrs:{index:a+"-"+o}},[i("template",{slot:"title"},[i("span",{staticStyle:{display:"inline-block",width:"100%"},on:{click:function(e){return t.secondClick(o)}}},[t._v(t._s(l))])]),t._v(" "),t._l(t.lastSiteList,function(s,n){return i("el-menu-item",{key:n,attrs:{index:a+"-"+o+"-"+n},on:{click:function(i){return t.thirdClick(e,l,s)}}},[i("span",[t._v(t._s(s))])])})],2)})],2)}),1)],1),t._v(" "),i("div",{staticClass:"right_box"},[i("div",{staticClass:"topOpt"},[i("el-button",{staticClass:"Btn",attrs:{type:"primary",size:"small"},on:{click:t.addNewdata}},[t._v("新增")]),t._v(" "),i("el-button",{staticClass:"Btn",attrs:{size:"small",type:"primary"},on:{click:t.openedit}},[t._v("编辑")]),t._v(" "),i("el-button",{staticClass:"Btn",attrs:{type:"danger",size:"small"},on:{click:t.deleteData}},[t._v("删除")]),t._v(" "),i("el-button",{staticClass:"Btn",attrs:{type:"primary",size:"small"},on:{click:function(e){return t.go_route("/AdSyncGroupControl")}}},[t._v("广告组合spu对应关系")])],1),t._v(" "),i("el-table",{ref:"multipleTable",staticStyle:{width:"1000"},attrs:{"max-height":"800",border:"",data:t.tableList},on:{"select-all":t.selectAll,select:t.select}},[i("el-table-column",{attrs:{type:"selection",width:"55"}}),t._v(" "),i("el-table-column",{attrs:{type:"index",label:"序号",index:t.indexMethod,width:"55",align:"center"}}),t._v(" "),i("el-table-column",{attrs:{prop:"country",width:"80",label:"国家"}}),t._v(" "),i("el-table-column",{attrs:{prop:"site",width:"80",label:"站点"}}),t._v(" "),i("el-table-column",{attrs:{prop:"manual_name",width:"300",label:"手动组名称"}}),t._v(" "),i("el-table-column",{attrs:{prop:"automatic_name",width:"380",label:"自动组名称"}})],1),t._v(" "),i("el-dialog",{attrs:{title:"新增",visible:t.DialogVisible,"close-on-click-modal":!1,width:"55%",center:""},on:{"update:visible":function(e){t.DialogVisible=e}}},[i("el-form",{ref:"addFormDialog",attrs:{rules:t.addFormRules,model:t.addForm,inline:!0,"label-width":"100px"}},[i("el-form-item",{attrs:{prop:"country",label:"国家"}},[i("el-input",{attrs:{readonly:""},model:{value:t.addForm.country,callback:function(e){t.$set(t.addForm,"country",e)},expression:"addForm.country"}})],1),t._v(" "),i("el-form-item",{attrs:{label:"站点",prop:"site"}},[i("el-input",{attrs:{readonly:""},model:{value:t.addForm.site,callback:function(e){t.$set(t.addForm,"site",e)},expression:"addForm.site"}})],1),t._v(" "),i("el-form-item",{attrs:{prop:"manual_name",label:"手动组名称"}},[i("el-input",{model:{value:t.addForm.manual_name,callback:function(e){t.$set(t.addForm,"manual_name",e)},expression:"addForm.manual_name"}})],1),t._v(" "),i("el-form-item",{attrs:{prop:"automatic_name",label:"自动组名称"}},[i("el-input",{attrs:{placeholder:"多个spu请以英文,分割"},model:{value:t.addForm.automatic_name,callback:function(e){t.$set(t.addForm,"automatic_name",e)},expression:"addForm.automatic_name"}})],1),t._v(" "),i("el-form-item",{staticClass:"lastBtnGroup"},[i("el-button",{attrs:{type:"primary"},on:{click:function(e){return t.addSubmit("addFormDialog")}}},[t._v("提 交")]),t._v(" "),i("el-button",{attrs:{type:"warning"},on:{click:t.addReset}},[t._v("重 置")])],1)],1)],1),t._v(" "),i("el-dialog",{attrs:{title:"编辑",visible:t.DialogVisible1,"close-on-click-modal":!1,width:"20%",center:""},on:{"update:visible":function(e){t.DialogVisible1=e}}},[i("el-form",{ref:"editFormDialog",attrs:{rules:t.editFormRules,model:t.editForm,inline:!0,"label-width":"100px"}},[i("el-form-item",{attrs:{prop:"country",label:"国家"}},[i("el-input",{attrs:{readonly:""},model:{value:t.editForm.country,callback:function(e){t.$set(t.editForm,"country",e)},expression:"editForm.country"}})],1),t._v(" "),i("el-form-item",{attrs:{label:"站点",prop:"site"}},[i("el-input",{attrs:{readonly:""},model:{value:t.editForm.site,callback:function(e){t.$set(t.editForm,"site",e)},expression:"editForm.site"}})],1),t._v(" "),i("el-form-item",{attrs:{prop:"manual_name",label:"手动组名称"}},[i("el-input",{model:{value:t.editForm.manual_name,callback:function(e){t.$set(t.editForm,"manual_name",e)},expression:"editForm.manual_name"}})],1),t._v(" "),i("el-form-item",{attrs:{prop:"automatic_name",label:"自动组名称"}},[i("el-input",{model:{value:t.editForm.automatic_name,callback:function(e){t.$set(t.editForm,"automatic_name",e)},expression:"editForm.automatic_name"}})],1),t._v(" "),i("el-form-item",{staticClass:"lastBtnGroup"},[i("el-button",{attrs:{type:"primary"},on:{click:function(e){return t.editSubmit("editFormDialog")}}},[t._v("保 存")]),t._v(" "),i("el-button",{attrs:{type:"warning"},on:{click:t.editReset}},[t._v("重 置")])],1)],1)],1),t._v(" "),i("el-dialog",{attrs:{title:"提示",visible:t.deleteVisible,width:"30%"},on:{"update:visible":function(e){t.deleteVisible=e}}},[i("span",[t._v("确认删除？")]),t._v(" "),i("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[i("el-button",{on:{click:function(e){t.deleteVisible=!1}}},[t._v("取 消")]),t._v(" "),i("el-button",{attrs:{type:"primary"},on:{click:t.deleteSubmit}},[t._v("确 定")])],1)])],1)])},staticRenderFns:[]};var n=i("VU/8")(o,s,!1,function(t){i("voM8"),i("GdUM"),i("tNZj")},"data-v-767b2f70",null);e.default=n.exports},tNZj:function(t,e){},voM8:function(t,e){}});
//# sourceMappingURL=14.bbb0a0cd5d90ef39a6e9.js.map
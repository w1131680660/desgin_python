webpackJsonp([61],{"2Fj8":function(e,t){},b65k:function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var a={name:"",props:{},components:{orderNav:r("uuOi").a},data:function(){return{waitOrder:[],fromRules:{transferDpm:[{type:"string",required:!0,message:"请选择转派部门",trigger:"change"}],transferStaff:[{type:"string",required:!0,message:"请选择转派人员",trigger:"change"}],rejectReason:[{required:!0,message:"请填写驳回原因",trigger:"blur"}]},departmentList:[],staff:[],transferVisible:!1,transferForm:{transferDpm:"",transferStaff:"",transferId:""},rejectVisible:!1,rejectForm:{rejectId:"",rejectReason:""}}},computed:{},watch:{},methods:{getWaitOrder:function(){var e=this;this.$api.getWaitOrder().then(function(t){console.log(t),e.waitOrder=t.data.data})},acceptOrder:function(e){var t=this;console.log(e),this.$confirm("是否要接取该工单",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then(function(){t.$api.acceptOrder(e).then(function(e){console.log(e),t.getWaitOrder(),t.$message.success("接取成功")})}).catch(function(){})},getSelectData:function(){var e=this;this.$api.getOrderSelectData().then(function(t){console.log(t),e.departmentList=t.data.data})},departmentChange:function(e){var t=this;this.$api.getReceivePerson(e).then(function(e){console.log(e),t.staff=e.data.data})},transferOrder:function(e){this.transferForm.transferId=e,this.getSelectData(),this.transferVisible=!0},transferConfirm:function(){var e=this;this.$refs.transferRef.validate(function(t){t&&e.$api.transferOrder(e.transferForm).then(function(t){console.log(t),e.getWaitOrder(),e.$message.success("转派成功"),e.transferVisible=!1})})},transferClose:function(){this.$refs.transferRef.resetFields()},rejectOrder:function(e){var t=this;this.$confirm("是否要驳回该工单",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then(function(){t.$api.rejectOrder(e).then(function(e){console.log(e),t.getWaitOrder(),t.$message.success("驳回成功")})}).catch(function(){})},rejectConfirm:function(){var e=this;this.$refs.rejectRef.validate(function(t){t&&e.$api.rejectOrder(e.rejectForm).then(function(t){console.log(t),e.getWaitOrder(),e.$message.success("驳回成功"),e.rejectVisible=!1})})},rejectClose:function(){this.$refs.rejectRef.resetFields()}},created:function(){this.getWaitOrder()},mounted:function(){}},n={render:function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{attrs:{id:"order-wait"}},[r("order-nav"),e._v(" "),r("h3",[e._v("待处理工单")]),e._v(" "),r("el-table",{staticStyle:{width:"80%",margin:"0 auto","margin-top":"24px"},attrs:{data:e.waitOrder,border:"","max-height":"500",size:"small"}},[r("el-table-column",{attrs:{type:"index",label:"序号",width:"60"}}),e._v(" "),r("el-table-column",{attrs:{prop:"initiate_department",label:"发单部门"}}),e._v(" "),r("el-table-column",{attrs:{prop:"initiate_person",label:"发单人"}}),e._v(" "),r("el-table-column",{attrs:{prop:"initiate_time",label:"发单时间"}}),e._v(" "),r("el-table-column",{attrs:{prop:"out_time",label:"结单时间"}}),e._v(" "),r("el-table-column",{attrs:{prop:"job_type",label:"工单类型"}}),e._v(" "),r("el-table-column",{attrs:{prop:"need",label:"内容需求"}}),e._v(" "),r("el-table-column",{attrs:{label:"操作",width:"220"},scopedSlots:e._u([{key:"default",fn:function(t){var a=t.row;return[r("div",[r("el-button",{attrs:{type:"primary",size:"mini"},on:{click:function(t){return e.acceptOrder(a.id)}}},[e._v("接取")]),e._v(" "),r("el-button",{attrs:{type:"primary",size:"mini"},on:{click:function(t){return e.transferOrder(a.id)}}},[e._v("转派")]),e._v(" "),r("el-button",{attrs:{type:"danger",size:"mini"},on:{click:function(t){return e.rejectOrder(a.id)}}},[e._v("驳回")])],1)]}}])})],1),e._v(" "),r("el-dialog",{attrs:{visible:e.transferVisible,width:"30%",center:""},on:{"update:visible":function(t){e.transferVisible=t},close:e.transferClose}},[r("el-form",{ref:"transferRef",attrs:{model:e.transferForm,rules:e.fromRules,"label-width":"100px"}},[r("el-form-item",{attrs:{label:"转派部门",prop:"transferDpm"}},[r("el-select",{attrs:{placeholder:"请选择"},on:{change:e.departmentChange},model:{value:e.transferForm.transferDpm,callback:function(t){e.$set(e.transferForm,"transferDpm",t)},expression:"transferForm.transferDpm"}},e._l(e.departmentList,function(e,t){return r("el-option",{key:t,attrs:{label:e,value:e}})}),1)],1),e._v(" "),r("el-form-item",{attrs:{label:"转派人员",prop:"transferStaff"}},[r("el-select",{attrs:{placeholder:"请选择"},model:{value:e.transferForm.transferStaff,callback:function(t){e.$set(e.transferForm,"transferStaff",t)},expression:"transferForm.transferStaff"}},e._l(e.staff,function(e,t){return r("el-option",{key:t,attrs:{label:e,value:e}})}),1)],1)],1),e._v(" "),r("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[r("el-button",{attrs:{type:"primary"},on:{click:e.transferConfirm}},[e._v("确 认")])],1)],1),e._v(" "),r("el-dialog",{attrs:{visible:e.rejectVisible,width:"30%",center:""},on:{"update:visible":function(t){e.rejectVisible=t},close:e.rejectClose}},[r("el-form",{ref:"rejectRef",attrs:{model:e.rejectForm,rules:e.fromRules,"label-width":"100px"}},[r("el-form-item",{attrs:{label:"驳回原因",prop:"rejectReason"}},[r("el-input",{attrs:{type:"textarea"},model:{value:e.rejectForm.rejectReason,callback:function(t){e.$set(e.rejectForm,"rejectReason",t)},expression:"rejectForm.rejectReason"}})],1)],1),e._v(" "),r("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[r("el-button",{attrs:{type:"primary"},on:{click:e.rejectConfirm}},[e._v("确 认")])],1)],1)],1)},staticRenderFns:[]};var s=r("VU/8")(a,n,!1,function(e){r("2Fj8")},"data-v-f6cf8cba",null);t.default=s.exports}});
//# sourceMappingURL=61.6d06f01043219863de6b.js.map
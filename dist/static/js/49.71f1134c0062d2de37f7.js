webpackJsonp([49],{"/B4x":function(t,e){},cYeE:function(t,e){},szOA:function(t,e,i){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n={name:"",props:{},components:{orderNav:i("uuOi").a},data:function(){return{queryInfo:{form:{checkedDpm:"",checkedStaff:"",checkedType:"",checkedDate:"",page:1},departmentList:[],staff:[],type:["及时","远期"]},orderGatherList:[],checkedList:[],indexList:[],status:0}},computed:{},watch:{},methods:{getAcceptedOrderList:function(){var t=this,e=this.$store.state.userName;this.$api.queryAccepted(e).then(function(e){console.log(e),t.orderGatherList=e.data.data})},goTop:function(){var t=this;if(this.checkedList.find(function(t){return 1==t})){for(var e in this.indexList=[],this.checkedList.forEach(function(e,i){1==e&&t.indexList.push(i)}),this.indexList){var i=this.orderGatherList[this.indexList[e]];this.orderGatherList.splice(this.indexList[e],1),this.orderGatherList.unshift(i)}for(var n in this.checkedList)this.$set(this.checkedList,n,!1)}else this.$message.error("请勾选工单")},jiedan:function(t){var e=this;console.log(t),this.$confirm("确定结单吗？",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then(function(){e.$api.jiedan(t).then(function(t){console.log(t),e.$message.success("结单成功"),e.getAcceptedOrderList()})}).catch(function(){})},getSelectData:function(){var t=this;this.$api.getSelectData().then(function(e){console.log(e),t.queryInfo.departmentList=e.data.department_list})},departmentChange:function(t){var e=this;this.$api.getSelectData(t).then(function(t){console.log(t),e.queryInfo.staff=t.data.person_list})},queryOrder:function(){var t=this;this.$api.queryAccepted(this.queryInfo.form).then(function(e){console.log(e),t.orderGatherList=e.data.data})}},created:function(){this.getAcceptedOrderList()},mounted:function(){}},a={render:function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{attrs:{id:"order-received"}},[i("order-nav"),t._v(" "),i("h3",[t._v("已接工单")]),t._v(" "),i("div",{staticClass:"order_table"},[i("el-table",{staticStyle:{width:"90%",margin:"0 auto"},attrs:{data:t.orderGatherList,border:"","max-height":"500",size:"small"}},[i("el-table-column",{attrs:{type:"index",label:"序号",width:"60"}}),t._v(" "),i("el-table-column",{attrs:{prop:"initiate_person",label:"发单人"}}),t._v(" "),i("el-table-column",{attrs:{prop:"initiate_time",label:"发单时间"}}),t._v(" "),i("el-table-column",{attrs:{prop:"out_time",label:"结单时间"}}),t._v(" "),i("el-table-column",{attrs:{prop:"need",label:"内容需求"}}),t._v(" "),i("el-table-column",{attrs:{prop:"next_info",label:"跟进信息"}}),t._v(" "),i("el-table-column",{attrs:{prop:"job_type",label:"工单类型"}}),t._v(" "),i("el-table-column",{attrs:{prop:"status",label:"状态"}}),t._v(" "),i("el-table-column",{attrs:{label:"结单",width:"180"},scopedSlots:t._u([{key:"default",fn:function(e){var n=e.row;return["进行中"==n.status?i("div",[i("el-button",{attrs:{type:"primary",size:"mini"},on:{click:function(e){return t.jiedan(n.id)}}},[t._v("结单")])],1):t._e()]}}])})],1)],1)],1)},staticRenderFns:[]};var r=i("VU/8")(n,a,!1,function(t){i("cYeE"),i("/B4x")},"data-v-1fcd719d",null);e.default=r.exports}});
//# sourceMappingURL=49.71f1134c0062d2de37f7.js.map
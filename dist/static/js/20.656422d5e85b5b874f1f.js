webpackJsonp([20],{BcNX:function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var a={data:function(){return{currentPage:1,totalNum:0,selectForm:{warehouse:"",country:"",orderid:"",state:1},carries:[],warehouse_country:[],country_order:[],countries:[],ordernums:[],orderstates:[{label:"未处理",value:0},{label:"已处理",value:1}],historyOrder:[]}},methods:{query:function(){this.orderlist()},indexMethod:function(e){return e+1+50*(this.currentPage-1)},pageChange:function(e){this.currentPage=e,this.orderlist()},changeCountry:function(){var e=this;this.selectForm.country&&this.country_order.forEach(function(t){console.log(t.country,e.selectForm.country),t.country===e.selectForm.country&&(e.ordernums=t.orderid||[],e.selectForm.orderid=e.ordernums.length>0?e.ordernums[0]:"")})},getSelect:function(e){var t=this;this.$axios.get(this._url2+"server/order_management/get_warehouse/").then(function(r){t.carries=r.data.warehouse_list||[],t.selectForm.warehouse=t.carries.length>0?t.carries[0]:"",t.country_order=r.data.country_order||[],t.$axios.get(t._url2+"server/personnel_management/get_sign_country/").then(function(r){t.countries=r.data.data||[],t.selectForm.country=t.countries.length>0?t.countries[0]:"",t.changeCountry(),e&&"function"==typeof e&&e()})})},orderlist:function(){var e=this,t={};for(var r in this.selectForm)""!==this.selectForm[r]&&(t[r]=this.selectForm[r]);t.page=this.currentPage,this.$axios.get(this._url2+"server/order_management/get_bad_order/",{params:t}).then(function(t){e.historyOrder=t.data.data,e.totalNum=t.data.total_num,e.$nextTick(function(){e.$refs.phTable.bodyWrapper.scrollTop=0})})}},created:function(){this.getSelect(this.orderlist)}},l={render:function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"historyList"},[r("div",{staticClass:"left_box"},[r("el-form",{staticClass:"demo-form-inline",attrs:{inline:!0,model:e.selectForm}},[r("el-form-item",{attrs:{label:"海外仓承运商"}},[r("el-select",{model:{value:e.selectForm.warehouse,callback:function(t){e.$set(e.selectForm,"warehouse",t)},expression:"selectForm.warehouse"}},e._l(e.carries,function(e,t){return r("el-option",{key:t,attrs:{label:e,value:e}})}),1)],1),e._v(" "),r("el-form-item",{attrs:{label:"国家"}},[r("el-select",{on:{change:e.changeCountry},model:{value:e.selectForm.country,callback:function(t){e.$set(e.selectForm,"country",t)},expression:"selectForm.country"}},e._l(e.countries,function(e,t){return r("el-option",{key:t,attrs:{label:e,value:e}})}),1)],1),e._v(" "),r("el-form-item",{attrs:{label:"订单号"}},[r("el-select",{attrs:{filterable:""},model:{value:e.selectForm.orderid,callback:function(t){e.$set(e.selectForm,"orderid",t)},expression:"selectForm.orderid"}},e._l(e.ordernums,function(e,t){return r("el-option",{key:t,attrs:{label:e,value:e}})}),1)],1),e._v(" "),r("el-form-item",{attrs:{label:"订单状态"}},[r("el-select",{attrs:{filterable:""},model:{value:e.selectForm.state,callback:function(t){e.$set(e.selectForm,"state",t)},expression:"selectForm.state"}},e._l(e.orderstates,function(e,t){return r("el-option",{key:t,attrs:{label:e.label,value:e.value}})}),1)],1),e._v(" "),r("el-form-item",[r("el-button",{attrs:{type:"primary"},on:{click:e.query}},[e._v("搜索")])],1)],1)],1),e._v(" "),r("div",{staticClass:"right_box"},[r("el-table",{ref:"phTable",staticStyle:{width:"100%"},attrs:{"max-height":"750",border:"",data:e.historyOrder}},[r("el-table-column",{attrs:{type:"index",label:"序号",width:"60",align:"center",index:e.indexMethod}}),e._v(" "),r("el-table-column",{attrs:{prop:"sys_num",label:"系统单号",width:"160",align:"center"}}),e._v(" "),r("el-table-column",{attrs:{prop:"order_num",label:"订单号",width:"160",align:"center"}}),e._v(" "),r("el-table-column",{attrs:{prop:"product_code",label:"产品编码",width:"100",align:"center"}}),e._v(" "),r("el-table-column",{attrs:{prop:"fbm_carrites",label:"海外仓承运商",width:"140",align:"center"}}),e._v(" "),r("el-table-column",{attrs:{prop:"product_name",label:"品名",width:"240",align:"center"}}),e._v(" "),r("el-table-column",{attrs:{prop:"sku",label:"sku",width:"240",align:"center"}}),e._v(" "),r("el-table-column",{attrs:{prop:"country",label:"国家",width:"100",align:"center"}}),e._v(" "),r("el-table-column",{attrs:{prop:"receive_name",label:"收件人",width:"100",align:"center"}}),e._v(" "),r("el-table-column",{attrs:{prop:"problem_reason",label:"问题原因",width:"100",align:"center"}}),e._v(" "),r("el-table-column",{attrs:{prop:"order_state",label:"订单状态",width:"100",align:"center"}})],1),e._v(" "),r("el-pagination",{attrs:{"current-page":e.currentPage,"page-size":50,layout:"total, prev, pager, next,jumper",total:e.totalNum},on:{"current-change":e.pageChange,"update:currentPage":function(t){e.currentPage=t},"update:current-page":function(t){e.currentPage=t}}})],1)])},staticRenderFns:[]};var n=r("VU/8")(a,l,!1,function(e){r("q2kY"),r("yEdx"),r("k+cp")},"data-v-28a5ebae",null);t.default=n.exports},"k+cp":function(e,t){},q2kY:function(e,t){},yEdx:function(e,t){}});
//# sourceMappingURL=20.656422d5e85b5b874f1f.js.map